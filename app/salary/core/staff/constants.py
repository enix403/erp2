class Gender:
    MALE = 0
    FEMALE = 1


class FacultyCategory:
    FAC_CATERGORY_M = 0
    FAC_CATERGORY_M_AND_E = 1
    FAC_CATERGORY_M_PLUS_E = 2
    FAC_CATERGORY_V = 3
        
    @classmethod
    def is_valid(cls, cat):
        return cat >= 0 and cat <= 3


class StaffStatus:
    ACTIVE = 1
    INACTIVE = 2
    TRANSFER_OUTGOING = 4
    # TRANSFER_INCOMING = 4
