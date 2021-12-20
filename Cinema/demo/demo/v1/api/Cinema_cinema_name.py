# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import json


class CinemaCinemaName(Resource):

    def get(self, cinema_name):

        cinemas = read_from_file()

        l = []
        val = {}
        print("hello")
        print(cinemas)
        for c in cinemas:
            print(c)
            if(cinemas[c]['name'] == cinema_name):
                result = {}
                result['c_id'] = c
                result["name"] = cinemas[c]['name']
                result["address"] = cinemas[c]['address']
                result["phone"] = cinemas[c]['phone']
                result["snacks"] = cinemas[c]['snacks']
                result['movies'] = cinemas[c]['movies']
                l.append(result)
        
        if(len(l)==0):
            return None, 404, None

        val['result'] = l

        return val, 200, None



def write_to_file(content):
    with open("./cinemas.json", "w") as cinemas:
        cinemas.write(json.dumps(content))


def read_from_file():
    with open("./cinemas.json", "r") as cinemas:
        return json.loads(cinemas.read())