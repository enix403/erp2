class SectionType:
    REGULAR = 0
    MERGED = 1
    
    
class Gender:
    MALE = 0
    FEMALE = 1
    
    
class FacultyCategory:
    FAC_CATERGORY_M = 0
    FAC_CATERGORY_M_AND_E = 1
    FAC_CATERGORY_M_PLUS_E = 2
    FAC_CATERGORY_V = 3
    
    @classmethod
    def get_list(cls):
        return [
            cls.FAC_CATERGORY_M,
            cls.FAC_CATERGORY_M_AND_E,
            cls.FAC_CATERGORY_M_PLUS_E,
            cls.FAC_CATERGORY_V
        ]
        
    @classmethod
    def is_valid(cls, cat):
        return cat in cls.get_list()

class LectureType:
    NORMAL = 0
    BREAK = 1
    ZERO = 2



class LectureRecordStatus:
    UNSPEC = 0
    COMPLETED = 1
    FIXED = 2
    CANCELLED = 3
    EMPTY = 4
    


class StaffStatus:
    ACTIVE = 1
    INACTIVE = 2
    TRANSFERRED = 3
    
    TRANSFER_INCOMING = 4
    TRANSFER_OUTGOING = 5