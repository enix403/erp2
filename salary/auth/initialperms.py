from ..models import (
    AppUser,
    
    AclGroup,
    AclGroupPermission,
    
    AclUserGroup,
    AclUserPermission
    
)

from .constants import PermissionType
from collections import namedtuple

def groups_factory(slug, pk, name = ''):
    gr = AclGroup()
    gr.pk = pk
    gr.slug = slug
    gr.name = name
    
    # gr.save()
    
    return gr


PermsInfo = namedtuple("PermsInfo", ('read', 'write', 'edit', 'has'), defaults=([], [], [], []))
    
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
    
    
    for perm in perms.has:
        gr_perm = AclGroupPermission()
        gr_perm.group = grp
        gr_perm.perm_type = PermissionType.PERM_HAS
        gr_perm.perm = perm
        
        all_perms.append(gr_perm)
        
    # AclGroupPermission.objects.bulk_create(all_perms)
    return all_perms
    

def run():

    AclGroup.objects.all().delete()
    AclGroupPermission.objects.all().delete()

    grp_univeral_clg = groups_factory('grp_univeral_clg', 1)
    grp_own_clg_read = groups_factory("grp_own_clg_read", 2)
    grp_principal = groups_factory('grp_principal', 3)
    grp_atnd = groups_factory("grp_atnd", 4)
    grp_lecture_mark = groups_factory('grp_lecture_mark', 5)
    grp_lecture_fix = groups_factory('grp_lecture_fix', 6)
    
    AclGroup.objects.bulk_create([
        grp_univeral_clg,
        grp_own_clg_read,
        grp_principal,
        grp_atnd,
        grp_lecture_mark,
        grp_lecture_fix,
    ])



    group_perms = []
    group_perms.extend(
        add_perms(grp_univeral_clg, PermsInfo(
            [],
            [], [],
            ['access_all_clgs']
        ))
    )


    group_perms.extend(
        add_perms(grp_own_clg_read, PermsInfo(
            [
                'staff',
                'sections',
                'timetables',
                'atnd',
                'lecture',
                'holidays'
            ],
            [], [],
            []
        ))
    )


    group_perms.extend(
        add_perms(grp_principal, PermsInfo(
            [
                'staff',
                'sections',
                'timetables',
                'atnd',
                'lecture',
                'holidays'
            ],
            [
                'staff',
                'sections',
                'timetables',
                'atnd',
                'lecture_all',
                'holidays'
            ], [],
            []
        ))
    )


    group_perms.extend(
        add_perms(grp_atnd, PermsInfo(
            [
                'atnd',
            ],
            [
                'atnd',
            ], [],
            []
        ))
    )

    group_perms.extend(
        add_perms(grp_lecture_mark, PermsInfo(
            [
                'lecture',
            ],
            [
                'mark_lecture',
            ], [],
            []
        ))
    )

    group_perms.extend(
        add_perms(grp_lecture_fix, PermsInfo(
            [
                'lecture',
            ],
            [
                'fix_lecture',
            ], [],
            []
        ))
    )
    
    # print(group_perms)
    
    AclGroupPermission.objects.bulk_create(group_perms)
