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


class TimeslotsTimeslotIdUserIdPeopleAdd(Resource):

    def put(self, timeslot_id, user_id, people):
        print(timeslot_id)
        print(user_id)
        print(people)
        new_tid = query_db('SELECT MAX(ticketid) FROM tickets')
        print(new_tid)


        new_ticketid = new_tid[0][0] + 1



        newticket = (str(user_id),str(new_ticketid), str(timeslot_id), "n/a" , str(people))
        insert_db('INSERT INTO tickets(holderID,ticketid,timeslot_id,holderName,people) VALUES(?,?,?,?,?)', newticket)

        update_db('UPDATE timeslots SET avail_seats=avail_seats-? WHERE timeslot_id=?', (str(people), str(timeslot_id)))

        updated_slot = query_db('SELECT * from timeslots WHERE timeslot_id=?', (str(timeslot_id),))

        t_dict= {}
        t_dict['timeslot_id'] = updated_slot[0]['timeslot_id']
        t_dict['m_id'] = updated_slot[0]['m_id']
        t_dict['cinema_name'] = updated_slot[0]['cinema_name']
        t_dict['theatre_type'] = updated_slot[0]['theatre_type']
        t_dict['start_time'] = updated_slot[0]['start_time']

        t_dict['end_time'] = updated_slot[0]['end_time']
        t_dict['day'] = updated_slot[0]['day']
        t_dict['max_seats'] = updated_slot[0]['max_seats']
        t_dict['avail_seats'] = updated_slot[0]['avail_seats']
        t_dict['movie_name'] = updated_slot[0]['m_name']
        

        return t_dict, 200, None

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=(), one=False):
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