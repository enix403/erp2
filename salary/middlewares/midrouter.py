from .internals import RouteGroup
from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from .schema import route_schema

import base.helpers as helpers

from ..auth.manager import AuthManager
from ..auth.execptions import UnauthorizedCollegeAccess
from ..controllers.execptions import DisplayToUserException

noop = lambda *args, **kwargs: None

class RouterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.schema: RouteGroup  = route_schema
        self.schema.process_middleware()
        self.handler_cache = {}

    def __call__(self, req):
        
        
        return self.get_response(req)

    def process_view(self, request: HttpRequest, view_func, view_args, view_kwargs):
        AuthManager.fill_from_session(request)
        
        # print(request.session.items())
        
        name = request.resolver_match.url_name
        if name in self.handler_cache:
            reduced = self.handler_cache.get(name)
        else:
            reduced = self.schema.get_handler(name, noop)
            self.handler_cache[name] = reduced

        if reduced is None:
            return None
    
        # return reduced(request)
        
        try:
            return reduced(request)
        except Exception as e:
            res = self.process_exception(request, e)
            if res is not None:
                return res
            
            raise
        
    
    def process_exception(self, request : HttpRequest, exp: Exception):
        if isinstance(exp, UnauthorizedCollegeAccess):
            return render(request, 'sl/errors/generic.html', {
                "code": 401,
                "msg": "Unauthorized"
            })
        
        elif isinstance(exp, DisplayToUserException):
            if exp.route_name == None:
                response = helpers.redirect_back(request)
            else:
                response = redirect(reverse(exp.route_name, args=exp.route_args) + exp.query_params)

            return helpers.response_error(exp.user_msg, request, response)
        
        
        return None
        
