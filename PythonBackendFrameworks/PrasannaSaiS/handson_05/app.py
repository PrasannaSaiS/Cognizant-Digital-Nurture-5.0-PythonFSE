from flask import Flask
from flask_migrate import Migrate
from config import Config
from courses.models import db
from courses.routes import courses_bp, make_response_json


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    Migrate(app, db)
    app.register_blueprint(courses_bp)

    @app.errorhandler(404)
    def not_found(error):
        return make_response_json({'error': 'Resource not found'}, 404)

    @app.errorhandler(500)
    def server_error(error):
        return make_response_json({'error': 'Internal server error'}, 500)

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
