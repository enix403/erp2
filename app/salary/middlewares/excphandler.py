from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from app.salary.core.exceptions import (
    HttpResponseErrorCode,
    UserLogicException
)
from app.base import utils

class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, req):
        return self.get_response(req)

    def process_exception(self, request : HttpRequest, exp: Exception):
        if isinstance(exp, HttpResponseErrorCode):
            return render(request, 'bs/errors/generic.html', {
                "code": exp.code,
                "msg": exp.msg
            })
        
        elif isinstance(exp, UserLogicException):
            if exp.route_name == None:
                response = utils.redirect_back(request)
            else:
                response = redirect(reverse(exp.route_name, args=exp.route_args) + exp.query_params)

            messages.error(request, exp.user_msg)
            return response
        
        
        return None
        
