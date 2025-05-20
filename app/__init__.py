from flask import Flask
import logging
import os
from datetime import timedelta


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Load config
    app.config.from_object('config.Config')

    if test_config:
        app.config.update(test_config)

    # Ensure temp folder exists
    os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, app.config['LOG_LEVEL']),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Set session lifetime
    app.permanent_session_lifetime = timedelta(hours=8)

    # Register blueprints
    from .routes import bp
    app.register_blueprint(bp)

    return app

