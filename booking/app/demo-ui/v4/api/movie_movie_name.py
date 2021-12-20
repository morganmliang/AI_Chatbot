# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
import json
import copy
import sqlite3 as sql

DATABASE = "/service/database.db"

class MovieMovieName(Resource):

    def get(self, movie_name):
        timeslots = []
        slot_list = query_db('SELECT * FROM timeslots WHERE m_name=?', [movie_name])

        for slot in slot_list:
            t_dict= {}
            t_dict['timeslot_id'] = slot['timeslot_id']
            t_dict['m_id'] = slot['m_id']
            t_dict['cinema_name'] = slot['cinema_name']
            t_dict['theatre_type'] = slot['theatre_type']
            t_dict['start_time'] = slot['start_time']

            t_dict['end_time'] = slot['end_time']
            t_dict['day'] = slot['day']
            t_dict['max_seats'] = slot['max_seats']
            t_dict['avail_seats'] = slot['avail_seats']
            t_dict['movie_name'] = slot['m_name']
            timeslots.append(t_dict)
            



        return timeslots,200, None

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_db():
    db =  sql.connect(DATABASE)
    db.row_factory = sql.Row
    return db
