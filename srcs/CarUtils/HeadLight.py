import cv2
import numpy as np

from Tools.GeometryUtils import GeometryUtils


class Headlight(GeometryUtils):
    coord: tuple
    angle: float
    intensity: float
    angle_range: float
    _using_time: float = 0.0
    _temperature: float = 1.0  # not use yet but need a calculus to change consumption when temperature graduate (simulation)
    _energy_usage: float = 0.0

    def __init__(
        self, coord: tuple, intensity: float, angle: float, angle_range: float
    ):
        self.angle = angle
        self.coord = coord
        self.intensity = intensity
        self.angle_range = angle_range

    @property
    def _consumption(self) -> float:
        return self.intensity * self.using_time * self._temperature

    @property
    def light_vector(self):
        return np.array(
            [self.coord[0] + self.intensity, self.coord[1] + self.intensity]
        )

    def light(
        self, car_coord: tuple, car_angle: float, track_map: np.ndarray, i
    ) -> np.ndarray:
        """
        PowerUnits._consumption(self._consumption, self._energy_usage)
        everything will stop right now if there not enough power
        """
        """"
        Generate a binary map and an intensity map of the light's emission 
        """
        self.coord = car_coord
        print("light")
        mask = self._get_triangle_mask(
            track_map,
            self.light_vector,
            car_coord,
            car_angle - self.angle,
            car_angle - self.angle + self.angle_range,
        )
        print("-" * 50)
        l = mask == 0
        dist = mask.astype(np.uint8)
        dist[l] = 255
        dist = cv2.cvtColor(dist, cv2.COLOR_GRAY2RGBA)
        dist[car_coord[0]][car_coord[1]] = (0, 255, 0, 255)
        cv2.putText(
            dist,
            f"{np.degrees(car_angle)} {car_coord}",
            (10, 200),
            cv2.FONT_HERSHEY_DUPLEX,
            0.5,
            [0, 255, 0, 255],
            1,
            cv2.LINE_AA,
        )
        cv2.imwrite(f"light{i}.png", dist)
        return mask, self._intensity_map(mask, bin_map=True)
