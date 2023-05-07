import os
import random

import numpy as np
import seaborn as sns
from statistics import mean
import matplotlib.pyplot as plt

from constants import N
from chromosome import Chromosome


class Population:
    def __init__(self, chromosomes, p_m=0, p_c=0):
        self.chromosomes = chromosomes
        self.fitness_list = [chromosome.fitness for chromosome in self.chromosomes]
        self.genotypes_list = [list(x.code) for x in self.chromosomes]
        self.p_m = p_m
        self.p_c = p_c
        self.total_key = N + 1

    def print_genotypes_distribution(self, encode_type,
                                     p_m,
                                     p_c, func_name, run, iteration, file_name, optimal):

        path = "data/Report" + "/" + str(
            N) + "/" + file_name + "/" + encode_type.value + "/" + f"p_m_{p_m}" + f"__p_c_{p_c}" + "/" + func_name + "/" + str(
            run) + "/" + "genotypes"

        if not os.path.exists(path):
            os.makedirs(path)

        if optimal == 0:
            optimal = 11

        ax = sns.displot(self.fitness_list)
        ax.set(title='F(X) distribution', xlabel='F(X)', ylabel='Count')
        plt.ylim(0, len(self.fitness_list) * 1.1)
        plt.xlim(0, optimal * 1.1)
        plt.savefig(path + "/" + str(iteration) + ".png")
        plt.close()

    def print_phenotypes_distribution(
            self, encode_type,
            p_m,
            p_c, func_name, run, iteration, fitness_func, file_name, optimal
    ):
        path = "data/Report" + "/" + str(
            N) + "/" + file_name + "/" + encode_type.value + "/" + f"p_m_{p_m}" + f"__p_c_{p_c}" + "/" + func_name + "/" + str(
            run) + "/" + "phenotypes"

        if not os.path.exists(path):
            os.makedirs(path)

        x_list = [fitness_func.decode(code) for code in self.genotypes_list]

        if optimal == 0:
            optimal = 11

        ax = sns.displot(x_list)
        ax.set(title='X distribution', xlabel='x', ylabel='Count')
        plt.ylim(0, len(x_list) * 1.1)
        plt.xlim(0, optimal * 1.1)
        plt.savefig(path + "/" + str(iteration) + ".png")
        plt.close()

    def print_bit_ones_distribution(
            self, encode_type,
            p_m,
            p_c, func_name, run, iteration, fitness_func, file_name
    ):
        path = "data/Report" + "/" + str(
            N) + "/" + file_name + "/" + encode_type.value + "/" + f"p_m_{p_m}" + f"__p_c_{p_c}" + "/" + func_name + "/" + str(
            run) + "/" + "bit_ones"

        if not os.path.exists(path):
            os.makedirs(path)

        x_list = [fitness_func.get_count_ones(chromosome.code) for chromosome in self.chromosomes]
        ax = sns.displot(x_list)
        ax.set(title='1 bits distribution', xlabel='Number of bits with 1', ylabel='Count')
        plt.ylim(0, len(x_list) * 1.1)
        plt.xlim(0, len(self.chromosomes[0].code))
        plt.savefig(path + "/" + str(iteration) + ".png")
        plt.close()

    def estimate_convergence(self):
        if self.p_m == 0:
            return self.is_identical
        else:
            return self.is_homogeneous(percentage=99)

    @property
    def is_identical(self) -> bool:
        unique = self.get_unique()
        return len(unique) == 1

    def is_homogeneous(self, percentage: float):
        total = len(self.chromosomes)
        unique = len(self.get_unique())
        difference = total - unique + 1
        pop_percentage = (difference / total) * 100
        return pop_percentage >= percentage

    def crossover(self, fitness_function, n, l):
        if self.p_c == 0:
            return
        chromosome_pairs = list(zip(random.choices(self.chromosomes, weights=[self.p_c] * n, k=n // 2),
                                    random.choices(self.chromosomes, weights=[self.p_c] * n, k=n // 2)))
        new_chromosomes = []
        for chromosome_a, chromosome_b in chromosome_pairs:
            point = random.randrange(l)
            code_a = np.concatenate([chromosome_a.code[:point], chromosome_b.code[point:]]).astype(int)
            code_b = np.concatenate([chromosome_b.code[:point], chromosome_a.code[point:]]).astype(int)
            fitness_a = fitness_function.estimate(code_a)
            fitness_b = fitness_function.estimate(code_b)
            new_chromosomes.append(Chromosome(code=code_a, fitness=fitness_a, key=self.total_key + 1))
            new_chromosomes.append(Chromosome(code=code_a, fitness=fitness_b, key=self.total_key + 2))

        self.total_key += 2
        self.chromosomes = new_chromosomes
        self.update()

    def mutate(self, fitness_function):
        if self.p_m == 0:
            return
        for chromosome in self.chromosomes:
            for i in range(0, len(chromosome.code)):
                if random.random() < self.p_m:
                    chromosome.code[i] = int(not chromosome.code[i])
                    chromosome.fitness = fitness_function.estimate(chromosome.code)
                    chromosome.key = self.total_key + 1

                    self.total_key += 1
        self.update()

    def get_mean_fitness(self):
        return mean(self.fitness_list)

    def get_max_fitness(self):
        return max(self.fitness_list)

    def get_best_genotypes(self) -> list[list[int]]:
        max_fitness = self.get_max_fitness()
        best_genotypes = [
            self.genotypes_list[index]
            for index, fitness_value in enumerate(self.fitness_list)
            if fitness_value == max_fitness
        ]
        return list(np.unique(best_genotypes, axis=0))

    def get_unique(self) -> set:
        return {''.join(map(str, genotype)) for genotype in self.genotypes_list}

    def get_chromosomes_copies_counts(self, genotypes: list[list[int]]) -> int:
        all_genotypes = [''.join(map(str, genotype)) for genotype in self.genotypes_list]
        unique_genotypes = {''.join(map(str, genotype)) for genotype in genotypes}

        copies_count = 0
        for genotype in unique_genotypes:
            copies_count += all_genotypes.count(genotype)
        return copies_count

    def get_fitness_std(self):
        return np.std(self.fitness_list)

    def get_keys_list(self):
        return list([chromosome.key for chromosome in self.chromosomes])

    def update(self):
        self.fitness_list = [chromosome.fitness for chromosome in self.chromosomes]
        self.genotypes_list = [list(x.code) for x in self.chromosomes]

    def update_rws(self, probabilities):
        self.chromosomes = [
            np.random.choice(self.chromosomes, p=probabilities)
            for _ in range(0, len(self.chromosomes))
        ]
        self.update()

    def update_chromosomes(self, chromosomes):
        self.chromosomes = chromosomes
        self.update()

    def __copy__(self):
        return Population(self.chromosomes.copy(), self.p_m, self.p_c)
