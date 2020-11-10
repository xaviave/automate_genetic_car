import random
import datetime

from Tools.Genetic import Genetic


class Individual:
    genes: list
    match: int

    def __init__(self, genes):
        self.match = 0
        self.genes = genes

    def __str__(self):
        return f"Genes = {self.genes}, match = {self.match}"

    def change_match(self, n: int):
        self.match = n


class DigitalcodeFounder(Genetic):
    solution: list
    password_len: int

    """
        Override Methods
    """

    def init_population(self):
        self.population = [
            Individual(self._gen_code(self.password_len)) for _ in range(self.population_size)
        ]

    def fitness_calculation(self):
        for i, individual in enumerate(self.population):
            self.population[i].change_match(
                sum(1 for x, gene in enumerate(individual.genes) if gene == self.solution[x])
            )

    def mating_poll(self):
        """
        select the first half of the population with the highest match
        """
        self.past_population = self.population
        self.population = sorted(self.population, key=lambda ind: ind.match, reverse=True)[
            : int(self.population_size / 2)
        ]

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

    def _crossover(self, parent1, parent2) -> list:
        super()._crossover(parent1, parent2)
        len_genes = int(len(parent1.genes) / 2)
        return [
            Individual(genes=[*parent1.genes[:len_genes], *parent2.genes[len_genes:]]),
            Individual(genes=[*parent2.genes[:len_genes], *parent1.genes[len_genes:]]),
        ]

    def _mutation(self, individual):
        super()._mutation(individual)
        individual.genes[random.randint(0, len(individual.genes) - 1)] = random.randint(0, 9)

    def check_result(self) -> bool:
        if any([1 for ind in self.population if ind.genes == self.solution]):
            return True
        return False

    def logging(self):
        super().logging()
        print(f"Solution is {self.solution}")
        for x in self.population:
            if self.solution == x.genes:
                print(x)
                return

    """
    Private Methods
    """

    @staticmethod
    def _gen_code(password_len):
        code = []
        for _ in range(password_len):
            code.append(random.randint(0, 9))
        return code

    def __init__(self, population_size, password_len=100, mutation=0):
        self.population_size = population_size
        self.initial_population = population_size
        self.mutation = mutation
        self.password_len = password_len
        self.solution = self._gen_code(password_len)
        self.init_population()
