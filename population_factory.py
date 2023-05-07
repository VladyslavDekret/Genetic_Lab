from numpy import random
from chromosome import Chromosome
from population import Population
from coding import encode, encode_bin, EncodeType


class PopulationFactory:
    def __init__(self, fitness_function):
        self.fitness_function = fitness_function
        self.encode_func = encode if fitness_function.encode_type is EncodeType.GRAY_CODE else encode_bin

    def generate_population_bit(self, n, l):
        chromosomes = [self.fitness_function.generate_optimal(l)]
        for j in range(1, n):
            code = random.binomial(n=1, p=0.5, size=l)
            fitness = self.fitness_function.estimate(code)
            chromosomes.append(Chromosome(code, fitness, j + 1))
        return Population(chromosomes)

