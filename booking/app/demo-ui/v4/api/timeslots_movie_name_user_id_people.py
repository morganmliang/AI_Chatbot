# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas

import json
import copy
import sqlite3 as sql

#DATABASE =  'C:\\Users\morga\OneDrive\Desktop\COMP9322\Assignment2\booking\database.db'
DATABASE = "/service/database.db"


class TimeslotsMovieNameUserIdPeople(Resource):
    #Return all timeslots that are available to the user
    def get(self, movie_name, user_id, people):
        print("hello")
        timeslots = []
        #print("hello")

        ticket_tab = query_db('SELECT * FROM tickets WHERE holderID=?', [str(user_id)]) 
        booked_ids = [i['timeslot_id'] for i in ticket_tab]

        slots = query_db('SELECT * FROM timeslots WHERE m_name=?', [movie_name])


        # userList = [ticket['holderID'] for ticket in ticket_tab]
        # if(user_id in userList):
        #     return {'message': "You have booked a ticket already for this timeslot" }, 404, None

        for slot in slots:

            #Check if capacity is available
            if (people >= slot['max_seats'] or slot['avail_seats'] < people):
                continue
        
            #Check if timeslot is already booked
            if(slot['timeslot_id'] in booked_ids):
                continue
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


        # print(timeslots)



        return timeslots,200, None
        #return {timeslots}, 200, None

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
