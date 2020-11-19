import datetime
import sys
import threading

from numpy import random

from CarUtils.Car import Car
from CarUtils.Headlight import Headlight
from CarUtils.Motor import Motor
from CarUtils.Sensor import Sensor
from Tools.Genetic import Genetic
from Tools.ImageHandler import ImageHandler
from TrackUtils.TrackGenerator import TrackGenerator


class GeneticCar(Genetic):
    @staticmethod
    def _generate_sensor_headlight(coord, avoid, c):
        angle = random.random() + 0.01
        orientation = 1 if (random.randint(0, 9) % 2) == 1 else -1
        angle_range = random.randint(20, 70) / 100
        intensity = random.randint(1, 30)
        args = [coord, intensity, orientation * angle, angle_range]
        if c == Sensor:
            args.append(avoid)
        return c(*args)

    def init_population(self):
        coord = (0, 0)
        self.m = Motor(10, 100)
        self.population = []
        for _ in range(self.population_size):
            angle = random.random() + 0.01
            min_heat_map = random.randint(0, 255)
            s = self._generate_sensor_headlight(coord, self.avoid, Sensor)
            h = self._generate_sensor_headlight(coord, self.avoid, Headlight)
            self.population.append(
                {
                    "obj": Car(
                        coord=coord,
                        default_angle=angle,
                        min_heat_map=min_heat_map,
                        sensors=[s],
                        headlights=[h],
                        motors=[self.m],
                        power_utils=[],
                    ),
                    "grade": 0,
                }
            )

    def _launch_car(self, car, track_map):
        car.launch(track_map, gif=True)

    def fitness_calculation(self):
        track = TrackGenerator()
        track_map = ImageHandler().get_img(track.file_name, delete=True)
        threads = []
        for individual in self.population:
            x = threading.Thread(
                target=self._launch_car, args=(individual["obj"], track_map)
            )
            x.start()
            threads.append(x)
        for x in threads:
            x.join()
        for i, individual in enumerate(self.population):
            g = 0
            if tuple(
                track_map[individual["obj"].coord[0]][individual["obj"].coord[1]]
                > (200, 200, 200, 255)
            ):
                g += 1000
            g += - individual["obj"].iteration + individual["obj"].coord[0] + individual["obj"].coord[1]
            self.population[i]["grade"] = g

    def mating_poll(self):
        """
        select the first half of the population with the highest match
        """
        self.past_population = self.population
        self.population = sorted(
            self.population, key=lambda ind: ind["grade"], reverse=True
        )[: int(self.population_size / 2)]

    def parents_selection(self):
        if len(self.population) < self.initial_population:
            self.population.extend(
                [
                    self.past_population[random.randint(0, self.population_size - 1)]
                    for _ in range(self.population_size - len(self.population))
                ]
            )
        random.shuffle(self.population)
        self.population_size = len(self.population)

    def _random_crossover(self, parent1, parent2):
        args = [(0, 0)]
        for k, v in parent1.__dict__().items():
            args.append(v if (random.randint(0, 9) % 2) == 1 else parent2.__dict__()[k])
        return args + [[self.m], []]

    def _crossover(self, parent1, parent2) -> list:
        super()._crossover(parent1, parent2)
        args1 = self._random_crossover(parent1["obj"], parent2["obj"])
        args2 = self._random_crossover(parent1["obj"], parent2["obj"])
        return [{"obj": Car(*args1), "grade": 0}, {"obj": Car(*args2), "grade": 0}]

    def _random_mutation(self, individual, max_mut):
        args = [(0, 0)]
        mut = 0
        for k, v in individual.__dict__().items():
            r = v
            if (random.randint(0, 9) % 2) == 1 and mut < max_mut:
                mut += 1
                if k == "min_heat_map":
                    r = random.randint(0, 255)
                elif k == "angle":
                    r = random.random() + 0.01
                elif k == "sensor":
                    r = [self._generate_sensor_headlight((0, 0), self.avoid, Sensor)]
                elif k == "headlight":
                    r = [self._generate_sensor_headlight((0, 0), self.avoid, Headlight)]
            args.append(r)
        return args + [[self.m], []]

    def _mutation(self, individual):
        super()._mutation(individual)
        args = self._random_mutation(individual["obj"], 2)
        individual["obj"] = Car(*args)

    def check_result(self) -> bool:
        timer = datetime.timedelta(minutes=self.timer)
        if datetime.datetime.now() - self.start_time < timer:
            return False
        return True

    def mating(self):
        temp_pop = []
        for _ in range(int(self.population_size / 2)):
            parent1 = random.randint(0, self.population_size - 1)
            parent2 = random.randint(0, self.population_size - 1)
            temp_pop.extend(
                self._crossover(self.population[parent1], self.population[parent2])
            )
        if self.mutation > 0:
            for _ in range(self.mutation):
                self._mutation(temp_pop[random.randint(0, self.population_size - 1)])
        self.population = temp_pop
        self.population_size = len(self.population)

    def logging(self):
        super().logging()
        print(
            sorted(self.population, key=lambda ind: ind["grade"], reverse=True)[0][
                "obj"
            ].gif_path
        )

    def __init__(self, population_size, mutation, timer, avoid):
        self.mutation = mutation
        self.population_size = population_size
        self.initial_population = population_size
        self.avoid = avoid
        self.timer = timer
        self.init_population()
