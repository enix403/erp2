from __future__ import annotations
from ..constants import LectureType

class TableLectures:
    def __init__(self, code):
        # code is a string starting and ending with "l"
        # and containing digits in between(0, 1 and 2)
        # e.g "l0001002000l"
        self.lectures_types = list(map(int, code[1:-1]))