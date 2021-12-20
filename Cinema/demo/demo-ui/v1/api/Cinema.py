# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import json
import copy
import sqlite3 as sql

#DATABASE =  'C:\\Users\morga\OneDrive\Desktop\COMP9322\Assignment2\Cinema\database.db'
DATABASE = "/service/database.db"

class Cinema(Resource):

    def get(self):
        ans = []
        tab = query_db('SELECT * FROM cinemas')

        for cinema in tab:
            c_dict = {}
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
            ans.append(c_dict)
        print(ans)

        return ans, 200, None


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_db():
    db =  sql.connect(DATABASE)
    db.row_factory = sql.Row
    return db
