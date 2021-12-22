import time
from flask import Blueprint, request
from commons_pkg.commons import frontend_stream_name, request_handler


asteroids_bp = Blueprint('asteroids_bp', __name__, url_prefix='/')


@asteroids_bp.route('asteroid/create', methods=['POST'])
def create_asteroid():
    try:
        # get the details of asteroid to be added
        body = request.json
        body.update(method=request.method)
        body.update(response_stream_name=frontend_stream_name)
        ret, ret_code = request_handler(request, body)
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


@asteroids_bp.route('getasteroidinfo/<path:asteroidid>', methods=['GET'])
def get_asteroid_info(asteroidid):
    try:
        body = dict(asteroid_id=asteroidid)
        body.update(method=request.method)
        body.update(response_stream_name=frontend_stream_name)
        ret, ret_code = request_handler(request, body)
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


@asteroids_bp.route('updateasteroid/<path:asteroidid>', methods=['PUT'])
def update_asteroid_info(asteroidid):
    try:
        body = request.json
        body.update(asteroid_id=asteroidid)
        body.update(method=request.method)
        body.update(response_stream_name=frontend_stream_name)
        ret, ret_code = request_handler(request, body)
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


@asteroids_bp.route('deleteasteroid/<path:asteroidid>', methods=['DELETE'])
def delete_asteroid_info(asteroidid):
    try:
        body = dict(asteroid_id=asteroidid)
        body.update(method=request.method)
        body.update(response_stream_name=frontend_stream_name)
        ret, ret_code = request_handler(request, body)
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

