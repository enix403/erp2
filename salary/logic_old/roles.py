from collections import namedtuple

ROLE_FACULTY = 1
ROLE_PRINCIPLE = 2
ROLE_VICE_PRINCIPLE = 3
ROLE_INFO_OFFICER = 4
ROLE_ACCOUNTANT = 5
ROLE_AE_CONTROLLER = 6
ROLE_CONSELLER = 7

ROLE_ADMIN_MANAGER = 8
ROLE_ASSISTANT_ACC = 9
ROLE_LIBRARIAN = 10
ROLE_SECURITY_GUARD = 11
ROLE_SWEEPER = 12
ROLE_OFFICE_BOY = 13
ROLE_ELECTRICIAN = 14
ROLE_EXAM_CTLR = 15
ROLE_ACADEMIC_COORD = 16
ROLE_DATA_OP = 17

RoleInfo = namedtuple("RoleInfo", ['name', 'role', 'duplicate'])

__all_roles = [
    RoleInfo("Faculty", ROLE_FACULTY, True),
    RoleInfo("Principal", ROLE_PRINCIPLE, False),
    RoleInfo("Vice Principle", ROLE_VICE_PRINCIPLE, True),
    RoleInfo("Info Officer", ROLE_INFO_OFFICER, True),
    
    RoleInfo("Assistant Examination Controller", ROLE_AE_CONTROLLER, True),
    RoleInfo("Accountant", ROLE_ACCOUNTANT, True),
    RoleInfo("Student Counseller", ROLE_CONSELLER, True),
    RoleInfo("Assistant Accountant", ROLE_ASSISTANT_ACC, True),
    RoleInfo("Admin Manager", ROLE_ADMIN_MANAGER, True),
    RoleInfo("Librarian", ROLE_LIBRARIAN, True),
    RoleInfo("Security Gaurd", ROLE_SECURITY_GUARD, True),
    RoleInfo("Sweeper", ROLE_SWEEPER, True),
    RoleInfo("Office Boy", ROLE_OFFICE_BOY, True),
    RoleInfo("Electrician", ROLE_ELECTRICIAN, True),
    RoleInfo("Examination Controller", ROLE_EXAM_CTLR, True),
    RoleInfo("Academic Coordinator", ROLE_ACADEMIC_COORD, True),
    RoleInfo("Data Entry Operator", ROLE_DATA_OP, True),

    
]


    
def is_role_valid(role):
    # return role >= 1 and role <= 7
    return True


def all_roles():
    return __all_roles

def role_from_id(role) -> RoleInfo:
    role_info_list = list(filter(lambda role_info: role_info.role == role, __all_roles))
    if len(role_info_list) > 0:
        return role_info_list[0]
    
    return None
