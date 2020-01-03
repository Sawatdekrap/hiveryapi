from flask import Flask
from hivery.models import db, init_db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.cli.add_command(init_db)

    @app.route("/")
    @app.route("/status")
    def _status():
        return "Yes, it's working"

    return app
