import logging
import multiprocessing
import sys
from multiprocessing import Pool
from tqdm.auto import tqdm
import shutil

sys.path.extend(['D:/Korysne/naukma/Genetic_algorithm/Lab_2_v3', 'd'])

import time
from constants import env
from functions import *
from rws import RankLinearRWS
from sus import RankLinearSUS
from plots import *
from program import main, main_noise
from excel import save_avg_to_excel

release_sm = [RankLinearSUS(b=1.5), RankLinearSUS(b=1.6), RankLinearSUS(b=1.8), RankLinearRWS(b=1.9),
              RankLinearRWS(b=1.5), RankLinearRWS(b=1.6), RankLinearRWS(b=1.8), RankLinearSUS(b=1.9)]

testing_sm = [RankLinearSUS(b=1.5), RankLinearRWS(b=1.5)]

selection_methods = testing_sm if env == "test" else release_sm

p_arr = [(0, 0), (0, 1), (0.0001, 0), (0.0001, 1)]

release_functions = [
    (FHD(delta=100), selection_methods, "FHD", N, 10, p_arr, [EncodeType.BINARY]),

    (Fx2(a=0, b=10.23), selection_methods, "Fx2", N, 10, p_arr, [EncodeType.GRAY_CODE, EncodeType.BINARY]),

    (F5122subx2(a=-5.11, b=5.12), selection_methods, "F5122subx2", N, 10,
     p_arr, [EncodeType.GRAY_CODE, EncodeType.BINARY]),

    (Fecx(a=0, b=10.23, c=0.25, encode_type=EncodeType.GRAY_CODE), selection_methods, "Fecx_025", N, 10,
     p_arr, [EncodeType.GRAY_CODE, EncodeType.BINARY])
]

test_functions = [
    (FHD(delta=100), selection_methods, "FHD", N, 10, p_arr, [EncodeType.BINARY]),
    (Fx2(a=0, b=10.23), selection_methods, "Fx2", N, 10, p_arr, [EncodeType.GRAY_CODE, EncodeType.BINARY]),
    (F5122subx2(a=-5.11, b=5.12), selection_methods, "F5122subx2", N, 10,
     p_arr, [EncodeType.GRAY_CODE, EncodeType.BINARY]),
]

functions = test_functions if env == "test" else release_functions


def main_args(args, pool):
    return main(fitness_function=args[0], selection_functions=args[1], file_name=args[2], n=args[3],
                l=args[4], p_arr=args[5], encode_types=args[6], pool=pool)


if __name__ == "__main__":
    p_start = time.time()

    func_runs = {}
    noise_runs = {}

    if os.path.exists('data'):
        shutil.rmtree(os.path.join(os.path.dirname(__file__), 'data'))

    with Pool(8) as p:
        for func in tqdm(functions, desc='Functions', position=0):
            func_runs[func[2]] = main_args(func, p)

        noise_runs["FConst"] = main_noise(selection_methods, p)

        save_avg_to_excel(func_runs, noise_runs)

        p_end = time.time()
        logging.info("Program calculation (in sec.): " + str((p_end - p_start)))
