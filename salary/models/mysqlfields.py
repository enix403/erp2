from django.db import models


class TinyIntegerField(models.IntegerField):
    
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint"
        else:
            return super(TinyIntegerField, self).db_type(connection)


class PositiveTinyIntegerField(models.IntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint unsigned"
        else:
            return super(PositiveTinyIntegerField, self).db_type(connection)


class UnsignedAutoField(models.AutoField):
    
    def __init__(self, *args, **kwargs):
        kwargs['primary_key'] = True
        kwargs['db_column'] = 'id'
        # self.primary_key = True
        # self.db_column = 'id'
        
        super().__init__(*args, **kwargs)
        
    def db_type(self, connection):
        return 'integer UNSIGNED AUTO_INCREMENT'

    def rel_db_type(self, connection):
        return 'integer UNSIGNED'
