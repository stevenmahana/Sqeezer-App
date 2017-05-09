from flask import Blueprint, request, jsonify, abort, make_response, render_template
import json
import os

from config import ProductionConfig
from src.resource import Sqeezer


access_key = ProductionConfig.AWS_ACCESS_KEY_ID
secret_key = ProductionConfig.AWS_SECRET_ACCESS_KEY

actions = ['sqz_compress_test_result', 'sqz_compress_test', 'lzw_compress_test_result', 'lzw_compress_test']

_FILE = ['png', 'jpg', 'jpeg', 'gif', 'JPG', 'JPEG', 'mp4', 'MP4', 'pdf', 'PDF']
_PATH = os.path.join(ProductionConfig.BASE_PATH, './tmp')

sqeezer1_0 = Blueprint('sqeezer1_0', __name__)


# == [ APP CONTROLLER ] == #
# http://127.0.0.1:5000/v1/sqeezer/ACTION
@sqeezer1_0.route('/<string:action>', methods=['GET'])
def get_sqeezer(action):
    """

    """
    if action not in actions:
        return make_response(jsonify({'error': '400', 'message': 'Method not allowed'}), 400)

    params = {k: v for k, v in request.args.items() if v}

    response = Sqeezer(params).sqeezer_action(str(action))

    # replace this process with a dynamic template
    if response and response['meta']['algorithm'] == 'sqz':
        return render_template('sqz.html', data=response)
    elif response and response['meta']['algorithm'] == 'lzw':
        return render_template('lzw.html', data=response)
    else:
        return render_template('home.html', data={})


# http://127.0.0.1:5000/v1/sqeezer/ACTION
@sqeezer1_0.route('/<string:action>', methods=['PUT'])
def put_sqeezer(action):
    """

    """
    if action not in actions:
        return make_response(jsonify({'error': '400', 'message': 'Method not allowed'}), 400)

    return make_response(jsonify({'error': '400', 'message': 'HTTP Method PUT inactive.'}), 400)


# http://127.0.0.1:5000/v1/sqeezer/ACTION
@sqeezer1_0.route('/<string:action>', methods=['POST'])
def post_sqeezer(action):
    """

    """
    if action not in actions:
        return make_response(jsonify({'error': '400', 'message': 'Method not allowed'}), 400)

    return make_response(jsonify({'error': '400', 'message': 'HTTP Method POST inactive.'}), 400)


# http://127.0.0.1:5000/v1/sqeezer/ACTION
@sqeezer1_0.route('/<string:action>', methods=['DELETE'])
def delete_sqeezer(action):
    """

    """
    if action not in actions:
        return make_response(jsonify({'error': '400', 'message': 'Method not allowed'}), 400)

    return make_response(jsonify({'error': '400', 'message': 'HTTP Method POST inactive.'}), 400)


# == [ UTILITY ] == #
def process_search_params(meth):
    """
    :return: DICT
    """
    if 'Content-Type' not in request.headers and 'application/json' not in request.headers['Content-Type']:
        abort(400, {'message': 'Bad Content-Type in Header'})

    access = {}

    params = {k: v for k, v in request.args.items() if v}  # remove all keys with empty value -- will remove 0

    data = {
        'AUID': access['AUID'] if 'AUID' in access else None,
        'UUID': params['UUID'] if 'UUID' in params else None,
        'object': params['object'] if 'object' in params else None,
        'objectID': params['objectID'] if 'objectID' in params else None,
        'keyword': params['keyword'] if 'keyword' in params else None,
        'results': int(params['results']) if 'results' in params else 20,
        'page': int(params['page']) if 'page' in params else 1,
        'cache': int(params['cache']) if 'cache' in params else 600,
        'http_method': 'GET',
        'method': meth
    }

    return data
