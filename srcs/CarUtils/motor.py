class Motor:
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

    def move(self, angle, acceleration, actual_speed, sensor_map):
        """
        PowerUnits._consumption(self._consumption, self._energy_usage)
        everything will stop right now if there not enough power
        """
        """
            use logarithm like function to calcul the acceleration thanks to the top speed and the actual speed 
        """
        dist: float = 0.0
        return dist
