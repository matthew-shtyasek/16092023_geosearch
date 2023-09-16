from threading import Timer

from django.conf import settings
from redis import StrictRedis


class GeoSearch:
    user_id: int
    location: tuple
    timer: Timer  # threading

    redis = StrictRedis(host=settings.REDIS_HOST,
                        port=settings.REDIS_PORT)
    items = {}  # user_id: GeoSearch()

    def __init__(self, user_id, location):
        self.user_id = user_id

        if -90 > location[1] or location[1] > 90:
            raise ValueError('Широта дОлжна быть в пределах -90:90')
        if -180 > location[0] or location[0] > 180:
            raise ValueError('Долгота должна быть в пределах -180:180')

        self.location = location


