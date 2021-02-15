class IAuthenticationPolicy:
    def unauthenticated_userid(self, request):
        """Returns the unauthenticated userid provided by the user"""

    def authenticated_user(self, request):
        """Returns the authenticated userid provided by the user"""


    def effective_principals(self, user):
        """Returns the effective principals associated with the user"""


    def remember(self, request, userid):
        pass

    def forget(self, request):
        pass
    

class IAuthorizationPolicy:
    def permits(self, context, principals, permission):
        pass