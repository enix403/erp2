from django.db import models

from .core import RelatableModel

from passlib.hash import pbkdf2_sha256



# mysqladminpass

class AppUser(models.Model, RelatableModel):
    relation_name = 'user_id'
    class Meta:
        db_table = 'sl_users'

    name = models.CharField(db_column='name', max_length=191)
    username = models.CharField(db_column='username', max_length=191, unique=True)
    password_hash = models.CharField(db_column='password_hash', max_length=200)
    college_id = models.SmallIntegerField(db_column='college_id')
    role_param_id = models.SmallIntegerField(db_column='role_param_id')
    type = models.SmallIntegerField(db_column='type')
    invalidate = models.SmallIntegerField(db_column='invalidate', default=0)
    
    acl_user_groups: models.Manager
    acl_user_perms: models.Manager
    
    
    @staticmethod
    def make(name, username, password):
        user = AppUser()
        user.name = name
        user.username = username
        user.password_hash = pbkdf2_sha256.hash(password)
        
        return user
    
    def is_type(self, *types):
        for t in types:
            if self.type == t:
                return True
        return False
    
    
    
class AclGroup(models.Model, RelatableModel):
    relation_name = 'acl_group_id'
    class Meta:
        db_table = 'sl_acl_groups'
    
    slug = models.CharField(db_column='slug', max_length=30, blank=True)
    name = models.CharField(db_column='name', max_length=30)
    
    perms: models.Manager
    

class AclGroupPermission(models.Model):
    class Meta:
        db_table = "sl_acl_group_premissons"
        
    
    group = AclGroup.get_key(r_name='perms')
    perm_type = models.PositiveSmallIntegerField(db_column='perm_type')
    perm = models.CharField(db_column='perm', max_length=50)
    
    
    
class AclUserGroup(models.Model):
    class Meta:
        db_table = 'sl_acl_user_groups'
        
    user = AppUser.get_key(r_name='acl_user_groups')
    group = AclGroup.get_key()
    # group_slug = models.CharField()
    
    
    
    
class AclUserPermission(models.Model, RelatableModel):
    class Meta:
        db_table = 'sl_acl_user_permissions'
        
    user = AppUser.get_key(r_name='acl_user_perms')
    revoke = models.PositiveSmallIntegerField(db_column="revoke")
    perm_type = models.PositiveSmallIntegerField(db_column='perm_type')
    perm = models.CharField(db_column='perm', max_length=50)
    

    
    
