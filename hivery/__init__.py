from flask import Flask, url_for
from hivery.models import db, init_db
from hivery.api import api


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['RESTPLUS_MASK_SWAGGER'] = False
    app.config['ERROR_404_HELP'] = False

    db.init_app(app)
    app.cli.add_command(init_db)

    api.init_app(app)

    @app.route("/")
    @app.route("/status")
    def _status():
        return "Yes, it's working"

    return app
