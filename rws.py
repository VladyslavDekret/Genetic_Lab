import random

from population import Population


class RankLinearRWS:
    def __init__(self, b):
        self.b = b
        self.name = self.__class__.__name__ + str(b)

    def linear_rws(self, population: Population):
        size = len(population.chromosomes)
        individuals_prob = list(
            map(lambda index: self.calc_prob(size, index), range(size))
        )

        population.update_rws(individuals_prob)

        chromosomes = population.chromosomes.copy()
        chromosomes = self.shuffle(chromosomes)
        population.update_chromosomes(chromosomes)

        return population

    def select(self, population: Population):
        chromosomes = population.chromosomes.copy()
        chromosomes = self.shuffle(chromosomes)
        chromosomes = self.sort(chromosomes)
        population.update_chromosomes(chromosomes)
        return self.linear_rws(population)

    def calc_prob(self, size: int, rank: int):
        prob = ((2 - self.b) / size) + ((2 * rank * (self.b - 1)) / (size * (size - 1)))
        return prob

    def shuffle(self, chromosomes):
        return sorted(chromosomes.copy(), key=lambda _: random.random())

    def sort(self, chromosomes):
        return sorted(chromosomes.copy(), key=lambda chromosome: chromosome.fitness)
