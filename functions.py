import numpy as np
from chromosome import Chromosome
from constants import DELTA, SIGMA
from population import Population
from population_factory import PopulationFactory
from coding import *


# Health functions


class Fconst:
    """
    Fconst(X) = 100

    Used to test noise and difference
    """

    def __init__(self):
        self.encode_type = EncodeType.BINARY
        self.factory = PopulationFactory(self)

    def estimate(self, chromosome: Chromosome):
        return 100

    def get_genotype_value(self, chromosome_code):
        return decode_bin(chromosome_code, 0, pow(2, len(chromosome_code)), len(chromosome_code))

    def generate_optimal(self, length: int):
        return Chromosome(np.zeros((length,), dtype=int), length)

    def generate_population(self, n, l):
        return self.factory.generate_population_bit(n, l)


class FHD:
    """
    FHD(X) = (l-k) + k * delta

    l = 100
    k - number of 0
    """

    def __init__(self, delta: float):
        self.delta = delta
        self.encode_type = EncodeType.BINARY
        self.factory = PopulationFactory(self)

    def get_genotype_value(self, chromosome_code):
        return np.count_nonzero(chromosome_code)

    def get_count_ones(self, chromosome_code):
        return np.count_nonzero(chromosome_code)

    def decode(self, code):
        return self.estimate(chromosome=code)

    def estimate(self, chromosome):
        k = len(chromosome) - np.count_nonzero(chromosome)
        return (len(chromosome) - k) + k * self.delta

    def generate_optimal(self, length):
        optimal = np.zeros((length,), dtype=int)
        return Chromosome(optimal, self.estimate(optimal))

    def get_optimal(self, n, l, p_m, i):
        return self.generate_optimal(l)

    def generate_population(self, n, l):
        return self.factory.generate_population_bit(n, l)


class Fx2:
    """
    Fx2 = x^2, 0 <= x <= 10.23

    max(y) = (10.23)^2, x = 10.23
    """

    def __init__(self, a: float, b: float, encode_type: EncodeType = None):
        self.a = a
        self.b = b
        self.encode_type = encode_type
        self.factory = PopulationFactory(self)

    def decode(self, code):
        decode_func = decode if self.encode_type is EncodeType.GRAY_CODE else decode_bin
        return decode_func(code, self.a, self.b, len(code))

    def encode(self, x, length):
        encode_func = encode if self.encode_type is EncodeType.GRAY_CODE else encode_bin
        return encode_func(x, self.a, self.b, length)

    def estimate(self, chromosome_code):
        x = self.decode(chromosome_code)
        return math.pow(x, 2)

    def get_genotype_value(self, chromosome_code):
        x = self.decode(chromosome_code)
        return x

    def get_count_ones(self, chromosome_code):
        return np.count_nonzero(chromosome_code)

    def generate_optimal(self, length):
        code = self.encode(self.b, length)
        return Chromosome(code, self.estimate(code))

    def get_optimal(self, n, l, p_m, i):
        return self.generate_optimal(l)

    def generate_population(self, n, l):
        return self.factory.generate_population_bit(n, l)

    def check_chromosome_success(self, ch: Chromosome):
        x = self.decode(ch.code)
        return ((math.pow(self.b, 2) - ch.fitness) <= DELTA) and (x - self.b) <= SIGMA


class F5122subx2:
    """
        F5122subx2 = (5.12)^2 - x^2, -5.12 <= x < 5.12

        max(y) = (5.12)^2, x = 0
    """

    def __init__(self, a: float, b: float, encode_type: EncodeType = None):
        self.a = a
        self.b = b
        self.extremum_x = 0
        self.extremum_y = math.pow(5.12, 2)
        self.encode_type = encode_type
        self.factory = PopulationFactory(self)

    def decode(self, code):
        decode_func = decode if self.encode_type is EncodeType.GRAY_CODE else decode_bin
        return decode_func(code, self.a, self.b, len(code))

    def encode(self, x, length):
        encode_func = encode if self.encode_type is EncodeType.GRAY_CODE else encode_bin
        return encode_func(x, self.a, self.b, length)

    def score(self, x: float):
        return math.pow(5.12, 2) - math.pow(x, 2)

    def estimate(self, chromosome_code):
        x = self.decode(chromosome_code)
        return math.pow(5.12, 2) - math.pow(x, 2)

    def get_genotype_value(self, chromosome_code):
        x = self.decode(chromosome_code)
        return x

    def get_count_ones(self, chromosome_code):
        return np.count_nonzero(chromosome_code)

    def get_optimal(self, n, l, p_m, i):
        return self.generate_optimal(l)

    def generate_optimal(self, length):
        code = self.encode(self.extremum_x, length)
        return Chromosome(code, self.extremum_y)

    def generate_population(self, n, l):
        return self.factory.generate_population_bit(n, l)

    def check_chromosome_success(self, chromosome: Chromosome):
        x = self.decode(chromosome.code)
        y = chromosome.fitness
        return (self.extremum_y - y) <= DELTA and abs(self.extremum_x - x) <= SIGMA


class Fecx:
    """
        Fecx = e^(c*x), 0 <= x <= 10.23

        max(y) = e^(c*x), x = 10.23
        """

    def __init__(self, a: float, b: float, c: float, encode_type: EncodeType = None):
        self.a = a
        self.b = b
        self.c = c
        self.extremum_x = b
        self.extremum_y = math.exp(c * b)
        self.encode_type = encode_type
        self.factory = PopulationFactory(self)

    def score(self, x: float):
        return math.exp(self.c * x)

    def decode(self, code):
        decode_func = decode if self.encode_type is EncodeType.GRAY_CODE else decode_bin
        return decode_func(code, self.a, self.b, len(code))

    def encode(self, x, length):
        encode_func = encode if self.encode_type is EncodeType.GRAY_CODE else encode_bin
        return encode_func(x, self.a, self.b, length)

    def estimate(self, chromosome_code):
        x = self.decode(chromosome_code)
        return self.score(x)

    def get_genotype_value(self, chromosome_code):
        x = self.decode(chromosome_code)
        return x

    def get_count_ones(self, chromosome_code):
        return np.count_nonzero(chromosome_code)

    def generate_optimal(self, length):
        gray_code = self.encode(self.extremum_x, length)
        return Chromosome(gray_code, self.extremum_y)

    def get_optimal(self, n, l, p_m, i):
        return self.generate_optimal(l)

    def generate_population(self, n, l):
        return self.factory.generate_population_bit(n, l)

    def check_chromosome_success(self, chromosome: Chromosome):
        x = self.decode(chromosome.code)
        y = chromosome.fitness
        return (self.extremum_y - y) <= DELTA and abs(self.extremum_x - x) <= SIGMA
