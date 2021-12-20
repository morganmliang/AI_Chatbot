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


class TimeslotsUserIdTimeslotIdDelete(Resource):

    def put(self, user_id, timeslot_id):
        print(user_id)
        print(timeslot_id)




        people = query_people_db('SELECT people FROM tickets WHERE timeslot_id=? AND holderID=?',(str(timeslot_id), str(user_id)))

        print(people)
        delete_db('DELETE FROM tickets WHERE timeslot_id=? AND holderID=?',(str(timeslot_id), str(user_id)))


        update_db('UPDATE timeslots SET avail_seats = avail_seats + ? WHERE timeslot_id=?',(str(people), str(timeslot_id)))
        
        updated_slot = query_db('SELECT * from timeslots WHERE timeslot_id=?', (str(timeslot_id),))
        slot = updated_slot[0]


    
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

        return t_dict, 200, None 



def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def query_people_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchone()
    cur.close()
    return (rv[0] if rv else None) 

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
