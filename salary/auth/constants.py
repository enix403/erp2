class PermissionType:
    PERM_READ = 1
    PERM_WRITE = 2
    PERM_EDIT = 3
    PERM_HAS = 4  # magic...

    @classmethod
    def slug_to_id(cls, slug):
        if slug == 'read':
            return cls.PERM_READ
        if slug == 'write':
            return cls.PERM_WRITE
        if slug == 'edit':
            return cls.PERM_EDIT
        if slug == 'has':
            return cls.PERM_HAS

    @classmethod
    def id_to_slug(cls, perm_id):
        if perm_id == cls.PERM_READ:
            return 'read'
        if perm_id == cls.PERM_WRITE:
            return 'write'
        if perm_id == cls.PERM_EDIT:
            return 'edit'
        if perm_id == cls.PERM_HAS:
            return 'has'
