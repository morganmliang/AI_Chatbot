# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from os import read

from flask import request, g
import json

from . import Resource
from .. import schemas


class Cinema(Resource):

    def get(self):
        cinemas = read_from_file()
        r= []
        results = {}
        for c in cinemas:
            c_dict={}
            c_dict['c_id'] = c
            c_dict['name'] = cinemas[c]['name']
            c_dict['address'] = cinemas[c]['address']
            c_dict['phone'] = cinemas[c]['phone']
            c_dict['snacks'] = cinemas[c]['snacks']
            c_dict['movies'] = cinemas[c]['movies']
            r.append(c_dict)
        results["result"] = r
        return results, 200, None


def write_to_file(content):
    with open("./cinemas.json", "w") as cinemas:
        cinemas.write(json.dumps(content))


def read_from_file():
    with open("./cinemas.json", "r") as cinemas:
        return json.loads(cinemas.read())