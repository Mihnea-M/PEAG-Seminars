import matplotlib.pyplot as plt
import numpy as np


# Compute the quality of each individual
def compute_quality(individual, contiguity_matrix):
    val = 0
    no_of_cities = len(individual)

    for i in range(no_of_cities - 1):
        # we add the cost of the distance between current and next city
        val = val + contiguity_matrix[individual[i]][individual[i + 1]]

    # we also need to add the distance between the last and first city
    val = val + contiguity_matrix[individual[0]][individual[no_of_cities - 1]]

    return 100 / val


# population representation by points (individual index, quality) - to see the variability in the population
def draw_pop_graph(qualities):
    population_size = len(qualities)

    # on the x-axis we represent the index of each individual
    x_axis = [i for i in range(population_size)]

    # on the y-axis we represent the quality of each individual
    y_axis = [qualities[i] for i in range(population_size)]

    plt.plot(x_axis, y_axis, "gs-", markersize=11)
    plt.show()


# generate initial population
def generate_initial_population(input_file_name, pop_size):
    # read the data from the file nxn of costs
    contiguity_matrix = np.genfromtxt(input_file_name)

    # no_of_cities = the dimension of the problem
    no_of_cities = len(contiguity_matrix)

    # define a population matrix where each line is an individual
    pop = np.zeros((pop_size, no_of_cities), dtype=int)

    # remember the quality of each individual in a separate list
    qualities = np.zeros(pop_size, dtype=float)

    for i in range(pop_size):
        # generate the permutation candidate with no_of_cities elements
        pop[i] = np.random.permutation(no_of_cities)

        # evaluate each individual
        qualities[i] = compute_quality(pop[i], contiguity_matrix)

    draw_pop_graph(qualities)
    # returns a list out of which the first element is the population and the second one the list of qualities
    return [pop, qualities]


[p, v] = generate_initial_population("costuri.txt", 30)
