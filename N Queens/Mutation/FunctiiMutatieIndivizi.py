import numpy as np


# ------------ Binary Arrays ------------

# bit flip mutation
def bit_flip_mutation(initial_value):
    mutation_result = not initial_value
    return int(mutation_result)


# ------------ Integer Numbers Arrays ------------

# randomly resetting - resets the value, randomly choosing it from the interval
def random_resetting_mutation(lower_limit, upper_limit):
    mutation_result = np.random.randint(lower_limit, upper_limit)
    return mutation_result


# "creep" mutation - slightly changes the initial value (very small change)
def creep_mutation(initial_value, lower_limit, upper_limit):
    # generating +1 or -1
    sign = np.random.choice([-1, 1])

    mutation_result = initial_value + sign

    if mutation_result > upper_limit:
        mutation_result = upper_limit

    if mutation_result < lower_limit:
        mutation_result = lower_limit

    return mutation_result


# ------------ Real Numbers Arrays ------------

# Uniform Mutation - resets the value, randomly choosing it from the interval
def uniform_mutation(lower_limit, upper_limit):
    mutation_result = np.random.uniform(lower_limit, upper_limit)
    return mutation_result


# non-uniform mutation - slightly changes the initial value with a random number
def non_uniform_mutation(initial_value, max_creep_value, lower_limit, upper_limit):
    # generate noise
    random_factor = np.random.normal(-max_creep_value, max_creep_value)
    mutation_result = initial_value + random_factor

    if mutation_result > upper_limit:
        mutation_result = upper_limit

    if mutation_result < lower_limit:
        mutation_result = lower_limit

    return mutation_result


# ------------ Permutations ------------

# Inversion Mutation - reverses a randomly selected portion of the permutation

# Example:
# poz_1 = 2
# poz_2 = 6
# Initial permutation = 4 3 !6 5 7 2 1! 8
# Result =              4 3 !1 2 7 5 6! 8
# Note: the "!" encapsulates the changed members
# Note: due to being python arrays, the position in the permutation starts from 0

def inversion_mutation(initial_permutation):
    # Find out the length of the permutation
    permutation_size = len(initial_permutation)

    # generates the positions for the inversion
    poz_1 = np.random.randint(0, permutation_size - 1)
    poz_2 = np.random.randint(poz_1 + 1, permutation_size)

    # Copy the initial permutation
    mutation_result = initial_permutation.copy()

    # And reverse the segment denoted by poz_1 and poz_2
    mutation_result[poz_1:poz_2 + 1] = initial_permutation[poz_2:poz_1 - 1:-1]

    return mutation_result


# Swap Mutation - swaps 2 random values of the permutation

# Example:
# poz_1 = 2
# poz_2 = 6
# Initial permutation = 4 3 6 5 7 2 1 8
# Result =              4 3 1 5 7 2 6 8
# Note: due to being python arrays, the position in the permutation starts from 0

def swap_mutation(initial_permutation):
    # Find out the length of the permutation
    permutation_size = len(initial_permutation)

    # generates the positions for the swap
    poz_1 = np.random.randint(0, permutation_size - 1)
    poz_2 = np.random.randint(poz_1 + 1, permutation_size)

    mutation_result = initial_permutation.copy()
    mutation_result[poz_1] = initial_permutation[poz_2]
    mutation_result[poz_2] = initial_permutation[poz_1]

    return mutation_result


# Insertion Mutation - chooses 2 random positions and:
# 1. copies the element from position 2 in front of position 1
# 2. copies the elements which were initially between the 2 positions after

# Example:
# poz_1 = 2
# poz_2 = 6
# Initial permutation = 4 3 !6 5 7 2 1! 8
    # Result =          4 3 !6 1 5 7 2! 8
# Note: the "!" encapsulates the changed members
# Note: due to being python arrays, the position in the permutation starts from 0

def insertion_mutation(initial_permutation):
    # Find out the length of the permutation
    permutation_size = len(initial_permutation)

    # generates the positions for the swap
    poz_1 = np.random.randint(0, permutation_size - 1)
    poz_2 = np.random.randint(poz_1 + 1, permutation_size)
    print(poz_1, poz_2)

    mutation_result = initial_permutation.copy()
    mutation_result[poz_1 + 1] = initial_permutation[poz_2]

    for i in range(poz_2 - poz_1 - 1):
        mutation_result[poz_1 + i + 2] = initial_permutation[poz_1 + i + 1]

    return mutation_result
