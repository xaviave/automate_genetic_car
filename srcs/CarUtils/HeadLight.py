import cv2
import numpy as np

from Tools.GeometryUtils import GeometryUtils


class Headlight(GeometryUtils):
    position: tuple
    light_vector: np.array
    angle: float
    intensity: float
    angle_range: float
    _using_time: float = 0.0
    _temperature: float = 1.0  # not use yet but need a calculus to change consumption when temperature graduate (simulation)
    _energy_usage: float = 0.0

    def __init__(self, pos, intensity, angle, angle_range):
        self.angle = angle
        self.position = pos
        self.intensity = intensity
        self.angle_range = angle_range
        self.light_vector = np.array([pos[0] + self.intensity, pos[1] + self.intensity])

    @property
    def _consumption(self):
        return self.intensity * self.using_time * self._temperature

    def light(self, car_coord: tuple, car_angle: float, track_map: np.ndarray):
        """
        PowerUnits._consumption(self._consumption, self._energy_usage)
        everything will stop right now if there not enough power
        """
        mask = self._get_triangle_mask(
            track_map,
            self.light_vector,
            car_coord,
            car_angle - self.angle,
            car_angle - self.angle + self.angle_range,
        )
        return mask, self._intensity_map(mask, bin_map=True)
