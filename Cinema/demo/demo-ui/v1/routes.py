# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.Cinema import Cinema
from .api.Cinema_cinema_name import CinemaCinemaName


routes = [
    dict(resource=Cinema, urls=['/Cinema'], endpoint='Cinema'),
    dict(resource=CinemaCinemaName, urls=['/Cinema/<cinema_name>'], endpoint='Cinema_cinema_name'),
]