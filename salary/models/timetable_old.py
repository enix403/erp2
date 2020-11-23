from django.db import models
from .core import RelatableModel, College

from .sectioning import Section
from .core import Subject
from .staff import RoleParam

from ..logic.constants import LectureType

class TimeTable(models.Model, RelatableModel):
    relation_name = 'time_table_id'
    class Meta:
        db_table = 'sl_time_tables'
    
    college = College.get_key(r_name='time_tables')
    # session = models.IntegerField(db_column='session')
    week_day = models.IntegerField(db_column='week_day')
    active = models.IntegerField(db_column='active')
    
    lectures: models.Manager
    cells: models.Manager
    
class TimeTableLecture(models.Model, RelatableModel):
    relation_name = 'lecture_id'
    class Meta:
        db_table = 'sl_time_table_lectures'
        
    time_table = TimeTable.get_key(r_name='lectures')
    lecture_index = models.IntegerField(db_column='lecture_index')
    
    time_start = models.TimeField(db_column='time_start')
    time_end = models.TimeField(db_column='time_end')
    
    ui_number = models.IntegerField(db_column='ui_number')
    lecture_type = models.IntegerField(db_column='lecture_type')

    def format_name(self):
        if self.lecture_type == LectureType.NORMAL:
            return "Lecture %d" % self.ui_number
        elif self.lecture_type == LectureType.BREAK:
            return "Break"
        elif self.lecture_type == LectureType.ZERO:
            return 'Zero Lecture'
        
        return "ERROR"

    
class TimeTableCell(models.Model, RelatableModel):
    relation_name = 'cell_id'
    class Meta:
        db_table = 'sl_time_table_cells'
        
    time_table = TimeTable.get_key(r_name='cells')
    
    section = Section.get_key()
    faculty_param = RoleParam.get_key(col_name='faculty_param_id')
    subject = Subject.get_key()
    
    active = models.PositiveSmallIntegerField(db_column='active')

    
    # lecture_index = models.IntegerField(db_column='lecture_index')
    lecture = TimeTableLecture.get_key(r_name='lecture_id')
    lecture_type = models.IntegerField(db_column='lecture_type')
    lecture_index = models.IntegerField(db_column='lecture_index')
