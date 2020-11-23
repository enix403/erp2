from django.db import models


class RelatableModel:

    relation_name = ""

    @classmethod
    def get_key(cls, col_name=None, r_name=None, null=False):
        return models.ForeignKey(
            cls,
            db_column=cls.relation_name if col_name is None else col_name,
            db_constraint=False,
            related_name="+" if r_name is None else r_name,
            on_delete=models.DO_NOTHING,
            null=null,
            blank=null
        )


class Station(models.Model, RelatableModel):
    relation_name = "station_id"

    class Meta:
        db_table = "sl_stations"
    name = models.CharField(max_length=20, db_column="name")
    colleges: models.Manager


class College(models.Model, RelatableModel):
    relation_name = "college_id"

    class Meta:
        db_table = "sl_colleges"
    name = models.CharField(max_length=20, db_column="name")
    station = Station.get_key("station_id", 'colleges')

    sections: models.Manager
    staffs: models.Manager
    time_tables: models.Manager
    role_params: models.Manager
    lecture_records: models.Manager

    staffs_v2: models.Manager
        
    
    
class Subject(models.Model, RelatableModel):
    relation_name = 'subject_id'

    class Meta:
        db_table = "sl_subjects"
    name = models.CharField(max_length=20, db_column='name')


