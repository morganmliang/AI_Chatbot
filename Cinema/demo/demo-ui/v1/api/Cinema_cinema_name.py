# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

import sqlite3 as sql

from . import Resource
from .. import schemas
import json
import copy

DATABASE =  "/service/database.db"

class CinemaCinemaName(Resource):

    def get(self, cinema_name):

        tab = query_db("SELECT * FROM cinemas WHERE name=?", [cinema_name])
        c_dict = {}
        for cinema in tab:
            c_dict["c_id"] = cinema['c_id']
            c_dict["name"] = cinema['name']
            c_dict["address"] = cinema['address']
            c_dict["phone"] = cinema['phone']
            c_dict["snacks"] = []
            snacks = query_db("SELECT * FROM snacks WHERE c_id = ?", str(cinema['c_id']))
            for s in snacks:
                c_dict["snacks"].append(s['s_name'])
            c_dict["movies"] = []
            movies = query_db("SELECT * FROM movies WHERE c_id = ?", str(cinema['c_id']))
            for m in movies:
                m_dict = {}
                m_dict['m_id'] = m['m_id']
                m_dict['name'] = m['m_name']
                m_dict['description'] = m['description']
                c_dict["movies"].append(m_dict)

        if(len(c_dict)==0):
            print("is is a error")
            return None, 404, None

        return c_dict, 200, None



def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_db():
    db =  sql.connect(DATABASE)
    db.row_factory = sql.Row
    return db
