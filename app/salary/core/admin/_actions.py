from app.salary.models import (
    Station,
    Subject,
    College
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


def make_college(name: str, station_id: int):
    college = College()
    college.name = name
    college.station_id = station_id

    college.save()

    return college