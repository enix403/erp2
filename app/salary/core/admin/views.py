from __future__ import annotations
from django.views import View
from django.shortcuts import render
from app.salary.typehints import HttpRequest
from django.contrib import messages

from app.base import utils
from app.salary.models import Station, College
from app.salary.core.college import college_validate_simple
from app.salary.core.exceptions import UserLogicException

from . import _actions
from .permissions import ManagePermissions


class IndexManageView(View):
    def get(self, req: HttpRequest):

        req.auth_manager.require_perm(
            ManagePermissions, "station:read", "clg:read"
        )

        return render(
            req,
            "sl/manage.html",
            {"stations": Station.objects.all().prefetch_related("colleges")},
        )


class Action_CreateStation(View):
    def _transform_input(self, req, bag):
        req.auth_manager.require_perm(ManagePermissions, "station:create")

        name = bag.get("name", None)
        if not name:
            raise UserLogicException("Invalid name")

        if Station.objects.filter(name=name).exists():
            raise UserLogicException(f"Station {name} already exists")

        return name

    def post(self, req: HttpRequest):
        bag = utils.get_bag(req)
        name = self._transform_input(req, bag)

        _actions.make_station(name)
        messages.success(req, "Station added successfully")

        return utils.redirect_back(req)


class Action_CreateCollege(View):
    def _transform_input(self, req, bag):
        req.auth_manager.require_perm(ManagePermissions, "clg:create")

        name = bag.get("name", None)
        if name == "":
            raise UserLogicException("Invalid name")

        station = Station.objects.filter(pk=utils.to_int(bag.get("station_id"))).first()
        if station is None:
            raise UserLogicException("Given station not found")

        if College.objects.filter(name=name).exists():
            raise UserLogicException(f"College {name} already exists")

        return name, station

    def post(self, req):
        bag = utils.get_bag(req)
        name, station = self._transform_input(req, bag)
        _actions.make_college(name, station.pk)
        messages.success(req, "College added successfully")

        return utils.redirect_back(req)

        