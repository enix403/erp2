from ..models import (
    Station,
    Subject
)

def make_station(name: str):
    
    station = Station()
    station.name = name
    station.save()
    
    return station

def make_subject(name):
    subject = Subject()
    subject.name = name
    subject.save()
    
    return subject