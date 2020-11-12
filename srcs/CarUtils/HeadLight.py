import cv2
import numpy as np


class Headlight:
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

    @staticmethod
    def _rotate_around_point(vec, angle) -> np.array:
        rotate = np.array(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
        )
        return np.dot(rotate, vec)

    def light(self, car_coord: tuple, car_angle: float, track_map: np.ndarray):
        # call power unit_checker
        """
        PowerUnits._consumption(self._consumption, self._energy_usage)
        everything will stop right now if there not enough power
        """
        """
        Need to create an efficiency param for light precision counting in sensor
        and alpha in the gif rendering
        """
        angles = [car_angle - self.angle, car_angle - self.angle + self.angle_range]
        vec1 = np.add(
            self._rotate_around_point(self.light_vector, angles[0]), car_coord
        )
        vec2 = np.add(
            self._rotate_around_point(self.light_vector, angles[1]), car_coord
        )
        pts = np.array([[car_coord, vec1, vec2]], dtype=np.int32)
        cv2.fillPoly(track_map, pts, (1, 0, 0, 255))
        track_map = 1 * np.all(track_map == np.array([1, 0, 0, 255]), axis=2)
        return track_map
