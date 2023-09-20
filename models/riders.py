from odmantic import Model
from typing import Optional


class Location(Model):
    lat: float
    long: float


class Rider(Model):
    username: str
    password: str
    isActive: bool = True
    cur_loc: Optional[Location]


class RiderResponse(Model):
    username: str
    isActive: bool = True
    cur_loc: Optional[Location]
