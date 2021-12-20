# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask

import v4


def create_app():
    app = Flask(__name__, static_folder='static')
    app.register_blueprint(
        v4.bp,
        url_prefix='/v4')
    return app

if __name__ == '__main__':
    create_app().run(debug=True, host="0.0.0.0")