from django.db import models
from .core import RelatableModel, College, Subject
from .sectioning import Section

from .staff import Staff

from ..logic.constants import LectureType


class TimeTable(models.Model, RelatableModel):

    relation_name = 'tbl_id'

    class Meta:
        db_table = 'sl_tbls'

    college = College.get_key()

    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

    main = models.PositiveSmallIntegerField()
    lecture_count = models.PositiveSmallIntegerField()

    cells: models.Manager
    lectures: models.Manager


class TimeTableCell(models.Model, RelatableModel):

    relation_name = 'tbl_cell_id'

    class Meta:
        db_table = 'sl_tbl_cells'

    table = TimeTable.get_key(r_name='cells')

    lecture_index = models.PositiveSmallIntegerField()
    section = Section.get_key()

    active = models.PositiveSmallIntegerField()

    # dates active between (both inclusive)
    date_start = models.DateField()
    date_end = models.DateField(default="9999-12-31")
    
    fragments: models.Manager


class TimeTableCellFragment(models.Model, RelatableModel):
    relation_name = 'tbl_cellfrag_id'

    class Meta:
        db_table = 'sl_tbl_cellfrags'

    cell = TimeTableCell.get_key(r_name='fragments')

    staff = Staff.get_key()
    subject = Subject.get_key()

    rep_policy = models.CharField(max_length=20)


class TimeTableLectureSet(models.Model, RelatableModel):
    relation_name = 'tbl_lecset_id'
    
    class Meta:
        db_table = "sl_tbl_lecsets"
        
    table = TimeTable.get_key(r_name='lecture_sets')
    
    date_start = models.DateField()
    date_end = models.DateField(default="9999-12-31")
    active = models.PositiveSmallIntegerField()
    
    lectures: models.Manager


class TimeTable_SetLecture(models.Model, RelatableModel):
    relation_name = 'lec_id'

    class Meta:
        db_table = 'sl_tbl_set_lectures'

    lectureset = TimeTableLectureSet.get_key(r_name='lectures')
    lecture_index = models.IntegerField(db_column='lecture_index')

    time_start = models.TimeField(db_column='time_start')
    time_end = models.TimeField(db_column='time_end')

    lecture_type = models.PositiveSmallIntegerField(db_column='lecture_type')



class TimeTableLecture(models.Model, RelatableModel):
    relation_name = 'lec_id'

    class Meta:
        db_table = 'sl_tbl_lectures'

    table = TimeTable.get_key(r_name='lectures')
    lecture_index = models.IntegerField(db_column='lecture_index')

    time_start = models.TimeField(db_column='time_start')
    time_end = models.TimeField(db_column='time_end')

    # ui_number = models.IntegerField(db_column='ui_number')
    lecture_type = models.IntegerField(db_column='lecture_type')

    # def format_name(self):
    #     if self.lecture_type == LectureType.NORMAL:
    #         return "Lecture %d" % self.ui_number
    #     elif self.lecture_type == LectureType.BREAK:
    #         return "Break"
    #     elif self.lecture_type == LectureType.ZERO:
    #         return 'Zero Lecture'

    #     return "ERROR"
