from django.db import models
from .core import RelatableModel, College, Subject
from .sectioning import Section

from .staff import Staff

from ..logic.constants import LectureType


class TimeTable(models.Model, RelatableModel):

    relation_name = 'tbl_id'

    class Meta:
        db_table = 'sl_tbls'

    college = College.get_key(r_name='time_tables')

    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

    main = models.PositiveSmallIntegerField()
    # lecture_count = models.PositiveSmallIntegerField()

    cells: models.Manager
    lectures: models.Manager
    lecture_sets: models.Manager


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
    
    code = models.CharField(max_length=20)
    
    active = models.PositiveSmallIntegerField()
    
    lectures: models.Manager
    
    def parse_code(self):
        return list(map(int, self.code[1:-1]))


class TimeTableLecture(models.Model, RelatableModel):
    relation_name = 'lec_id'

    class Meta:
        db_table = 'sl_tbl_set_lectures'

    # shortcut for lectureset.table
    table = TimeTable.get_key(r_name='lectures')
    lectureset = TimeTableLectureSet.get_key(r_name='lectures')
    lecture_index = models.IntegerField(db_column='lecture_index')

    time_start = models.TimeField(db_column='time_start')
    time_end = models.TimeField(db_column='time_end')
    
    active = models.PositiveSmallIntegerField()

    lecture_type = models.PositiveSmallIntegerField(db_column='lecture_type')



