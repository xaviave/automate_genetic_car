import numpy as np


class Headlight:
    position: tuple
    angle: float
    intensity: float  # define the "lenght" of the vision like 2 meter irl
    angle_range: float
    _using_time: float = 0.0
    _temperature: float = 1.0  # not use yet but need a calculus to change consumption when temperature graduate (simulation)
    _energy_usage: float = 0.0

    def __init__(self, pos, intensity, angle, angle_range):
        self.angle = angle
        self.position = pos
        self.intensity = intensity
        self.angle_range = angle_range

    @property
    def _consumption(self):
        return self.intensity * self.using_time * self._temperature

    def light(self, track_map: np.ndarray, car_angle: float):
        # call power unit_checker
        """
        PowerUnits._consumption(self._consumption, self._energy_usage)
        everything will stop right now if there not enough power
        """
        """
        Need to create an efficiency param for light precision counting in sensor
        and alpha in the gif rendering 
        
        Calculus must be a list of coord (x, y) in the map size track_map.shape
        then update with a mask the track_map like:
            mask = [(1, 6), (6, 19)]
            track_map[mask] = 1
        """
        track_map.fill(1)
        return track_map
