import numpy as np


class TrackData:
    car_pos: tuple
    file_name: str
    light_map: np.ndarray
    sensor_map: np.ndarray

    def __init__(self, file_name, light_map, sensor_map, car_pos):
        self.car_pos = car_pos
        self.file_name = file_name
        self.light_map = light_map
        self.sensor_map = sensor_map
