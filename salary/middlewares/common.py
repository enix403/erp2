# def flasher(get_response):
#     def __middleware(req):
#         response = get_response(req)
#         req.session['flash__prev_url']

class FlashMiddleware(object):
    
    flash_key_prefix = 'flash___'
    
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        for key, _ in list(request.session.items()): # type: str, str
            if key.startswith(self.flash_key_prefix):
                del request.session[key]
            

        # Code to be executed for each request/response after
        # the view is called.

        # TODO: flash last http method too
        request.session[self.flash_key_prefix + 'prev_url'] = request.path + "?" + request.GET.urlencode()
        
        # print(list(request.session.items()))

        return response
