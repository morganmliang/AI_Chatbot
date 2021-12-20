# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import json
import copy
import sqlite3 as sql

#DATABASE =  'C:\\Users\morga\OneDrive\Desktop\COMP9322\Assignment2\newBooking\database.db'
DATABASE = "/service/database.db"

class Movie(Resource):

    def get(self):

        tab = query_db('SELECT * FROM movies')

        movie_list = []

        for movie in tab:
            m_dict= {}
            m_dict['m_id'] = movie['m_id']
            m_dict['m_name'] = movie['m_name']
            m_dict['description'] = movie['description']
            movie_list.append(m_dict)

        print(movie_list)
        return movie_list,200, None
        #return {}, 200, None

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_db():
    db =  sql.connect(DATABASE)
    db.row_factory = sql.Row
    return db
