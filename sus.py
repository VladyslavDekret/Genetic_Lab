import random

from numpy import random

from population import Population


class RankLinearSUS:
    def __init__(self, b):
        self.b = b
        self.name = self.__class__.__name__ + str(b)

    def linear_sus(self, population: Population):
        size = len(population.chromosomes)
        individuals_prob = list(
            map(lambda index: self.calc_prob(size, index), range(size))
        )
        individuals_prob.reverse()
        population.chromosomes.reverse()
        reversed_chromosomes = population.chromosomes
        number_of_parents = len(reversed_chromosomes)
        step = sum(individuals_prob) / number_of_parents
        point = random.random() * step
        sus_selection = []

        shuffled_probs = zip(reversed_chromosomes, individuals_prob)

        for chromosome, prob in shuffled_probs:
            while point <= prob:
                sus_selection.append(chromosome)
                point += step
            point = point - prob

        population.update_chromosomes(sus_selection)

        chromosomes = population.chromosomes.copy()
        chromosomes = self.shuffle(chromosomes)
        population.update_chromosomes(chromosomes)

        return population

    def select(self, population: Population):
        chromosomes = population.chromosomes.copy()
        chromosomes = self.shuffle(chromosomes)
        chromosomes = self.sort(chromosomes)
        population.update_chromosomes(chromosomes)
        return self.linear_sus(population)

    def calc_prob(self, size: int, rank: int):
        prob = ((2 - self.b) / size) + ((2 * rank * (self.b - 1)) / (size * (size - 1)))
        return prob

    def shuffle(self, chromosomes):
        return sorted(chromosomes.copy(), key=lambda _: random.random())

    def sort(self, chromosomes):
        return sorted(chromosomes.copy(), key=lambda chromosome: chromosome.fitness)
