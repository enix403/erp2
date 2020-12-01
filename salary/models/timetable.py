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



class TimeTableLecture(models.Model, RelatableModel):
    relation_name = 'tbl_lec_id'

    class Meta:
        db_table = 'tbl_lecs'

    lecture_index = models.PositiveSmallIntegerField()
    table = TimeTable.get_key(r_name='cells')
    active = models.PositiveSmallIntegerField()

    # dates active between (both inclusive)
    date_start = models.DateField()
    date_end = models.DateField(default="9999-12-31")
    
    fragments: models.Manager


class TimeTableLectureFragment(models.Model, RelatableModel):
    relation_name = 'tbl_lecfrag_id'

    class Meta:
        db_table = 'tbl_lecfrags'

    lecture = TimeTableLecture.get_key(r_name='fragments')
    rep_policy = models.CharField(max_length=20)


    time_start = models.TimeField()
    time_end = models.TimeField()
