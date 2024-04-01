import numpy as np
import matplotlib.pyplot as plt


# function to compute the quality of each individual (permutation)
def compute_quality(permutation):
    # we subtract 1 from the length of the list because on the last position we find the quality
    no_of_queens = len(permutation) - 1

    # we assume maximum quality from the start
    quality = no_of_queens * (no_of_queens - 1) / 2

    for i in range(no_of_queens - 1):
        for j in range(i + 1, no_of_queens):
            # for each queen that attacks each other we decrease the quality by 1
            if abs(i - j) == abs(permutation[i] - permutation[j]):
                quality -= 1

    return quality


# function with returns a list (on the last position is the quality)
def create_individual(no_of_queens):
    # create a random permutation
    individual = np.random.permutation(no_of_queens).tolist()

    # compute the quality of the individual (permutation)
    quality = compute_quality(individual)

    # attach the quality on the last position of the individual
    individual.append(quality)

    return individual


# population representation by points (individual index, quality) - to see the variability in the population
def draw_population(population):
    population_size = len(population)
    # compute the index of the quality
    position_of_quality = len(population[0]) - 1

    # on the x-axis we represent the index of each individual
    x_axis = [i for i in range(population_size)]

    # on the y-axis we represent the quality of each individual
    y_axis = [population[i][position_of_quality] for i in range(population_size)]

    plt.plot(x_axis, y_axis, "gs-", markersize=11)
    plt.show()


# generate the initial population
def generate_initial_population(no_of_queens, population_size):
    # define matrix with all elements 0
    # the matrix will have population_size number of lines (each line = one individual)
    # the matrix will have no_of_queens + 1 number of columns (last column for quality)
    population = np.zeros((population_size, no_of_queens + 1), dtype=int)

    for i in range(population_size):
        # generate the permutation
        population[i] = create_individual(no_of_queens)

    draw_population(population)
    return population


p = generate_initial_population(8, 30)
plt.show()
