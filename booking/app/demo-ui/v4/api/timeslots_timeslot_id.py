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

class TimeslotsTimeslotId(Resource):

    def get(self, timeslot_id):

        table = query_db('SELECT * FROM timeslots WHERE timeslot_id=?', (str(timeslot_id),))

        if(len(table) != 1):
            print("is is a error")
            return None, 404, None
        slot = table[0]

        #for slot in tab:
        get_timeslot= {}
        get_timeslot['timeslot_id'] = slot['timeslot_id']
        get_timeslot['m_id'] = slot['m_id']
        get_timeslot['cinema_name'] = slot['cinema_name']
        get_timeslot['theatre_type'] = slot['theatre_type']
        get_timeslot['start_time'] = slot['start_time']
        get_timeslot['end_time'] = slot['end_time']
        get_timeslot['day'] = slot['day']
        get_timeslot['max_seats'] = slot['max_seats']
        get_timeslot['avail_seats'] = slot['avail_seats']
        get_timeslot['movie_name'] = slot['m_name']

        return get_timeslot,200, None


        


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_db():
    db =  sql.connect(DATABASE)
    db.row_factory = sql.Row
    return db
