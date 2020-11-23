from django.db import models
from .core import RelatableModel, College
from .timetable import TimeTableCell, TimeTable
from .sectioning import Section
from .staff import Staff


class LectureRecord(models.Model, RelatableModel):
    relation_name = "lecture_record_id"
    class Meta:
        db_table = "sl_lecture_records"
    
    college = College.get_key(r_name='lecture_records')
    m_date = models.DateField(db_column='m_date')
    score = models.SmallIntegerField(db_column='score')
    cell = TimeTableCell.get_key(col_name='cell_id')
    
    section = Section.get_key()
    lecture_index = models.PositiveSmallIntegerField()
    
    status = models.SmallIntegerField(db_column='status')
    
    fixtures: models.Manager

class Fixture(models.Model, RelatableModel):
    relation_name = "fixture_id"
    class Meta:
        db_table = "sl_fixtures"
    
    college = College.get_key()
    m_date = models.DateField(db_column='m_date')
    lecture_record = LectureRecord.get_key(col_name='lecture_record_id', r_name='fixtures')
    # cell = TimeTableCell.get_key()
    section = Section.get_key(r_name='section_id')
    staff = Staff.get_key()
    lecture_index = models.SmallIntegerField(db_column='lecture_index')
    
    reason = models.SmallIntegerField(db_column='reason')
    
    remarks = models.CharField(db_column='remarks', max_length=200, null=True, blank=True)
        
        
# class TableActivationHistory(models.Model, RelatableModel):
#     relation_name = "table_history_id"
#     class Meta:
#         db_table = "sl_table_history"
        
#     college = College.get_key()
#     date_start = models.DateField(db_column='date_start')
#     date_end = models.DateField(db_column='date_end', null=True, blank=True)
#     table = TimeTable.get_key()
#     table_weekday = models.SmallIntegerField(db_column='table_weekday')
#     current = models.SmallIntegerField(db_column='current')
    
    
# class TargetTableRecord(models.Model, RelatableModel):
#     relation_name = 'target_record_id'
#     class Meta:
#         db_table = "sl_target_records"
        
#     m_date = models.DateField()
#     college = College.get_key()
#     table = TimeTable.get_key()
#     invalid = models.SmallIntegerField(db_column='invalid', default=0)
    

class Holiday(models.Model, RelatableModel):
    relation_name = 'holiday_id'
    class Meta:
        db_table = 'sl_holidays'
        
    college = College.get_key()
    allow_atnd = models.SmallIntegerField(db_column='allow_atnd')
    remarks = models.CharField(db_column='remarks', max_length=200, null=True, blank=True)
    
    date_start = models.DateField(db_column='date_start')
    date_end = models.DateField(db_column='date_end')
