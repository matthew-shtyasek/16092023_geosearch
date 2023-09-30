from threading import Timer

from django.conf import settings
from redis import StrictRedis


class GeoSearch(object):
    user_id: int
    location: tuple
    timer: Timer  # threading

    redis = StrictRedis(host=settings.REDIS_HOST,
                        port=settings.REDIS_PORT)
    items = {}  # user_id: GeoSearch()

    def __new__(cls, user_id, location):

        if user_id in cls.items:
            cls.items[user_id].set_location(location)
            return cls.items[user_id]

        instance = super().__new__(cls) # это теперь self

        instance.user_id = user_id
        cls.items[user_id] = instance
        instance.set_location(location)

        return instance

    def set_location(self, location):
        self.validate_location(location)
        self.location = (str(location[0]), str(location[1]))

        print((settings.REDIS_GEOPOS_NAME,
                          (*self.location, self.user_id)))

        self.redis.geoadd(settings.REDIS_GEOPOS_NAME,
                          (*self.location, self.user_id))
        # self.redis.save()

    def validate_location(self, location):
        if -90 > location[1] or location[1] > 90:
            raise ValueError('Широта дОлжна быть в пределах -90:90')
        if -180 > location[0] or location[0] > 180:
            raise ValueError('Долгота должна быть в пределах -180:180')

        return True

    def __getitem__(self, item):
        item = float(item)
        result = self.redis.georadiusbymember(settings.REDIS_GEOPOS_NAME,
                                              self.user_id,
                                              item,
                                              settings.REDIS_UNITS)
        ids = list(map(int, result))
        coordinates = self.redis.geopos(settings.REDIS_GEOPOS_NAME,
                                        *ids)
        print(coordinates)
        return {id: coordinate for id, coordinate in zip(ids, coordinates)}
