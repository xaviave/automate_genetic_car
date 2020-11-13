import os

import cv2
import string
import random
import logging
import datetime

import numpy as np

from Tools.ImageHandler import ImageHandler
from Tools.TrackData import TrackData

import sys

np.set_printoptions(threshold=sys.maxsize)


class Car:
    angle: float = 4.72
    coord: tuple = (0, 0)
    tracks: list = []
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
        self.light_map.fill(0)
        self.light_mask.fill(0)
        for light in self.headlights:
            tmask, tmap = light.light(
                self.coord,
                self.angle,
                np.zeros(shape=shape),
            )
            # print(f"light_mask = {self.light_mask.dtype} - tmask {tmask.dtype}")
            # print(f"light_map = {self.light_map.dtype} - tmap {tmap.dtype}")
            self.light_mask += tmask
            self.light_map = cv2.add(tmap, self.light_map)

    def _get_sensor_map(self, track_map: np.ndarray):
        """
        sum all matrix, allow weight on each pixel
        """
        self.sensor_map.fill(0)
        for sensor in self.sensors:
            self.sensor_map = cv2.add(
                self.sensor_map,
                sensor.detect(self.coord, self.angle, track_map, self.light_mask),
            )

    def _use_motors(self):
        """
        could add efficiency depending to environment et number of motors
        """
        dist: float = 0
        for x in self.motors:
            dist += x.move(self.angle, 1, 10, self.sensor_map)
        return dist / len(self.motors)

    def _update_coord(self, move: float):
        # a thing like angle * move + self.pos -> nope at all
        # self.pos =
        pass

    def _turn(self):
        return np.radians(5.0)

    def _drive(self, track_map, timer=datetime.timedelta(seconds=2)):
        i = 0
        start_time = datetime.datetime.now()
        while all(
            [
                datetime.datetime.now() - start_time < timer,
                self._check_sensors_state(),
                self._check_power_state(),
            ]
        ):
            # logging.info(f"iteration: {i}")
            file_name = os.path.join(self.tmp_tracks_path, f"{i}")
            self._get_light_map(track_map.shape)
            self._get_sensor_map(track_map)
            self.angle += self._turn()
            move = self._use_motors()
            self._update_coord(move)
            self.tracks.append(
                TrackData(
                    file_name,
                    np.copy(self.light_map),
                    np.copy(self.sensor_map),
                    self.coord,
                )
            )
            i += 1
        logging.info(f"iteration: {i}")

    def __init__(self, coord, sensors, headlights, motors, power_utils):
        self.coord = coord
        self.motors = motors  # for now multi-motors is useless
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
        self.light_map = np.zeros(track_map.shape, dtype=np.float32)
        self.light_mask = np.zeros(track_map.shape[:2], dtype=np.int64)
        self.sensor_map = np.zeros(track_map.shape, dtype=np.float32)
        self._drive(track_map)
        for x in self.tracks:
            ImageHandler().np_to_img(track_map, x)
        if gif:
            ImageHandler().save_gif(
                os.path.join(self.gif_path, "xagc.gif"),
                self.tmp_tracks_path,
                os.listdir(self.tmp_tracks_path),
                delete=True,
            )
