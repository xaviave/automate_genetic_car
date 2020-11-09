from enum import Enum


class TrackEnvironment(Enum):
    ROAD = 0x0
    GRASS = 0x00FF

    @staticmethod
    def list():
        return list(map(lambda c: c.value, TrackEnvironment))
