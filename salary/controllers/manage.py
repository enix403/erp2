from django.http import HttpRequest
from django.shortcuts import render
from django.contrib import messages
from django.views import View

from ..models import (
    Station,
    College
)

from ..logic import admin as l_admin
from ..logic import college as l_college
# from ..logic import exceptions as excp

from base import helpers
from .execptions import DisplayToUserException

from ..auth.validation import (
    validate_write
)

def index(req):
    return render(req, "sl/pages/manage.html", {
        "stations": Station.objects.all().prefetch_related('colleges'),
    })


# ************************** NEW COLLEGE **************************
class Action_CreateCollege(View):
    def _transform_input(self, bag):
        
        validate_write('colleges')
        
        name = bag.get('name', None)
        if name == '':
            raise DisplayToUserException("Invalid name")

        station = helpers.fetch_model_clean(Station, bag.get('station_id', 0))
        if station == None:
            raise DisplayToUserException("Given station not found")

        if College.objects.filter(name=name).exists():
            raise DisplayToUserException("College " + str(name) + " already exists")

        return name, station

    def post(self, req):
        bag = helpers.get_bag(req)
        name, station = self._transform_input(bag)
        l_college.Impl_College.make_college(name, station)
        messages.success(req, "College added successfully")

        return helpers.redirect_back(req)


# ************************** NEW STATION **************************
class Action_CreateStation(View):
    def _transform_input(self, req, bag):
        validate_write('stations')
        
        name = bag.get('name', None)
        if not name:
            raise DisplayToUserException("Invalid name")

        if Station.objects.filter(name=name).exists():
            raise DisplayToUserException("Station " + str(name) + " already exists")

        return name

    def post(self, req: HttpRequest):
        bag = helpers.get_bag(req)
        name = self._transform_input(req, bag)

        l_admin.make_station(name)
        messages.success(req, "Station added successfully")

        return helpers.redirect_back(req)
