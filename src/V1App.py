from flask import Blueprint, request, jsonify, abort, make_response, render_template
import json
import os

from config import ProductionConfig
from src.resource import Sqeezer


access_key = ProductionConfig.AWS_ACCESS_KEY_ID
secret_key = ProductionConfig.AWS_SECRET_ACCESS_KEY

methods = ['compress_test_result', 'compress_test', 'compress_test_reset']

_FILE = ['png', 'jpg', 'jpeg', 'gif', 'JPG', 'JPEG', 'mp4', 'MP4', 'pdf', 'PDF']
_PATH = os.path.join(ProductionConfig.BASE_PATH, './tmp')

sqeezer1_0 = Blueprint('sqeezer1_0', __name__)


# == [ APP CONTROLLER ] == #
# http://127.0.0.1:5000/v1/sqeezer/METHOD
@sqeezer1_0.route('/<string:meth>', methods=['GET'])
def get_sqeezer(meth):
    """

    """
    if meth not in methods:
        return make_response(jsonify({'error': '400', 'message': 'Method not allowed'}), 400)

    params = {k: v for k, v in request.args.items() if v}

    response = Sqeezer(params).sqeezer_action(str(meth))

    if response:
        return render_template('tests.html', data=response)
    else:
        return render_template('tests.html', data={})


# http://127.0.0.1:5000/v1/sqeezer/METHOD
@sqeezer1_0.route('/<string:meth>', methods=['PUT'])
def put_sqeezer(meth):
    """

    """
    if meth not in methods:
        return make_response(jsonify({'error': '400', 'message': 'Method not allowed'}), 400)

    sqeezer = Sqeezer.put_sqeezer(process_put_params(meth))

    if sqeezer:
        return make_response(jsonify(sqeezer), 200)
    else:
        return make_response(jsonify({'error': '400', 'message': 'Unable to update sqeezer'}), 400)


# http://127.0.0.1:5000/v1/sqeezer/METHOD
@sqeezer1_0.route('/<string:meth>', methods=['POST'])
def post_sqeezer(meth):
    """

    """
    if meth not in methods:
        return make_response(jsonify({'error': '400', 'message': 'Method not allowed'}), 400)

    sqeezer = Sqeezer.post_sqeezer(process_post_params(meth))

    if sqeezer:
        return make_response(jsonify(sqeezer), 200)
    else:
        return make_response(jsonify({'error': '400', 'message': 'Unable to Update sqeezer'}), 400)


# http://127.0.0.1:5000/v1/sqeezer/
@sqeezer1_0.route('/', methods=['DELETE'])
def delete_sqeezer():
    """

    """
    sqeezer = Sqeezer.put_sqeezer(process_delete_params())

    if sqeezer:
        return make_response(jsonify(sqeezer), 200)
    else:
        return make_response(jsonify({'error': '400', 'message': 'Unable to delete sqeezer'}), 400)


# == [ UTILITY ] == #
def process_search_params(meth):
    """

    : param params:
    :type params:
    :return:
    :rtype:
    """
    if 'Content-Type' not in request.headers and 'application/json' not in request.headers['Content-Type']:
        abort(400, {'message': 'Bad Content-Type in Header'})

    params = {k: v for k, v in request.args.items() if v}  # remove all keys with empty value -- will remove 0
    access = Access.access()

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


