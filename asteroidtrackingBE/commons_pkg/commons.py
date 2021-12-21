import random
import json
from redis_pkg import conn_handlers, redis_library

# creating some global variables for easy implementation. Of course this won't be the way for production code.
frontend_stream_name = 'asteroids_frontend_stream'
microservice_stream_name = 'asteroids_stream'

def getuniqueid():
    min = 000000000000000000000000
    max = 999999999999999999999999
    return str(random.randrange(start=min, stop=max))


def extract_response(data):
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


def request_handler(req, body):
    uid = getuniqueid()
    # send this body to the backend for processing
    # 1. Get the redis connections
    rconn = conn_handlers.connect()
    # 2. add this to redis stream(name): asteroids_stream
    redis_library.add_data_to_stream(rconn=rconn, stream=microservice_stream_name, data={uid: json.dumps(body)})
    response_data = redis_library.read_data_from_stream(
        stream=frontend_stream_name, rconn=rconn, count=1, block=2000
    )

    if response_data:
        data = extract_response(response_data[0][1])
        # print(data)
        data.update(path=req.path)
        response_code = data['response_code']
        del data['response_code']
    else:
        data = {
            'error': 'Error message described below',
            'message': 'Make sure the redis and asteroidprocessor services are running locally',
            'status': 503
        }
    ret = data
    ret_code = data.get('status')

    return ret, ret_code
