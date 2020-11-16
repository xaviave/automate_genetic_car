import cv2
import logging
import numpy as np

from Tools.GeometryUtils import GeometryUtils


class Sensor(GeometryUtils):
    avoid: np.array
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
    def _consumption(self) -> float:
        return self.intensity * self.using_time * self._temperature

    def __init__(
        self,
        pos: tuple,
        intensity: float,
        angle: float,
        angle_range: float,
        avoid: list,
    ):
        self.avoid = avoid
        self.angle = angle
        self.position = pos
        self.intensity = intensity
        self.angle_range = angle_range

    """
        Public Methods
    """

    @property
    def sensor_vector(self):
        return np.array(
            [self.coord[0] + self.intensity, self.coord[1] + self.intensity]
        )

    def detect(
        self,
        car_coord: tuple,
        car_angle: float,
        track_map: np.ndarray,
        light_map: np.ndarray,
        i,
    ) -> np.ndarray:
        """
        PowerUnits._consumption(self._consumption, self._energy_usage)
        everything will stop right now if there not enough power
        """

        """
        Generate an intensity map of sensor detection thanks to light_map
        """
        self.coord = car_coord
        # boolean map with sensor vision mask
        range_map = self._get_triangle_mask(
            np.zeros(track_map.shape),
            self.sensor_vector,
            car_coord,
            car_angle - self.angle,
            car_angle - self.angle + self.angle_range,
        )
        # boolean map with light map and sensor mask,
        light_sensor = np.logical_and(light_map, range_map)

        # boolean map with good env (road) mask
        tmp = np.any(track_map != self.avoid, axis=2)

        # apply all mask on road map mask
        c = np.logical_and(tmp, light_sensor)
        # mask = c * 1
        # l = mask == 0
        # mask[l] = 255
        # dist = mask.astype(np.uint8)
        # dist = cv2.cvtColor(dist, cv2.COLOR_GRAY2RGBA)
        # dist[car_coord[0]][car_coord[1]] = (0, 255, 0, 255)
        # cv2.putText(
        #     dist,
        #     f"{np.degrees(car_angle)} {car_coord}",
        #     (10, 200),
        #     cv2.FONT_HERSHEY_DUPLEX,
        #     0.5,
        #     [0, 255, 0, 255],
        #     1,
        #     cv2.LINE_AA,
        # )
        # cv2.imwrite(f"sensor{i}.png", dist)
        return self._intensity_map(c, bin_map=True)
