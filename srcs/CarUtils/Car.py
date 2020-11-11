import os
import string
import random
import datetime

import numpy as np

from Tools.ImageHandler import ImageHandler


class Car:
    angle: float = 0.0
    coord: tuple = (0, 0)
    motors: list = []
    sensors: list = []
    headlights: list = []
    power_utils: list = []

    """
        Private Methods
    """

    @staticmethod
    def _check_path(path):
        if os.path.exists(path) is False:
            os.makedirs(path)

    def _check_sensors_state(self):
        return True

    def _check_power_state(self):
        return True

    def _get_light_map(self, shape: tuple):
        light_map = np.zeros(shape=shape)
        for light in self.headlights:
            light_map += light.light(np.zeros(shape=shape), self.angle)
        return light_map

    def _get_sensor_map(self, light_map: np.ndarray):
        """
        sum all matrix, allow weight on each pixel
        """
        sensor_map = np.zeros(shape=light_map.shape)
        for sensor in self.sensors:
            sensor_map += sensor.detect(self.pos, self.angle, light_map)
        return sensor_map

    def _use_motors(self, sensor_map):
        """
        could add efficiency depending to environment et number of motors
        """
        dist: float = 0
        for x in self.motors:
            dist += x.move(self.angle, 1, 10, sensor_map)
        return dist / len(self.motors)

    def _update_coord(self, move: float):
        # a thing like angle * move + self.pos -> nope at all
        # self.pos =
        pass

    def _turn(self, light_map, sensor_map):
        return 1.0

    def _drive(self, track_map, timer=datetime.timedelta(seconds=1)):
        i = 0
        start_time = datetime.datetime.now()
        while all(
            [
                datetime.datetime.now() - start_time < timer,
                self._check_sensors_state(),
                self._check_power_state(),
            ]
        ):
            file_name = os.path.join(self.tmp_tracks_path, f"{i}")
            light_map = self._get_light_map(track_map.shape[:2])
            sensor_map = self._get_sensor_map(light_map)
            self.angle += self._turn(light_map, sensor_map)
            move = self._use_motors(sensor_map)
            self._update_coord(move)
            ImageHandler().np_to_img(
                file_name, track_map, light_map, sensor_map, self.pos
            )
            i += 1

    def __init__(self, pos, sensors, headlights, motors, power_utils):
        self.pos = pos
        self.motors = motors  # for now multi motors is useless
        self.sensors = sensors
        self.headlights = headlights
        self.power_utils = power_utils
        rn = "".join(random.choice(string.ascii_letters) for _ in range(10))
        self.gif_path = os.path.join("data", "recap_gif_tracks", rn)
        self.tmp_tracks_path = os.path.join("data", "tmp_tracks", rn)
        self._check_path(self.gif_path)
        self._check_path(self.tmp_tracks_path)

    """
        Public Methods
    """

    def launch(self, track_map, gif=False):
        self._drive(track_map)
        if gif:
            ImageHandler().save_gif(
                os.path.join(self.gif_path, "xagc.gif"),
                self.tmp_tracks_path,
                os.listdir(self.tmp_tracks_path),
                delete=True,
            )
