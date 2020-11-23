import salary.auth.initialperms as manage_perms
from salary.models import College

def run():
    
    # c = College()
    # c.pk = 2
    # c.name = 'LBC2'
    # c.station_id = 1
    
    # c.save()
    
    manage_perms.run()