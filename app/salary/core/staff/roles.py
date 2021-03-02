from collections import namedtuple

ROLE_FACULTY = 1
ROLE_PRINCIPLE = 2
ROLE_CONSELLER = 7

RoleInfo = namedtuple("RoleInfo", ['name', 'role', 'duplicate'])

_all_roles = [
    RoleInfo("Faculty", ROLE_FACULTY, True),
    RoleInfo("Principal", ROLE_PRINCIPLE, False),
    RoleInfo("Vice Principle", 3, True),
    RoleInfo("Info Officer", 4, True),
    RoleInfo("Assistant Examination Controller", 6, True),
    RoleInfo("Accountant", 5, True),
    RoleInfo("Student Counseller", ROLE_CONSELLER, True),
    RoleInfo("Assistant Accountant", 9, True),
    RoleInfo("Admin Manager", 8, True),
    RoleInfo("Librarian", 10, True),
    RoleInfo("Security Gaurd", 11, True),
    RoleInfo("Sweeper", 12, True),
    RoleInfo("Office Boy", 13, True),
    RoleInfo("Electrician", 14, True),
    RoleInfo("Examination Controller", 15, True),
    RoleInfo("Academic Coordinator", 16, True),
    RoleInfo("Data Entry Operator", 17, True),
]


def is_role_valid(role):
    return role >= 1 and role <= 17


def all_roles():
    return _all_roles


def roleinfo(role_id) -> RoleInfo:
    for role_info in _all_roles:
        if role_info.role == role_id:
            return role_info
    
    return None