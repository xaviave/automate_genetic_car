import numpy as np


class TrackData:
    file_name: str
    car_pos: tuple
    expeced_car_pos: tuple
    light_map: np.ndarray
    sensor_map: np.ndarray

    def __init__(self, file_name, light_map, sensor_map, car_pos, expected_car_pos):
        self.car_pos = car_pos
        self.file_name = file_name
        self.light_map = light_map
        self.sensor_map = sensor_map
        self.expected_car_pos = expected_car_pos

    def __str__(self):
        return f"""{'-' * 50}
light_map shape: {self.light_map.shape}
sensor_map shape: {self.sensor_map.shape}
file_name: {self.file_name}
car position: {self.car_pos}
expected car position: {self.expected_car_pos}
{'-' * 50}
"""
