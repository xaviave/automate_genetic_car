import numpy as np


class Sensor:
    position: tuple
    angle: float
    intensity: float  # define the "lenght" of the vision like 2 meter irl
    angle_range: float
    _efficiency: float
    _using_time: float = 0.0
    _temperature: float = 1.0  # not use yet but need a calculus to change consumption when temperature graduate (simulation)
    _energy_usage: float = 0.0
    _avoid: np.array = [
        np.array([0.0, 0.5019608, 0.0])
    ]  # let sensor find it by it s way

    """
        Private Methods
    """

    @property
    def _consumption(self):
        return self.intensity * self.using_time * self._temperature

    def _compute_efficiency(self):
        """
        Greater the angle and the intensity, less is the sensor efficinency
        efficiency is a factor that will affect the detection efficiency too
        """
        return 1.0

    def __init__(self, pos, intensity, angle, angle_range):
        self.angle = angle
        self.position = pos
        self.intensity = intensity
        self.angle_range = angle_range
        self._efficiency = self._compute_efficiency()

    """
        Public Methods
    """

    def detect(self, car_position, car_angle, light_map):
        # call power unit_checker
        """
        PowerUnits._consumption(self._consumption, self._energy_usage)
        everything will stop right now if there not enough power
        """
        """
        Need to count efficiency param in light_map
        An efficiency ratio could be created for sensor too use by motors and
        obvioulsy alpha color in gif
        
        Calculus must be a list of coord(x, y) in the map size track_map.shape
        then update with a mask the track_map like:
            mask = [(1, 6), (6, 19)]
            track_map[mask] = 1
        """
        return light_map
