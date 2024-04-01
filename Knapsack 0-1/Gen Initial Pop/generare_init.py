import numpy as np
import matplotlib.pyplot as plt


def read_from_file(file_name):
    data = np.genfromtxt(file_name)
    return data


# check the feasibility of the candidate
def check_feasible(candidate, costs, max_capacity):
    total_cost = 0
    for i in range(len(costs)):
        total_cost += costs[i] * candidate[i]
    return total_cost <= max_capacity


# compute the quality of the candidate
def compute_quality(candidate, values):
    total_value = 0
    for i in range(len(values)):
        total_value += values[i] * candidate[i]
    return total_value


# population representation by points (individual index, quality) - to see the variability in the population
def draw_pop(population):
    population_size = len(population)
    position_of_quality = len(population[0]) - 1

    # on the x-axis we remember the index of each individual
    x_axis = [i for i in range(population_size)]

    # on the y-axis we remember the quality of each individual which we can find on the last position
    y_axis = [population[i][position_of_quality] for i in range(population_size)]
    plt.plot(x_axis, y_axis, "gs-", markersize=11)
    plt.show()


# generate the initial population
# I: fc, fv - the name of the files cost, value
#    max - the maximum capacity
#    dim - the number of individuals from the population
# O: pop - initial population

def generate_initial_population(costs_file, values_file, max_capacity, population_size):
    # read the data from the files cost.txt and value.txt
    costs = read_from_file(costs_file)
    values = read_from_file(values_file)

    # individual_size = the dimension of the problem
    individual_size = len(costs)

    # works with the population as the list with dim elements - lists with individual_size+1 individuals
    population = []

    for i in range(population_size):
        done = False
        candidate = None
        while not done:
            # generate the candidate with elements 0, 1
            candidate = np.random.randint(0, 2, individual_size).tolist()
            done = check_feasible(candidate, costs, max_capacity)

        # compute the quality of the feasible candidate
        quality = compute_quality(candidate, values)

        # add the quality
        candidate.append(quality)

        # add the candidate to the population
        population += [candidate]

    draw_pop(population)
    return population


# for testing
pop = generate_initial_population("cost.txt", "valoare.txt", 50, 10)
