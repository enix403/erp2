Everyone = 'sys.Everyone'
Authenticated = 'sys.Authenticated'

def PR_UserId(userid):
    return f'UserId({userid})'

def PR_AuthRole(role):
    return f'AuthRole({role})'

def PR_StaffRole(role):
    return f'StaffRole({role})'

def PR_ClgAccess(college_id):
    return f'ClgAccess({college_id})'
