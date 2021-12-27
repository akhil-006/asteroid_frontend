import random
import json
from redis_pkg import conn_handlers, redis_library
from logger_pkg.logger import Logger
from redis_pkg.redis_library import ping_redis


frontend_stream_name = 'asteroids_frontend_stream'
microservice_stream_name = 'asteroids_stream'
service = 'asteroidtracking_service'
health_status = ['good', 'poor']


def getuniqueid():
    """
    Generates the unique id which is associated to a particular request and is also associated to a Asteroid(asteroid ID)
    """
    min = 000000000000000000000000
    max = 999999999999999999999999
    return str(random.randrange(start=min, stop=max))


def extract_response(data):
    """
    Extracts the response received by this(front-end) service from the backend service
    """
    actual_data_dict = dict()
    i = 1
    for detail_list in data:
        actual_data_dictionary = detail_list[i]
        # print(actual_data_dictionary)
        for subdetails_dict in actual_data_dictionary:
            actual_data_dict = json.loads(actual_data_dictionary[subdetails_dict].decode())
        i += 1
    actual_data_dict.pop('request_id', None)
    return actual_data_dict


def request_handler(req, body, microservice_strm_name, health_check=False):
    """
    A common request handler which delegates all the (asteroid)requests to the backend service with the help of
    `microservice_stream_name` (backend service)stream.
    """
    uid = getuniqueid()
    # send this body to the backend for processing
    # 1. Get the redis connections
    rconn = conn_handlers.connect()
    objlog = Logger(rconn=rconn, service_name=service)
    objlog.log(
        level='INFO', req_id=uid,
        message=f'request: {req.path}, method: {req.method}, header: {json.dumps({key:value for key, value in req.headers})}, body: {body}'
    )
    # 2. add this to redis stream(name): asteroids_stream
    redis_library.add_data_to_stream(rconn=rconn, stream=microservice_strm_name, data={uid: json.dumps(body)})
    response_data = redis_library.read_data_from_stream(
        stream=frontend_stream_name, rconn=rconn, count=1, block=10000
    )

    if response_data:
        data = extract_response(response_data[0][1])
        # print(data)
        data.update(path=req.path)
        objlog.log(level='INFO', message=f'response: {json.dumps(data)}', type='response', req_id=uid)
    else:
        data = {
            'error': 'Error message described below',
            'message': 'Make sure the redis and backend services are running locally and are functioning properly',
            'response_code': 503
        }
        objlog.log(level='ERROR', message=f'response: {json.dumps(data)}', type='response', req_id=uid)

    ret = data
    if health_check:
        data = ret.copy()
        services = data.get('services', {})
        if services:
            services.update(asteroidTrackingService=health_status[0] if ping_redis(rconn) else health_status[1])
        else:
            services.update({
                'asteroidTrackingService': health_status[0] if ping_redis(rconn) else health_status[1],
                body['service_name']: health_status[1]
            })
            data.update(services=services, status='failed')

        ret = data

    ret_code = data.get('response_code')
    del data['response_code']

    return ret, ret_code
