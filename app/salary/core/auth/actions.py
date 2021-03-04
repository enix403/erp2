from app.salary.core.exceptions import HttpUnauthorized, HttpRedirectException
from app.salary.typehints import HttpRequest

Allow = 1
Deny = 2


def handle_unauthorized(req: HttpRequest, msg='Not Authorized'):
    if req.auth_manager.user is not None:
        # User is logged in but does not have enough permissons.
        # Show an "Unauthorized page"
        raise HttpUnauthorized(msg)

    else:
        # User is not logged in.
        # Redirect the user to the login page.

        raise HttpRedirectException('sl_u:Auth.Login')
