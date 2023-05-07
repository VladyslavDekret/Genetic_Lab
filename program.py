from tqdm.auto import tqdm
import numpy as np

from functions import Fconst
from coding import EncodeType
from constants import MAX_RUNS, ITERATIONS_TO_PLOT, RUNS_TO_PLOT
from run import Run
from runs_stats import RunsStats
from evoalgorithm import EvoAlgorithm
from population import Population
from excel import save_to_excel, save_noise_to_excel
from plots import *
import time
import logging
import string

logging.basicConfig(filename='logs/run.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


def save_run_plots(encode_type, p_m, p_c, sf_name, run, iteration, file_name):
    save_line_plot(
        encode_type,
        p_m,
        p_c,
        sf_name,
        run.avg_fitness_list,
        "f_avg" + str(iteration + 1),
        "f avg",
        iteration + 1,
        file_name,
    )
    save_line_plot(
        encode_type,
        p_m,
        p_c,
        sf_name,
        run.pressure_stats.f_best,
        "f_best" + str(iteration + 1),
        "f best",
        iteration + 1,
        file_name,
        (min(run.pressure_stats.f_best) - 5, max(run.pressure_stats.f_best) + 5)
    )
    save_line_plot(
        encode_type,
        p_m,
        p_c,
        sf_name,
        run.std_fitness_list,
        "f_std" + str(iteration + 1),
        "f std",
        iteration + 1,
        file_name
    )
    save_line_plot(
        encode_type,
        p_m,
        p_c,
        sf_name,
        run.pressure_stats.intensities,
        "intensity" + str(iteration + 1),
        "intensity",
        iteration + 1,
        file_name,
        (-0.1, 1.1)
    )
    save_line_plot(
        encode_type,
        p_m,
        p_c,
        sf_name,
        run.selection_diff_stats.s_list,
        "selection_diff" + str(iteration + 1),
        "selection difference",
        iteration + 1,
        file_name
    )
    save_lines_plot(
        encode_type,
        p_m,
        p_c,
        sf_name,
        [run.pressure_stats.intensities, run.selection_diff_stats.s_list / np.max(run.selection_diff_stats.s_list)],
        ["Intensity", "EvoAlgorithm diff"],
        "intensity_and_sel_diff" + str(iteration + 1),
        "Intensity + EvoAlgorithm diff",
        iteration + 1,
        file_name,
        (-0.1, 1.1)
    )
    save_line_plot(
        encode_type,
        p_m,
        p_c,
        sf_name,
        run.pressure_stats.grs,
        "gr" + str(iteration + 1),
        "growth rate",
        iteration + 1,
        file_name
    )
    save_lines_plot(
        encode_type,
        p_m,
        p_c,
        sf_name,
        [
            run.reproduction_stats.rr_list,
            [1 - rr for rr in run.reproduction_stats.rr_list],
        ],
        ["Reproduction rate", "Loss of diversity"],
        "repro_rate_and_loss_of_diversity" + str(iteration + 1),
        "Reproduction rate + Loss of diversity",
        iteration + 1,
        file_name,
        (-0.1, 1.1)
    )
    save_line_plot(
        encode_type,
        p_m,
        p_c,
        sf_name,
        run.reproduction_stats.best_rr_list,
        "best_rr" + str(iteration + 1),
        "best chromosome rate",
        iteration + 1,
        file_name,
        (-0.1, 1.1)
    )


def main(fitness_function, selection_functions: [], file_name, n, l, p_arr, encode_types, pool):
    p_start = time.time()
    runs_dict = {}
    ff_name = fitness_function.__class__.__name__

    for encode_type in encode_types:
        fitness_function.encode_type = encode_type

        p = [fitness_function.generate_population(n=n, l=l) for _ in range(0, MAX_RUNS)]

        for j, (p_m, p_c) in tqdm(enumerate(p_arr), desc=f'{fitness_function.__class__.__name__} loop', leave=False,
                                  position=1, total=len(p_arr)):

            get_run_name = lambda sf_name: f'{sf_name} {encode_type.value} {f"p_m {p_m}" if p_m != 0 else ""} {f"p_c {p_c}" if p_c != 0 else ""}'

            for selection_function in selection_functions:
                runs_dict[get_run_name(selection_function.name)] = RunsStats()

            all_runs_args = [(selection_functions, fitness_function, n, l, p_m, i, encode_type, p_c,
                              p[i], file_name) for i in range(0, MAX_RUNS)]

            for results in pool.starmap(run_algo, tqdm(all_runs_args, total=len(all_runs_args),
                                                       desc=f'{fitness_function.__class__.__name__} - p_m {p_m} p_c {p_c} loop',
                                                       position=1, leave=False)):
                for sf_name, run in results:
                    runs_dict[get_run_name(sf_name)].runs.append(run)

            p_end = time.time()
            logging.info("Program " + file_name + " calculation (in sec.): " + str((p_end - p_start)))

            for selection_function in selection_functions:
                runs_dict[get_run_name(selection_function.name)].calculate()

            save_to_excel(runs_dict, file_name if file_name is not None else ff_name, encode_type, p_m, p_c, p[0])

            p_end_stats = time.time()
            logging.info("Program " + file_name + " stats calculation (in sec.): " + str((p_end_stats - p_end)))

    return runs_dict


def run_algo(selection_functions, fitness_function, n, l, p_m, i, encode_type, p_c, p, file_name):
    results = []

    population = p.__copy__()
    population.p_m = p_m
    population.p_c = p_c

    for sel_func in selection_functions:
        sf_name = sel_func.name

        optimal = fitness_function.get_optimal(n=n, l=l, p_m=p_m, i=i)

        iterations_to_plot = ITERATIONS_TO_PLOT if RUNS_TO_PLOT > i else 0
        current_run = EvoAlgorithm(
            population.__copy__(), sel_func, fitness_function, optimal, n, l
        ).run(run=i, encode_type=encode_type, p_m=p_m, p_c=p_c, iterations_to_plot=iterations_to_plot, file_name=file_name)

        if RUNS_TO_PLOT > i:
            save_run_plots(encode_type, p_m, p_c, sf_name, current_run, i, file_name)

        results.append((sf_name, current_run))

    return results


def main_noise(selection_functions: [], pool):
    p_start = time.time()
    runs_dict = {}
    file_name = "FConst"

    for selection_function in selection_functions:
        runs_dict[selection_function.name] = RunsStats()

    all_runs_args = [(selection_functions, i) for i in range(0, MAX_RUNS)]

    for results in pool.starmap(run_noise_algo, tqdm(all_runs_args, total=len(all_runs_args),
                                                     desc=f'{file_name} loop',
                                                     position=2, leave=False)):
        for sf_name, run in results:
            runs_dict[sf_name].runs.append(run)

    p_end = time.time()
    logging.info("Noise " + file_name + " calculation (in sec.): " + str((p_end - p_start)))

    for selection_function in selection_functions:
        runs_dict[selection_function.name].calculate_noise_stats()

    p_end_stats = time.time()
    logging.info("Noise " + file_name + " stats calculation (in sec.): " + str((p_end_stats - p_end)))

    save_noise_to_excel(runs_dict, file_name)

    return runs_dict


def run_noise_algo(selection_functions, i):
    results = []

    pop = Fconst().generate_population(N, 100)

    for selection_function in selection_functions:
        sf_name = selection_function.name

        ns = EvoAlgorithm(
            pop.__copy__(), selection_function, Fconst(), pop.chromosomes[0], N, 100
        ).calculate_noise(selection_function, i)

        results.append((sf_name, ns))
    return results
