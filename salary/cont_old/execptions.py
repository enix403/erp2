# import base.helpers as helpers
# from django.shortcuts import reverse, redirect

class DisplayToUserException(Exception):
    def __init__(self, user_msg="An error occured", route_name=None, route_args=[], query_params=''):
        self.user_msg = user_msg
        self.route_name = route_name
        self.route_args = route_args
        self.query_params = query_params
        

# def catch_user_error(func):
#     def _decorated(*args, **kwargs):
#         try:
#             res = func(*args, **kwargs)
#             return res
#         except DisplayToUserException as e:
#             req = args[1]
#             if e.route_name == None:
#                 res = helpers.redirect_back(req)
#             else:
#                 res = redirect(reverse(e.route_name, args=e.route_args))
            
#             return helpers.response_error(e.user_msg, req, res)
                
            

#     return _decorated
