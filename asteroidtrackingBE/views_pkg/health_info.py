import time
from flask import Blueprint, request
from commons_pkg.commons import frontend_stream_name, request_handler, microservice_stream_name


health_bp = Blueprint('health_bp', __name__, url_prefix='/')


@health_bp.route('health/service', methods=['GET'])
def service_health_info():
    """
    Flask Handler for DELETING asteroid info; DELETE CALL
    """
    try:
        service_name = request.args.get('name', None)
        if service_name:
            body = dict()
            body.update(method='fetch_service_health', service_name=service_name)
            body.update(response_stream_name=frontend_stream_name)
            ret, ret_code = request_handler(request, body, microservice_stream_name, health_check=True)
        else:
            msg = {
                'error': 'Error Occurred',
                'message': f'Service name (for which health has to be monitored) is missing. '
                           f'Please supply the service name in the request(API call)',
                'path': request.path,
                'status': 400,
                'timestamp': time.ctime()
            }
            ret, ret_code = msg, msg.get('status')
    except Exception as ex:
        msg = {
            'error': 'Error Occurred',
            'message': ex.__str__(),
            'path': request.path,
            'status': 500,
            'timestamp': time.ctime()
        }
        ret, ret_code = msg, msg.get('status')

    return ret, ret_code
