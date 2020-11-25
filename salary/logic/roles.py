from collections import namedtuple

ROLE_FACULTY = 1
ROLE_PRINCIPLE = 2
# ROLE_VICE_PRINCIPLE = 3
# ROLE_INFO_OFFICER = 4
# ROLE_ACCOUNTANT = 5
# ROLE_AE_CONTROLLER = 6
ROLE_CONSELLER = 7

# ROLE_ADMIN_MANAGER = 8
# ROLE_ASSISTANT_ACC = 9
# ROLE_LIBRARIAN = 10
# ROLE_SECURITY_GUARD = 11
# ROLE_SWEEPER = 12
# ROLE_OFFICE_BOY = 13
# ROLE_ELECTRICIAN = 14
# ROLE_EXAM_CTLR = 15
# ROLE_ACADEMIC_COORD = 16
# ROLE_DATA_OP = 17

RoleInfo = namedtuple("RoleInfo", ['name', 'role', 'duplicate', 'groups'])

__all_roles = [
    RoleInfo("Faculty", ROLE_FACULTY, True, []),
    RoleInfo("Principal", ROLE_PRINCIPLE, False, ['grp_principal']),
    RoleInfo("Vice Principle", 3, True, []),
    RoleInfo("Info Officer", 4, True, []),
    RoleInfo("Assistant Examination Controller", 6, True, []),
    RoleInfo("Accountant", 5, True, []),
    RoleInfo("Student Counseller", ROLE_CONSELLER, True, []),
    RoleInfo("Assistant Accountant", 9, True, []),
    RoleInfo("Admin Manager", 8, True, []),
    RoleInfo("Librarian", 10, True, []),
    RoleInfo("Security Gaurd", 11, True, []),
    RoleInfo("Sweeper", 12, True, []),
    RoleInfo("Office Boy", 13, True, []),
    RoleInfo("Electrician", 14, True, []),
    RoleInfo("Examination Controller", 15, True, []),
    RoleInfo("Academic Coordinator", 16, True, []),
    RoleInfo("Data Entry Operator", 17, True, []),
    
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
