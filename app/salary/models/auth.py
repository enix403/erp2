from django.db import models
from .core import RelatableModel
from passlib.hash import pbkdf2_sha256


class AppUser(models.Model, RelatableModel):
    relation_name = 'user_id'
    class Meta:
        db_table = 'sl_users'

    name = models.CharField(db_column='name', max_length=191)
    username = models.CharField(db_column='username', max_length=191, unique=True)
    password_hash = models.CharField(db_column='password_hash', max_length=200)
    
    ''' only assume global colleges access on college_id == -1 '''  
    college_id = models.SmallIntegerField(db_column='college_id')
    role_param_id = models.SmallIntegerField(db_column='role_param_id')

    # Superuser, admin, regular user etc...
    auth_role = models.SmallIntegerField(db_column='type')
    invalidate = models.SmallIntegerField(db_column='invalidate', default=0)
    
    @classmethod
    def make(cls, name, username, password):
        user = cls()
        user.name = name
        user.username = username
        user.password_hash = pbkdf2_sha256.hash(password)
        
        return user