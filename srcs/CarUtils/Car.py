import os

import cv2
import string
import random
import logging
import datetime

import numpy as np

from Tools.GeometryUtils import GeometryUtils
from Tools.ImageHandler import ImageHandler
from Tools.TrackData import TrackData

import sys

np.set_printoptions(threshold=sys.maxsize)


class Car(GeometryUtils):
    angle: float = 4.72
    default_angle: float
    _min_heat_map: float
    coord: tuple = (0, 0)
    tracks: list = []
    motors: list = []
    sensors: list = []
    headlights: list = []
    power_utils: list = []
    _has_turn: bool = False

    """
        Private Methods
    """

    @staticmethod
    def _check_path(path):
        if os.path.exists(path) is False:
            os.makedirs(path)

    def _check_sensors_state(self) -> bool:
        # Add error flag for gif and analysis
        return True

    def _check_power_state(self) -> bool:
        # Add error flag for gif and analysis
        return True

    def _check_coord(self) -> bool:
        # Add error flag for gif and analysis
        return False if self.coord[0] < 0 or self.coord[1] < 0 else True

    def _get_light_map(self, shape: tuple, i):
        self.light_map.fill(0)
        self.light_mask.fill(0)
        for light in self.headlights:
            tmask, tmap = light.light(self.coord, self.angle, np.zeros(shape=shape), i)
            self.light_mask += tmask
            self.light_map = cv2.add(tmap, self.light_map)

    def _get_sensor_map(self, track_map: np.ndarray, i):
        """
        sum all matrix, allow weight on each pixeldx
        """
        self.sensor_map.fill(0)
        for sensor in self.sensors:
            self.sensor_map = cv2.add(
                self.sensor_map,
                sensor.detect(self.coord, self.angle, track_map, self.light_mask, i),
            )

    def _use_motors(self, next_car_coord: tuple):
        """
        could add efficiency depending to environment and number of motors
        """
        """
        think about the multi motor calculation
        dist: float = 0
        for x in self.motors:
            dist += x.move(self.coord, self.angle)
        return dist / len(self.motors)
        """
        self.coord = self.motors[0].move(self.coord, next_car_coord, self.angle)

    def _no_sensor_detection(self, angle: bool) -> tuple:
        print("_no_sensor_detection")
        self._has_turn = False
        self.angle += -self.default_angle if angle else self.default_angle
        return self.coord

    def _compute_heat_map(self, sensor_map: np.ndarray) -> np.ndarray:
        """
        with a 2 axis sensor map (addition of RGBA) as heat_map
        return the farthest point from the map with
        higher dist from car coord ratio by the light intensity
        """
        coorda = np.where(sensor_map > self._min_heat_map)
        coorda = np.squeeze(coorda).T
        # need opti
        b = -1
        coord = [-1, -1]
        if len(coorda.shape) == 1:
            # one value found
            return coorda
        for a in coorda:
            tmp = self._vec_length(
                a, self.coord
            )  # * (sensor_map[a[0]][a[1]] * 0.2 / 100)
            if tmp > b:
                b = tmp
                coord = a
        return coord

    def _turn(self, i):
        """
        if b is returned, it's equaled to the point B of a right angle of the triangle CAB
        C is the car coord, BC are the hypotension of this triangle
        A is X's car coord and Y's B
        It allows us to find the angle of BCA, minus car angle is the good car direction
        """
        b = self._compute_heat_map(np.add.reduce(self.sensor_map, 2))
        if b is [-1, -1] or tuple(b) == tuple([self.coord[0], b[1]]):
            print(tuple(b) == tuple([self.coord[0], b[1]]))
            return self._no_sensor_detection(tuple(b) == tuple([self.coord[0], b[1]]))
        angle = self._vec_length(b, (self.coord[0], b[1])) / self._vec_length(
            self.coord, b
        )
        print(
            f"""
car coord {self.coord} - p2 = {b} - p3 = {(self.coord[0], b[1])}
(car_coord; p2) length: {self._vec_length(self.coord, b)}
(p2 p3) length: {self._vec_length(b,  (self.coord[0], b[1]))}
angle = {angle}
"""
        )
        if -1 <= angle <= 1:
            self._has_turn = True
            self.angle += np.arccos(angle)
            return b
        return self._no_sensor_detection(True)

    def _drive(self, track_map, timer=datetime.timedelta(seconds=20)):
        i = 0
        start_time = datetime.datetime.now()
        while all(
            [
                datetime.datetime.now() - start_time < timer,
                self._check_sensors_state(),
                self._check_power_state(),
                self._check_coord(),
                # i < 7,
            ]
        ):
            print(f"iteration: {i}")
            file_name = os.path.join(self.tmp_tracks_path, f"{i}")
            self._get_light_map(track_map.shape, i)
            self._get_sensor_map(track_map, i)
            next_car_coord = (
                self._turn(i)
                if np.max(self.sensor_map)
                else self._no_sensor_detection()
            )
            last_car_coord = self.coord
            if self._has_turn:
                self._use_motors(next_car_coord)
            self.tracks.append(
                TrackData(
                    file_name,
                    np.copy(self.light_map),
                    np.copy(self.sensor_map),
                    self.coord,
                    last_car_coord,
                )
            )
            i += 1
        logging.info(f"iteration: {i}")

    def __init__(
        self,
        coord,
        default_angle,
        min_heat_map,
        sensors,
        headlights,
        motors,
        power_utils,
    ):
        cv2.setUseOptimized(True)
        self.coord = coord
        self.motors = motors  # for now multi-motors is useless
        self.sensors = sensors
        self.headlights = headlights
        self.power_utils = power_utils
        self.default_angle = default_angle
        self._min_heat_map = min_heat_map
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
                # delete=True,
            )
