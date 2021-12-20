# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.timeslots import Timeslots
from .api.timeslots_timeslot_id import TimeslotsTimeslotId
from .api.timeslots_user_id_booked_tickets import TimeslotsUserIdBookedTickets
from .api.timeslots_user_id_timeslot_id_delete import TimeslotsUserIdTimeslotIdDelete
from .api.timeslots_timeslot_id_user_id_people_add import TimeslotsTimeslotIdUserIdPeopleAdd
from .api.timeslots_movie_name_user_id_people import TimeslotsMovieNameUserIdPeople
from .api.movie import Movie
from .api.movie_movie_name import MovieMovieName


routes = [
    dict(resource=Timeslots, urls=['/timeslots'], endpoint='timeslots'),
    dict(resource=TimeslotsTimeslotId, urls=['/timeslots/<int:timeslot_id>'], endpoint='timeslots_timeslot_id'),
    dict(resource=TimeslotsUserIdBookedTickets, urls=['/timeslots/<int:user_id>/booked_tickets'], endpoint='timeslots_user_id_booked_tickets'),
    dict(resource=TimeslotsUserIdTimeslotIdDelete, urls=['/timeslots/<int:user_id>/<int:timeslot_id>/delete'], endpoint='timeslots_user_id_timeslot_id_delete'),
    dict(resource=TimeslotsTimeslotIdUserIdPeopleAdd, urls=['/timeslots/<int:timeslot_id>/<int:user_id>/<int:people>/add'], endpoint='timeslots_timeslot_id_user_id_people_add'),
    dict(resource=TimeslotsMovieNameUserIdPeople, urls=['/timeslots/<movie_name>/<int:user_id>/<int:people>'], endpoint='timeslots_movie_name_user_id_people'),
    dict(resource=Movie, urls=['/movie'], endpoint='movie'),
    dict(resource=MovieMovieName, urls=['/movie/<movie_name>'], endpoint='movie_movie_name'),
]