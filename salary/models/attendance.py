from django.db import models
from .core import RelatableModel, College
from .staff import Staff

class AttendanceRow(models.Model, RelatableModel):
    relation_name = "atnd_row_id"
    class Meta:
        db_table = 'sl_attendance_rows'
        
    m_date = models.DateField(db_column="m_date")
    college = College.get_key()
    
    staff = Staff.get_key()
    
    time_in = models.TimeField(db_column="time_in", null=True, blank=True)
    time_out = models.TimeField(db_column="time_out", null=True, blank=True)
    
    rec_time_in = models.TimeField(db_column="rec_time_in", null=True, blank=True)
    rec_time_out = models.TimeField(db_column="rec_time_out", null=True, blank=True)
    
    leave_status = models.SmallIntegerField(db_column='leave_status')
    latest = models.SmallIntegerField(db_column='latest')
    replaces_row_id = models.IntegerField(db_column='replaces_row_id')
    
