env = "test12"

# Runs: amount of evolutionary algorithms to probe.
MAX_RUNS = 10 if env == "test" else 100

# Iterations to plot
ITERATIONS_TO_PLOT = 5
RUNS_TO_PLOT = 5

# Genotype: amount of genes.
N = 100 if env == "test" else 200

# Termination condition: maximum amount of iterations.
G = 10000 if env == "test" else 10000000

# Selection: exponential parameter for Rank selection.
C = 0.9801

# Operators: rate for Dense mutation / rate for Single-point crossover.
P_M = 0
P_C = 0

# Convergence condition:
SIGMA = DELTA = 0.01
