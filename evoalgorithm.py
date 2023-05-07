from pressure_stats import PressureStats
from noise_stats import NoiseStats
from selection_diff_stats import SelectionDiffStats
from reproduction_stats import ReproductionStats
from run import Run
from functions import *
from constants import *
import logging


class EvoAlgorithm:
    def __init__(
            self,
            initial_population: Population,
            selection_function,
            fitness_function,
            optimal,
            n,
            l
    ):
        self.population: Population = initial_population
        self.selection_function = selection_function
        self.iteration = 0
        self.pressure_stats = PressureStats()
        self.reproduction_stats = ReproductionStats()
        self.selection_diff_stats = SelectionDiffStats()
        self.best = self.population.genotypes_list[0]

        self.pressure_stats.f_best.append(self.population.get_max_fitness())
        self.fitness_function = fitness_function
        self.optimal = optimal
        num_of_best = self.population.get_chromosomes_copies_counts([list(self.optimal.code)])
        self.pressure_stats.num_of_best.append(
            num_of_best
        )
        self.n = n
        self.l = l

        self.optimal_x = self.fitness_function.get_genotype_value(self.optimal.code)
        self.optimal_genotype = self.fitness_function.estimate(self.optimal.code)

    def run(self, run, iterations_to_plot, file_name, encode_type, p_m, p_c):
        self.iteration = 0
        avg_fitness_list = []
        std_fitness_list = []
        convergent = self.population.estimate_convergence()

        # Stop condition
        # if convergent percentage is too big depending on mutation param
        # or iterations exceeds limit
        while not convergent and self.iteration < G:
            logging.debug(f"Iteration {self.iteration} with {self.selection_function.name}")
            # show stats
            if self.iteration < iterations_to_plot:
                if self.fitness_function.__class__.__name__ != 'FHD':
                    self.population.print_phenotypes_distribution(
                        encode_type,
                        p_m,
                        p_c,
                        self.selection_function.name,
                        run + 1,
                        self.iteration + 1,
                        self.fitness_function,
                        file_name,
                        self.optimal_x
                    )
                self.population.print_genotypes_distribution(
                    encode_type,
                    p_m,
                    p_c,
                    self.selection_function.name,
                    run + 1,
                    self.iteration + 1,
                    file_name,
                    self.optimal_genotype
                )
                self.population.print_bit_ones_distribution(
                    encode_type,
                    p_m,
                    p_c,
                    self.selection_function.name,
                    run + 1,
                    self.iteration + 1,
                    self.fitness_function,
                    file_name,
                )

            # stats before selection
            f_parents_pool = self.population.get_mean_fitness()
            avg_fitness_list.append(f_parents_pool)
            f_std = self.population.get_fitness_std()
            std_fitness_list.append(f_std)

            # selection process
            unique_chromosomes = self.population.get_unique()

            # select some individuals
            self.population = self.selection_function.select(self.population)

            unique_chromosomes_after = self.population.get_unique()

            # stats
            fs = self.population.get_mean_fitness()
            self.selection_diff_stats.s_list.append(fs - f_parents_pool)

            best_genotypes = self.population.get_best_genotypes()
            num_of_best = self.population.get_chromosomes_copies_counts(best_genotypes)
            num_of_optimal = self.population.get_chromosomes_copies_counts([list(self.optimal.code)])

            self.reproduction_stats.rr_list.append(
                len(unique_chromosomes_after) / len(unique_chromosomes)
            )
            self.reproduction_stats.best_rr_list.append(
                num_of_optimal / len(self.population.chromosomes)
            )
            self.pressure_stats.intensities.append(
                PressureStats.calculate_intensity(
                    fs, f_parents_pool, f_std
                )
            )
            self.pressure_stats.f_best.append(self.population.get_max_fitness())

            self.pressure_stats.num_of_best.append(num_of_best)

            self.iteration += 1

            self.pressure_stats.grs.append(
                PressureStats.calculate_growth_rate(
                    self.pressure_stats.num_of_best[self.iteration],
                    self.pressure_stats.num_of_best[self.iteration - 1],
                    self.pressure_stats.f_best[self.iteration],
                    self.pressure_stats.f_best[self.iteration - 1],
                )
            )

            if num_of_best >= N / 2 and self.pressure_stats.grl is None:
                # TODO check it
                self.pressure_stats.grli = self.iteration
                self.pressure_stats.grl = self.pressure_stats.grs[-1]

            # one-point crossover
            self.population.crossover(self.fitness_function, n=self.n, l=self.l)

            # mutate
            self.population.mutate(self.fitness_function)

            # update convergent value
            convergent = self.population.estimate_convergence()

        # stats
        if convergent:
            self.pressure_stats.NI = self.iteration

        avg_fitness_list.append(self.population.get_mean_fitness())
        std_fitness_list.append(self.population.get_fitness_std())

        if iterations_to_plot != 0:
            if self.fitness_function.__class__.__name__ != 'FHD':
                self.population.print_phenotypes_distribution(
                    encode_type,
                    p_m,
                    p_c,
                    self.selection_function.name,
                    run + 1,
                    self.iteration,
                    self.fitness_function,
                    file_name,
                    self.optimal_x
                )
            self.population.print_genotypes_distribution(
                encode_type,
                p_m,
                p_c,
                self.selection_function.name,
                run + 1,
                self.iteration,
                file_name,
                self.optimal_genotype
            )
            self.population.print_bit_ones_distribution(
                encode_type,
                p_m,
                p_c,
                self.selection_function.name,
                run + 1,
                self.iteration,
                self.fitness_function,
                file_name,
            )

        self.pressure_stats.takeover_time = self.iteration
        self.pressure_stats.f_found = self.population.get_max_fitness()
        self.pressure_stats.f_avg = self.population.get_mean_fitness()
        self.pressure_stats.calculate()
        self.reproduction_stats.calculate()
        self.selection_diff_stats.calculate()

        # calc stats based on success condition
        is_successful = self.check_success() if convergent else False
        return Run(
            avg_fitness_list,
            std_fitness_list,
            self.pressure_stats,
            self.reproduction_stats,
            self.selection_diff_stats,
            None,
            is_successful,
        )

    def check_success(self):
        ff_name = self.fitness_function.__class__.__name__
        if ff_name == "Fconst" or ff_name == "FHD":
            if self.population.p_m == 0:
                return (
                        self.population.get_chromosomes_copies_counts([list(self.optimal.code)])
                        == N
                )
            else:
                return (
                        self.population.estimate_convergence() and
                        self.population.get_chromosomes_copies_counts(
                            [list(self.optimal.code)]) >= 0.9 * N
                )
        else:
            return any(
                [
                    self.fitness_function.check_chromosome_success(p)
                    for p in self.population.chromosomes
                ]
            )

    def calculate_noise(self, sf, i):
        iteration = 0

        while not self.population.estimate_convergence() and iteration < G:
            # selection process
            unique_chromosomes = self.population.get_unique()

            self.population = sf.select(self.population)

            unique_chromosomes_after = self.population.get_unique()

            num_of_optimal = self.population.get_chromosomes_copies_counts([list(self.optimal.code)])

            self.reproduction_stats.rr_list.append(
                len(unique_chromosomes_after) / len(unique_chromosomes)
            )
            self.reproduction_stats.best_rr_list.append(
                num_of_optimal / len(self.population.chromosomes)
            )

            iteration += 1

        ns = NoiseStats()

        ns.reproduction_stats = self.reproduction_stats
        self.reproduction_stats.calculate()

        if self.population.estimate_convergence():
            ns.NI = iteration
            ns.conv_to = self.population.chromosomes[0].code[0]

        return ns
