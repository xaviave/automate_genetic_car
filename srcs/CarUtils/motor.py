import numpy as np

from Tools.GeometryUtils import GeometryUtils


class Motor(GeometryUtils):
    # could add torque
    top_speed: float
    max_acceleration: float
    _using_time: float = 0.0
    _temperature: float = 1.0  # not use yet but need a calculus to change consumption when temperature graduate (simulation)
    _energy_usage: float = 0.0

    def __init__(self, max_acceleration, top_speed):
        self.top_speed = top_speed
        self.max_acceleration = max_acceleration

    @property
    def _consumption(self):
        # redefine intensity around the acceleration parameter, nearly the same
        return self.intensity * self._using_time * self._temperature

    def move(self, car_coord, next_car_coord, angle):
        """
        PowerUnits._consumption(self._consumption, self._energy_usage)
        everything will stop right now if there not enough power
        """
        """
        add actual acceleration and actual speed
        then find equation that calcul distance to move thanks acceleration and speed 
        """
        return next_car_coord
        return (
            next_car_coord
            if self._vec_length_from_points(next_car_coord, car_coord)
            < self.max_acceleration
            else (
                int(car_coord[0] + (np.cos(angle) * self.max_acceleration)),
                int(car_coord[1] + (np.sin(angle) * self.max_acceleration)),
            )
        )
