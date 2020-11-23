from django.http import  HttpRequest, QueryDict
from django.contrib import messages
from django.shortcuts import redirect
from django.db import models

def get_bag(req: HttpRequest, method = None) -> QueryDict:
    if method == None:
        method = req.method.upper()
    
    if method == 'POST':
        return req.POST
    elif method == 'GET':
        return req.GET
    
    return req.GET


def fetch_model_clean(model_class: models.Model, pk):
    if not pk or pk == '0':
        return None
        
    try:
        model = model_class.objects.get(pk=pk)
        return model
    except model_class.DoesNotExist:
        return None

class LazyEval:
    def __init__(self, func, *args, **kwargs):
        self.val = None
        self.done = False
        self.func = func
        
        self.f_args = args
        self.f_kwargs = kwargs
        
    def get(self):
        if self.done == False:
            self.val = self.func(*self.f_args, **self.f_kwargs)
            self.done = True
            
        return self.val
    
def response_success(msg, req, res):
    messages.success(req, msg)
    return res


def response_error(msg, req, res):
    messages.error(req, msg)
    return res


def optional(val, default=None):
    if val == None or val == '':
        return default
    
    return val

def get_prev_url(req, default_url="/"):
    return optional(req.session.get('flash___prev_url'), default_url)


def redirect_back(req: HttpRequest, default_url='/'):
    # return redirect(get_prev_url(req, default_url))
    return redirect(req.META.get('HTTP_REFERER', default_url))
    

def to_int(num, default = 0) -> int:
    if num is None:
        return default
    try:
        return int(num)
    except:
        return default

def get_col(model: models.Model, field: str):
    try:
        field_obj = model._meta.get_field(field)
        return field_obj.db_column
    except:
        return None
    
def get_first(lst: list):
    if lst:
        return lst[0]