def process_put_params(meth):
    """

    : param params:
    :type params:
    :return:
    :rtype:
    """

    data = {}
    access = Access.access()
    auid = access['AUID'] if 'AUID' in access else None

    if meth == 'profile':  # TODO: Complete profile update

        if 'multipart/form-data' not in request.headers['Content-Type']:
            if 'application/x-www-form-urlencoded' not in request.headers['Content-Type']:
                abort(400, {'message': 'Bad Content-Type in Header'})

        params = request.form

        data = {
            'AUID': auid,
            'object': 'document',
            'UUID': params['UUID'] if 'UUID' in params else None,
            'title': params['title'] if 'title' in params else None,
            'bio': params['bio'] if 'bio' in params else None,
            'phone': params['phone'] if 'phone' in params else None,
            'contact': params['contact'] if 'contact' in params else None,
            'streetAddress1': params['streetAddress1'] if 'streetAddress1' in params else None,
            'streetAddress2': params['streetAddress2'] if 'streetAddress2' in params else None,
            'city': params['city'] if 'city' in params else None,
            'stateProvince': params['stateProvince'] if 'stateProvince' in params else None,
            'postalCode': params['postalCode'] if 'postalCode' in params else None,
            'country': params['country'] if 'country' in params else None,
            'longitude': params['longitude'] if 'longitude' in params else None,
            'latitude': params['latitude'] if 'latitude' in params else None,
            'http_method': 'POST',
            'method': meth,
            'results': 1,
            'page': 1,
            'cache': 0
        }

    elif meth == 'grant':

        if 'multipart/form-data' not in request.headers['Content-Type']:
            if 'application/x-www-form-urlencoded' not in request.headers['Content-Type']:
                abort(400, {'message': 'Bad Content-Type in Header'})

        params = request.form

        if 'UUID' not in params:
            abort(400, {'message': 'UUID is required'})

        if 'action' not in params:
            abort(400, {'message': 'action is required'})

        if params['action'] == 'grant_member_access':
            if 'person' not in params:
                abort(400, {'message': 'person list is required'})
            if 'type' not in params:
                abort(400, {'message': 'type is required'})

        elif params['action'] == 'grant_attribute_access':
            if 'attributes' not in params:
                abort(400, {'message': 'attributes list is required'})

        elif params['action'] == 'grant_entity_access':
            if 'object' not in params:
                abort(400, {'message': 'object is required'})
            if 'objectID' not in params:
                abort(400, {'message': 'objectID is required'})

        elif params['action'] == 'grant_classification_access':
            if 'classification' not in params:
                abort(400, {'message': 'classification is required'})

        data = {
            'AUID': auid,
            'UUID': params['UUID'],
            'action': params['action'],
            'person': json.loads(params['person']) if 'person' in params else None,
            'type': params['type'] if 'type' in params else None,
            'attributes': json.loads(params['attributes']) if 'attributes' in params else None,
            'classification': params['classification'] if 'classification' in params else None,
            'object': params['object'] if 'object' in params else None,
            'objectID': params['objectID'] if 'objectID' in params else None,
            'results': int(params['results']) if 'results' in params else 20,
            'page': int(params['page']) if 'page' in params else 1,
            'cache': int(params['cache']) if 'cache' in params else 600,
            'http_method': 'PUT',
            'method': meth
        }

    elif meth == 'remove-grant':

        if 'multipart/form-data' not in request.headers['Content-Type']:
            if 'application/x-www-form-urlencoded' not in request.headers['Content-Type']:
                abort(400, {'message': 'Bad Content-Type in Header'})

        params = request.form

        if 'UUID' not in params:
            abort(400, {'message': 'UUID is required'})

        if 'person' not in params:
            abort(400, {'message': 'personID is required'})

        data = {
            'AUID': auid,
            'UUID': params['UUID'],
            'person': params['person'],
            'results': int(params['results']) if 'results' in params else 20,
            'page': int(params['page']) if 'page' in params else 1,
            'cache': int(params['cache']) if 'cache' in params else 600,
            'http_method': 'PUT',
            'method': meth
        }

    elif meth == 'category':

        if 'multipart/form-data' not in request.headers['Content-Type']:
            if 'application/x-www-form-urlencoded' not in request.headers['Content-Type']:
                abort(400, {'message': 'Bad Content-Type in Header'})

        params = request.form

        if 'UUID' not in params:
            abort(400, {'message': 'UUID is required'})

        if 'category' not in params:
            abort(400, {'message': 'category is required'})

        data = {
            'AUID': auid,
            'UUID': params['UUID'],
            'category': params['category'],
            'results': int(params['results']) if 'results' in params else 20,
            'page': int(params['page']) if 'page' in params else 1,
            'cache': int(params['cache']) if 'cache' in params else 600,
            'http_method': 'PUT',
            'method': meth
        }

    elif meth == 'labels':

        if 'multipart/form-data' not in request.headers['Content-Type']:
            if 'application/x-www-form-urlencoded' not in request.headers['Content-Type']:
                abort(400, {'message': 'Bad Content-Type in Header'})

        params = request.form

        if 'UUID' not in params:
            abort(400, {'message': 'UUID is required'})

        if 'labels' not in params:
            abort(400, {'message': 'labels is required'})

        try:
            labels = json.loads(params['labels']) if 'labels' in params else None
        except Exception as e:
            print('>>> Error: Bad Label - '+str(e))
            abort(400, {'message': 'Bad Label - must be list stored as a json string.'})

        data = {
            'AUID': auid,
            'UUID': params['UUID'],
            'labels': labels,
            'results': int(params['results']) if 'results' in params else 20,
            'page': int(params['page']) if 'page' in params else 1,
            'cache': int(params['cache']) if 'cache' in params else 600,
            'http_method': 'PUT',
            'method': meth
        }

    elif meth == 'batch':

        if 'multipart/form-data' not in request.headers['Content-Type']:
            if 'application/x-www-form-urlencoded' not in request.headers['Content-Type']:
                abort(400, {'message': 'Bad Content-Type in Header'})

        params = request.form

        if 'UUID' not in params:
            abort(400, {'message': 'UUID is required'})

        if 'object' not in params:
            abort(400, {'message': 'object is required'})

        if 'objectID' not in params:
            abort(400, {'message': 'objectID is required'})

        try:
            UUID = json.loads(params['UUID'])
        except Exception as e:
            print('>>> Error: Bad UUID - '+str(e))
            abort(400, {'message': 'Bad UUID - must be list stored as a json string.'})

        data = {
            'AUID': auid,
            'UUID': UUID,
            'object': params['object'],
            'objectID': params['objectID'],
            'results': int(params['results']) if 'results' in params else 20,
            'page': int(params['page']) if 'page' in params else 1,
            'cache': int(params['cache']) if 'cache' in params else 600,
            'http_method': 'PUT',
            'method': meth
        }

    elif meth == 'version':

        if 'multipart/form-data' not in request.headers['Content-Type']:
            if 'application/x-www-form-urlencoded' not in request.headers['Content-Type']:
                abort(400, {'message': 'Bad Content-Type in Header'})

        form = request.form

        if 'UUID' not in form:
            abort(400, {'message': 'UUID is required'})

        if 'version' not in form:
            abort(400, {'message': 'version is required'})

        if 'file' in request.files:

            vd = {'UUID': form['UUID'], 'AUID': auid, 'method': 'document_by_uuid'}
            validate = Neo4j().get_search(vd)  # validate user role and org status
            if not validate['response']:
                abort(400, {'message': 'User is not authorized to upload this document.'})

            file = request.files['file']
            if file and sl.allowed_file(file.filename):

                try:
                    bucket_name = 'crossdeck-document'
                    file_use = 'document'
                    upload_data = {
                        'bucket_name': bucket_name,
                        'UUID': validate['response'][0]['path']
                    }

                    resp = sl.upload_document(upload_data, file)  # streams to S3 from this file
                    print('>> document added to payload')

                    data = {
                        'AUID': auid,
                        'UUID': form['UUID'],
                        'object': 'document',
                        'fileName': resp['file'],
                        'fileUUID': resp['UUID'],
                        'signedURL': resp['url'],
                        'filePath': str(_PATH),
                        'fileUse': file_use,
                        'fileType': 'document',
                        'bucket': bucket_name,
                        'path': validate['response'][0]['path'],
                        'version': form['version'],
                        'http_method': 'PUT',
                        'method': meth,
                        'results': 1,
                        'page': 1,
                        'cache': 0
                    }

                    return data

                except Exception as e:
                    abort(400, {'message': 'An upload error has occurred ' + str(e)})
            else:
                abort(400, {'message': 'Bad File'})

        else:
            abort(400, {'message': 'File is Missing'})

    elif meth == 'revert':

        if 'multipart/form-data' not in request.headers['Content-Type']:
            if 'application/x-www-form-urlencoded' not in request.headers['Content-Type']:
                abort(400, {'message': 'Bad Content-Type in Header'})

        params = request.form

        if 'UUID' not in params:
            abort(400, {'message': 'UUID is required'})

        if 'version' not in params:
            abort(400, {'message': 'version is required'})

        data = {
            'AUID': auid,
            'UUID': params['UUID'],
            'version': params['version'],
            'results': int(params['results']) if 'results' in params else 20,
            'page': int(params['page']) if 'page' in params else 1,
            'cache': int(params['cache']) if 'cache' in params else 600,
            'http_method': 'PUT',
            'method': meth
        }

    elif meth == 'view':

        if 'multipart/form-data' not in request.headers['Content-Type']:
            if 'application/x-www-form-urlencoded' not in request.headers['Content-Type']:
                abort(400, {'message': 'Bad Content-Type in Header'})

        params = request.form

        if 'UUID' not in params:
            abort(400, {'message': 'UUID is required'})

        data = {
            'AUID': auid,
            'UUID': params['UUID'],
            'object': params['object'] if 'object' in params else None,
            'objectID': params['objectID'] if 'objectID' in params else None,
            'keyword': params['keyword'] if 'keyword' in params else None,
            'download': int(params['download']) if 'download' in params else None,
            'favorite': int(params['favorite']) if 'favorite' in params else None,
            'results': int(params['results']) if 'results' in params else 20,
            'page': int(params['page']) if 'page' in params else 1,
            'cache': int(params['cache']) if 'cache' in params else 600,
            'http_method': 'PUT',
            'method': meth
        }

    elif meth == 'activate':

        if 'multipart/form-data' not in request.headers['Content-Type']:
            if 'application/x-www-form-urlencoded' not in request.headers['Content-Type']:
                abort(400, {'message': 'Bad Content-Type in Header'})

        params = request.form

        if 'UUID' not in params:
            abort(400, {'message': 'UUID is required'})

        if 'active' not in params:
            abort(400, {'message': 'active is required'})

        data = {
            'AUID': auid,
            'UUID': params['UUID'],
            'active': params['active'],
            'results': int(params['results']) if 'results' in params else 20,
            'page': int(params['page']) if 'page' in params else 1,
            'cache': int(params['cache']) if 'cache' in params else 600,
            'http_method': 'PUT',
            'method': meth
        }

    return data


