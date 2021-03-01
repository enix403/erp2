from django.db import models, connection


class TinyInt(models.SmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint"
        else:
            return super().db_type(connection)

class PositiveTinyInt(models.SmallIntegerField, models.fields.PositiveIntegerRelDbTypeMixin):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint unsigned"
        else:
            return super().db_type(connection)

