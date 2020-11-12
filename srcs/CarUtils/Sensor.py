import cv2
import logging
import numpy as np


class Sensor:
    avoid: np.array
    light_vector: np.array
    position: tuple
    angle: float
    intensity: float
    angle_range: float
    _efficiency: float
    _using_time: float = 0.0
    _temperature: float = 1.0  # not use yet but need a calculus to change consumption when temperature graduate (simulation)
    _energy_usage: float = 0.0

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

    def __init__(self, pos, intensity, angle, angle_range, avoid):
        self.avoid = avoid
        self.angle = angle
        self.position = pos
        self.intensity = intensity
        self.angle_range = angle_range
        self._efficiency = self._compute_efficiency()
        self.sensor_vector = np.array(
            [pos[0] + self.intensity, pos[1] + self.intensity]
        )

    """
        Public Methods
    """

    @staticmethod
    def _rotate_around_point(vec, angle) -> np.array:
        rotate = np.array(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
        )
        return np.dot(rotate, vec)

    import sys

    np.set_printoptions(threshold=sys.maxsize)

    def detect(self, car_coord, car_angle, track_map, light_map):
        # call power unit_checker
        """
        PowerUnits._consumption(self._consumption, self._energy_usage)
        everything will stop right now if there not enough power
        """
        """
        Need to count efficiency param in light_map
        An efficiency ratio could be created for sensor too use by motors and
        obvioulsy alpha color in gif
        """

        # redondant
        angles = [car_angle - self.angle, car_angle - self.angle + self.angle_range]
        vec1 = np.add(
            self._rotate_around_point(self.sensor_vector, angles[0]), car_coord
        )
        vec2 = np.add(
            self._rotate_around_point(self.sensor_vector, angles[1]), car_coord
        )
        pts = np.array([[car_coord, vec1, vec2]], dtype=np.int32)
        intersect_map = np.zeros(track_map.shape)
        cv2.fillPoly(intersect_map, pts, (1, 0, 0, 255))

        tmp = np.any(track_map != self.avoid, axis=2)
        tmp_intersect = np.all(intersect_map == np.array([1, 0, 0, 255]), axis=2)
        tmp_light = light_map > 0

        light_sensor = np.logical_and(tmp_light, tmp_intersect)
        c = np.logical_and(tmp, light_sensor)

        sensor_map = 1 * c
        return sensor_map
