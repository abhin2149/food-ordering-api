import requests
from utils.constants import BASE_URL
from utils.config import get_config


# Call distance-matrix API to fetch time between origin and destination(s)
def get_distance_time_between_locations(origin, destinations):
    destinations = "|".join(destinations)
    params = {
        'key': get_config()["API_TOKEN"],
        'origins': origin,
        'destinations': destinations
    }
    r = requests.get(url=BASE_URL, params=params)
    data = r.json()
    return [resp['duration']['value'] for resp in data['rows'][0]['elements']]
