from collections import namedtuple

STATUS_UNSPEC = 0
STATUS_PRESENT = 1
STATUS_ABSENT = 2

LeaveInfo = namedtuple('LeaveInfo', ['id', 'name'])

__all_leaves = [
    LeaveInfo(STATUS_UNSPEC, 'Not Yet Specified'),
    LeaveInfo(STATUS_PRESENT, 'Present'),
    LeaveInfo(STATUS_ABSENT, 'Absent'),
]

def get_all_leaves():
    return __all_leaves

def is_leave_valid(leave):
    return True
    # return leave >= 0 and leave <= 2


def leave_from_id(leave_id) -> LeaveInfo:
    if leave_id == None:
        return __all_leaves[0] # LEAVE_UNSPEC

    leave_info_list = list(filter(lambda leave_info: leave_info.id == leave_id, __all_leaves))
    if len(leave_info_list) > 0:
        return leave_info_list[0]

    return __all_leaves[0]