def process_post_params(meth):
    """

    :return:
    :rtype:
    """
    data = {}
    access = Access.access()
    auid = access['AUID'] if 'AUID' in access else None

    if 'multipart/form-data' not in request.headers['Content-Type']:
        if 'application/x-www-form-urlencoded' not in request.headers['Content-Type']:
            abort(400, {'message': 'Bad Content-Type in Header'})

    if 'title' not in request.form:
        abort(400, {'message': 'title is required'})

    if 'bio' not in request.form:
        abort(400, {'message': 'bio is required'})

    title = str(request.form['title'])
    form = request.form

    if 'file' in request.files:

        try:
            labels = json.loads(form['labels']) if 'labels' in form else []
        except Exception as e:
            print('>>> Error: Bad Label - '+str(e))
            abort(400, {'message': 'Bad Label - must be list stored as a json string.'})

        file = request.files['file']
        if file and sl.allowed_file(file.filename):

            try:
                bucket_name = 'crossdeck-document'
                data['bucket_name'] = bucket_name
                data['AUID'] = auid
                file_use = request.form['fileUse'] if 'fileUse' in request.form else 'document'

                resp = sl.upload_document(data, file)  # streams to S3 from this file
                print('>> document added to payload')

                data = {
                    'AUID': auid,
                    'UUID': None,
                    'object': 'document',
                    'fileName': resp['file'],
                    'fileUUID': resp['UUID'],
                    'signedURL': resp['url'],
                    'filePath': str(_PATH),
                    'fileUse': file_use,
                    'fileType': 'document',
                    'bucket': bucket_name,
                    'title': title,
                    'bio': str(form['bio']) if 'bio' in form else None,
                    'tags': str(form['tags']) if 'tags' in form else None,
                    'labels': labels,
                    'rules': form['rules'] if 'rules' in form else None,
                    'category': form['category'] if 'category' in form else None,
                    'attribute': form['attribute'] if 'attribute' in form else None,
                    'http_method': 'POST',
                    'method': meth,
                    'results': 1,
                    'page': 1,
                    'cache': 0
                }

                #print(type(labels))
                #print(json.dumps(data, indent=4, sort_keys=True))
                #raise Exception('STOP')

                return data

            except Exception as e:
                abort(400, {'message': 'An upload error has occurred ' + str(e)})
        else:
            abort(400, {'message': 'Bad File'})

    else:

        abort(400, {'message': 'File is Missing'})


def process_delete_params():
    """
    """
    access = Access.access()
    auid = access['AUID'] if 'AUID' in access else None

    if 'multipart/form-data' not in request.headers['Content-Type']:
        if 'application/x-www-form-urlencoded' not in request.headers['Content-Type']:
            abort(400, {'message': 'Bad Content-Type in Header'})

    if 'UUID' not in request.form:
        abort(400, {'message': 'UUID is required'})

    params = request.form

    data = {
        'AUID': auid,
        'UUID': params['UUID'],
        'results': int(params['results']) if 'results' in params else 20,
        'page': int(params['page']) if 'page' in params else 1,
        'cache': int(params['cache']) if 'cache' in params else 600,
        'http_method': 'DELETE',
        'method': 'delete'
    }

    return data


# == [ UTILITY ] == #
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in _FILE
