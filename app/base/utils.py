from django.http import  HttpRequest, QueryDict
from django.shortcuts import redirect

def get_bag(req: HttpRequest, method = None) -> QueryDict:
    if method == None:
        method = req.method.upper()
    
    if method == 'POST':
        return req.POST
    elif method == 'GET':
        return req.GET
    
    return req.GET


# def optional(val, default=None):
    # if val == None or val == '':
        # return default
    
    # return val

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

# def get_col(model: models.Model, field: str):
    # try:
        # field_obj = model._meta.get_field(field)
        # return field_obj.db_column
    # except:
        # return None
    
def get_first(lst: list):
    if lst:
        return lst[0]