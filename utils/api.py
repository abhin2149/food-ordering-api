import requests
from models.riders import Location
from utils.constants import BASE_URL
from utils.config import get_config


def loc_to_string(loc: Location):
    return str(loc.lat) + ',' + str(loc.long)


# Call distance-matrix API to fetch time for all riders from the restaurant
def get_distance_time_between_locations(origins, destinations):
    destinations = "|".join([loc_to_string(d) for d in destinations])
    params = {
        'key': get_config()["API_TOKEN"],
        'origins': origins,
        'destinations': destinations
    }
    r = requests.get(url=BASE_URL, params=params)
    data = r.json()
    return [resp['duration']['value'] for resp in data['rows'][0]['elements']]


