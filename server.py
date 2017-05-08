from flask import Flask, render_template, make_response, jsonify
from datetime import timedelta
import logging

from src import sqeezer1_0

logging.basicConfig(filename='logs/cd_errors.log', level=logging.DEBUG)


# == [ APP FACTORY ] == #
def create_app(config):

    app = Flask(__name__, template_folder='templates', static_url_path="/static")
    app.permanent_session_lifetime = timedelta(seconds=30)
    app.config.from_object(config)

    # == [ BLUEPRINT ] == #
    app.register_blueprint(sqeezer1_0, url_prefix="/v1/sqeezer")

    @app.route('/')
    def index():
        return render_template('home.html')

    # == [ SECURITY ] == #
    # add auth decorator here

    # == [ ERRORS ] == #
    @app.errorhandler(400)
    def bad_syntax(error):
        logging.exception(error)
        if "message" in error.description:
            return make_response(jsonify({
                "error": "400", "message": error.description["message"]
            }), 400)
        else:
            return make_response(jsonify({
                'error': '400', 'message': 'Bad Syntax - The request cannot be fulfilled due to bad syntax'
            }), 400)

    @app.errorhandler(401)
    def not_authorized(error):
        logging.exception(error)
        if "message" in error.description:
            return make_response(jsonify({
                "error": "401", "message": error.description["message"]
            }), 401)
        else:
            return make_response(jsonify({
                'error': '401', 'message': 'Unauthorized - You are unauthorized to access this data'
            }), 401)

    @app.errorhandler(403)
    def not_authorized(error):
        logging.exception(error)
        if "message" in error.description:
            return make_response(jsonify({
                "error": "403", "message": error.description["message"]
            }), 403)
        else:
            return make_response(jsonify({
                'error': '403', 'message': 'Unauthorized - You\'re not authorized to access this data'
            }), 403)

    @app.errorhandler(404)
    def page_not_found(error):
        logging.exception(error)
        return make_response(jsonify({
            'error': '404', 'message': 'Not Found - The requested resource could not be found'
        }), 404)

    @app.errorhandler(405)
    def not_authorized(error):
        logging.exception(error)
        return make_response(jsonify({
            'error': '405', 'message': 'Method Not Allowed - That method is not allowed'
        }), 405)

    @app.errorhandler(409)
    def not_authorized(error):
        logging.exception(error)
        return make_response(jsonify({
            'error': '409', 'message': 'The request could not be completed due to a conflict with the current state ' +
            'of the resource.'
        }), 409)

    @app.errorhandler(500)
    def internal_error(error):
        logging.exception(error)
        return make_response(jsonify({
            'error': '500', 'message': 'Internal Server Error - Something went wrong on our end while attempting to ' +
            'process your request'
        }), 500)

    @app.errorhandler(502)
    def service_unavailable(error):
        logging.exception(error)
        return make_response(jsonify({
            'error': '502', 'message': 'Service Unavailable - Server is currently unable to handle the request due ' +
            'to maintenance or overload of the server'
        }), 502)

    @app.errorhandler(503)
    def service_unavailable(error):
        logging.exception(error)
        return make_response(jsonify({
            'error': '503', 'message': 'Service Unavailable - Server is currently unable to handle the request due ' +
            'to maintenance or overload of the server'
        }), 503)

    return app