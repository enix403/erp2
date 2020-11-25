from ..models import (
    # AppUser,
    
    AclGroup,
    AclGroupPermission,
    
    # AclUserGroup,
    # AclUserPermission
    
)

from .constants import PermissionType
from collections import namedtuple

def groups_factory(slug, pk):
    gr = AclGroup()
    gr.pk = pk
    gr.slug = slug
    
    # gr.save()
    
    return gr


PermsInfo = namedtuple("PermsInfo", ('read', 'write', 'edit'), defaults=([], [], []))
    
def add_perms(grp, perms: PermsInfo):
    
    all_perms = []
    
    for perm in perms.read:
        gr_perm = AclGroupPermission()
        gr_perm.group = grp
        gr_perm.perm_type = PermissionType.PERM_READ
        gr_perm.perm = perm
        
        all_perms.append(gr_perm)
    
    for perm in perms.write:
        gr_perm = AclGroupPermission()
        gr_perm.group = grp
        gr_perm.perm_type = PermissionType.PERM_WRITE
        gr_perm.perm = perm

        all_perms.append(gr_perm)


    for perm in perms.edit:
        gr_perm = AclGroupPermission()
        gr_perm.group = grp
        gr_perm.perm_type = PermissionType.PERM_EDIT
        gr_perm.perm = perm
        
        all_perms.append(gr_perm)
    
        
    return all_perms
    
    
def run():
    AclGroup.objects.all().delete()
    AclGroupPermission.objects.all().delete()
    
    grp_root = groups_factory('grp_root', 1)
    grp_principal = groups_factory('grp_principal', 2)
    
    AclGroup.objects.bulk_create([
        grp_root,
        grp_principal
    ])
    
    group_perms = []
    group_perms.extend(
        add_perms(grp_root, PermsInfo(
            ['*'],
            ['*'], 
            ['*'],
        ))
    )
    
    group_perms.extend(
        add_perms(grp_principal, PermsInfo(
            ['*'],
            [
                'sections',
            ],
            [],
        ))
    )
    
    AclGroupPermission.objects.bulk_create(group_perms)