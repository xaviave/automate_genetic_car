class Sensor:
    pos: tuple
    intensity: float
    using_time: float
    sensor_angle: float
    _temperature: float = 1.0  # not use yet but need a calculus to change consumption when temperature graduate (simulation)
    _energy_usage: float

    def __init__(self):
        self.pos = (0, 0, 0)
        self.intensity = 0
        self.using_time = 0
        self.sensor_angle = 0
        self._energy_usage = 0

    @property
    def _consumption(self):
        return self.intensity * self.using_time * self._temperature

    def detect(self):
        # call power unit_checker
        """
        PowerUnits._consumption(self._consumption, self._energy_usage)
        everything will stop right now if there not enough power
        """
