from flask import Flask, url_for
from hivery.config import config_by_name
from hivery.models import db, db_init
from hivery.api import blueprint as api_bp
import os


def create_app():
    app = Flask(__name__)
    flask_env = os.environ.get('FLASK_ENV', 'production')
    app.config.from_object(config_by_name[flask_env])

    db.init_app(app)
    app.cli.add_command(db_init)

    app.register_blueprint(api_bp)

    # Route root calls to status page to show that it's live
    @app.route("/")
    @app.route("/status")
    def _status():
        return "Hivery api is running"

    return app
