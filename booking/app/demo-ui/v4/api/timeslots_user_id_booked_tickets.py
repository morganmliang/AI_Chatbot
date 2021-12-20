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

class TimeslotsUserIdBookedTickets(Resource):

    def get(self, user_id):

        ticket_tab = query_db('SELECT * FROM tickets WHERE holderID=?', [str(user_id)]) 
        booked_list = []
        t_ids = [str(t_slot['timeslot_id']) for t_slot in ticket_tab]
        for slot_id in t_ids:
            slot = query_db('SELECT * FROM timeslots WHERE timeslot_id=?', [slot_id])
            print(slot)

            get_timeslot= {}
            get_timeslot['timeslot_id'] = slot[0]['timeslot_id']
            get_timeslot['m_id'] = slot[0]['m_id']
            get_timeslot['cinema_name'] = slot[0]['cinema_name']
            get_timeslot['theatre_type'] = slot[0]['theatre_type']
            get_timeslot['start_time'] = slot[0]['start_time']
            get_timeslot['end_time'] = slot[0]['end_time']
            get_timeslot['day'] = slot[0]['day']
            get_timeslot['max_seats'] = slot[0]['max_seats']
            get_timeslot['avail_seats'] = slot[0]['avail_seats']
            get_timeslot['movie_name'] = slot[0]['m_name']
            booked_list.append(get_timeslot)

        return booked_list,200, None
        


        #return {'timeslot_id': 9573, 'cinema_name': 'something', 'theatre_type': 'Saver', 'start_time': 'something', 'end_time': 'something', 'day': 'something', 'max_seats': 9573, 'avail_seats': 9573, 'movie_name': 'something'}, 200, None


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def query_people_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchone()
    cur.close()
    return (rv if rv else None) 

def insert_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()

def delete_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()

def update_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()


def get_db():
    db =  sql.connect(DATABASE)
    db.row_factory = sql.Row
    return db
