from app.salary.typehints import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from app.salary.core.exceptions import (
    HttpResponseErrorCode,
    UserLogicException,
    HttpRedirectException,
)
from app.base import utils
from app.salary.core.auth.manager import AuthManager
from app.salary.core.auth.policy import SimpleAuthPolicy, AclAuthorizationPolicy


class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        auth_manager = AuthManager(
            request, SimpleAuthPolicy(), AclAuthorizationPolicy()
        )

        request.auth_manager = auth_manager

        if auth_manager.user is not None:
            if auth_manager.user.invalidate != 0:
                auth_manager.logout()
                self.process_exception(
                    request,
                    UserLogicException(
                        "Session expired. Please log in again.",
                        route_name="sl_u:Auth.Login",
                    ),
                )

        return self.get_response(request)

    def process_exception(self, request: HttpRequest, exp: Exception):

        if isinstance(exp, HttpRedirectException):
            return redirect(exp.url, permanent=exp.permanent)

        if isinstance(exp, HttpResponseErrorCode):
            return render(
                request,
                "bs/errors/generic.html",
                {"code": exp.code, "msg": exp.msg},
                status=exp.code,
            )

        elif isinstance(exp, UserLogicException):
            if exp.route_name == None:
                response = utils.redirect_back(request)
            else:
                response = redirect(
                    reverse(exp.route_name, args=exp.route_args) + exp.query_params
                )

            messages.error(request, exp.user_msg)
            return response

        return None