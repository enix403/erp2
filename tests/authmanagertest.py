#!/usr/bin/env python
from app.salary.core.auth.manager import AuthManager
from app.salary.core.auth.policy import SimpleAuthPolicy, AclAuthorizationPolicy

auth_manager = AuthManager(
    None, SimpleAuthPolicy(), AclAuthorizationPolicy()
)

# still working on it :)