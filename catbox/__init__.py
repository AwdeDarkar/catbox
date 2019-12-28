"""
init
====================================================================================================

Setup script for catbox app

----------------------------------------------------------------------------------------------------

**Created**
    2019-12-27
**Updated**
    2019-12-27 by Darkar
**Author**
    Darkar
**Copyright**
    This software is Free and Open Source for any purpose
"""

import os
import logging

from flask import Flask, render_template

from . import server


def init_logger():
    log_formatter = logging.Formatter(
            "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
            )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)


def create_app(test_config=None):
    """ Create and configure the app """
    init_logger()
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    game_server = server.Server(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    def landing():
        return render_template("page.html")
    
    game_server.socketio.run(app, debug=True)

    return app
