# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g
from .wit import wit
from . import Resource
from .. import schemas




class Chatmessage(Resource):

    def get(self):
        print(g.args)

        answer = wit(g.args['userMessage'],g.args['userName'])

        return {'answer': answer}, 200, None