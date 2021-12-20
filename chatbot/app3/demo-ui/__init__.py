# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask
from flask_cors import CORS
import v3


def create_app():
    app = Flask(__name__, static_folder='static')
    
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.register_blueprint(
        v3.bp,
        url_prefix='/v3')
    return app

if __name__ == '__main__':
    create_app().run(debug=True)