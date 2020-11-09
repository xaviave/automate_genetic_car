class PowerUnits:
    _total: float

    """
        Property
    """

    @property
    def remaining_power(self) -> float:
        return self._total

    @property
    def power_state(self) -> float:
        # temperature state could be added
        return self._total / 100

    """
        Private Method
    """

    @staticmethod
    def _estimate_consumption(consumption: float, usage: float) -> float:
        return consumption * usage

    def _check_remaining_power(self, expected_consumption: float) -> bool:
        if expected_consumption > self._total:
            return False
        return True

    def _consumption(self, consumption: float, power_usage: float) -> bool:
        expected_consumption: float = self._estimate_consumption(consumption, power_usage)
        if self._check_remaining_power(expected_consumption) is False:
            # logger here
            # need to stop the car here like no power no sensor or motor
            return False
        self._total -= expected_consumption
        return True
