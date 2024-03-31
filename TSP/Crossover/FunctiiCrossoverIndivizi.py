import numpy as np


# ------------ Binary or integer representation ------------


# one-point crossover
def single_point_crossover(parent_1, parent_2):
    size = len(parent_1)

    # randomly generates the crossover point
    rand_point = np.random.randint(1, size)

    child_1 = [] * (size + 1)
    child_2 = [] * (size + 1)

    # selecting the sequences that create the first child
    child_1[0:rand_point] = parent_1[0:rand_point]
    child_1[rand_point:size] = parent_2[rand_point:size]

    # selecting the sequences that create the second child
    child_2[0:rand_point] = parent_2[0:rand_point]
    child_2[rand_point:size] = parent_1[rand_point:size]

    return child_1, child_2


# Uniform Crossover
def uniform_crossover(parent_1, parent_2):
    size = len(parent_1)
    # initializes children with values of the parents
    child_1 = [] * size
    child_2 = [] * size

    # child construction
    for i in range(size):
        r = np.random.randint(0, 2)

        if r == 0:
            child_1[i] = parent_1[i]
            child_2[i] = parent_2[i]
        else:
            child_1[i] = parent_2[i]
            child_2[i] = parent_1[i]

    return child_1, child_2


# ------------ Permutation representation ------------

# Partially mapped crossover (PMX)
# used in problems with adjancency dependencies
def partially_mapped_crossover(parent_1, parent_2):
    permutation_size = len(parent_1)

    # Generate random positions
    poz_1 = np.random.randint(0, permutation_size - 1)
    poz_2 = np.random.randint(poz_1 + 1, permutation_size)

    child_1 = __pmx_helper__(parent_1, parent_2, poz_1, poz_2)
    child_2 = __pmx_helper__(parent_2, parent_1, poz_1, poz_2)

    return child_1, child_2


# apply PMX on x, y of size n, with recombination/crossover sequence (p1, p2)
def __pmx_helper__(parent_1, parent_2, poz_1, poz_2):
    permutation_size = len(parent_1)
    child = [-1] * permutation_size

    # copy the sequence from between poz_1 and poz_2 from the first parent into the child
    child[poz_1:poz_2 + 1] = parent_1[poz_1:poz_2 + 1]

    # analyze the elements between poz_1 and poz_2 from the second parent
    for i in range(poz_1, poz_2 + 1):
        current_value = parent_2[i]
        if current_value not in child:

            # we check which value from parent 1 occupies the space we need to put our value in
            element_in_parent_1 = parent_1[i]
            # we need to know where we can find that element in the second parent
            pos_in_parent_2 = parent_2.index(element_in_parent_1)

            # if that position doesn't represent an empty space in the child we repeat the process until
            # we find an empty position (marked by -1)
            while child[pos_in_parent_2] != -1:
                element_in_parent_1 = parent_1[pos_in_parent_2]
                pos_in_parent_2 = parent_2.index(element_in_parent_1)

            # when we find the empty space we fill it with our value
            child[pos_in_parent_2] = current_value

    # for the remaining empty values fill them with the values from the second parent
    for i in range(permutation_size):
        if child[i] == -1:
            child[i] = parent_2[i]

    return child


# Order Crossover (OCX)
def order_crossover(parent_1, parent_2):
    permutation_size = len(parent_1)

    # Generate random positions
    poz_1 = np.random.randint(0, permutation_size - 1)
    poz_2 = np.random.randint(poz_1 + 1, permutation_size)

    child_1 = __ocx_helper__(parent_1, parent_2, permutation_size, poz_1, poz_2)
    child_2 = __ocx_helper__(parent_2, parent_1, permutation_size, poz_1, poz_2)

    return child_1, child_2


def __ocx_helper__(parent_1, parent_2, size, poz_1, poz_2):
    # initialize child with -1
    child = [-1] * size

    # copy content from between the positions of parent 1 into child
    child[poz_1: poz_2 + 1] = parent_1[poz_1: poz_2 + 1]

    # create 2 separate indexes to parse through the child and parent
    i_child = (poz_2 + 1) % size
    i_parent = poz_2

    # because we may pass the max size of the arrays we need to add the "% size" to start from the begining
    while -1 in child:
        if parent_2[i_parent] not in child:
            child[i_child] = parent_2[i_parent]
            i_child = (i_child + 1) % size

        i_parent = (i_parent + 1) % size

    return child


# Cycle Crossover (CX)
def cycle_crossover(parent_1, parent_2):
    permutation_size = len(parent_1)
    child_1 = [-1] * permutation_size
    child_2 = [-1] * permutation_size

    # we create a copy of a parent because we want to mark it with -1 when we find a cycle
    copy_parent_1 = parent_1.copy()

    # we also need to remember the cycle number to find out which child gets the cycle:
    # for odd numbered cycles we start by assigning them to the first child
    # for even numbered cycles we start with the second child
    cycle_no = 1

    for i in range(permutation_size):
        # we check for a cycle of size 1
        if parent_1[i] == parent_2[i]:
            child_1[i] = parent_1[i]
            child_2[i] = parent_1[i]
            cycle_no += 1

        # we check if the current element hasn't been part of a marked cycle
        elif copy_parent_1[i] != -1:
            cycle_index = i

            # we need to remember the first element in the cycle, so we know when it ends
            first_in_cycle = copy_parent_1[cycle_index]

            while parent_2[cycle_index] != first_in_cycle:
                # cycle with odd no. => parent 1 in child 1, parent 2 in child 2
                if cycle_no % 2 == 1:
                    child_1[cycle_index] = parent_1[cycle_index]
                    child_2[cycle_index] = parent_2[cycle_index]
                # cycle with even no. => parent 2 in child 1, parent 1 in child 2
                else:
                    child_2[cycle_index] = parent_1[cycle_index]
                    child_1[cycle_index] = parent_2[cycle_index]

                # we mark the element with -1
                copy_parent_1[cycle_index] = -1

                # we move the index to the position denoted by the value we find in the second parent in the first one
                cycle_index = parent_1.index(parent_2[cycle_index])

            # Because the while loop exists 1 step too early we have to repeat the operations
            copy_parent_1[cycle_index] = -1
            if cycle_no % 2 == 1:
                child_1[cycle_index] = parent_1[cycle_index]
                child_2[cycle_index] = parent_2[cycle_index]
            else:
                child_2[cycle_index] = parent_1[cycle_index]
                child_1[cycle_index] = parent_2[cycle_index]

            cycle_no += 1

    return child_1, child_2


# if you want to test the functions uncomment the following lines:
# i = np.random.randint(5, 30)
# p1 = np.random.permutation(i).tolist()
# p2 = np.random.permutation(i).tolist()
# print("Permutation 1 = " + str(p1))
# print("Permutation 2 = " + str(p2))
# c1, c2 = partially_mapped_crossover(p1, p2) # - change with the function name you want to change
# print("Child 1 = " + str(c1))
# print("Child 2 = " + str(c2))


# EDGE CROSSOVER - optional

# construieste tabela muchiilor pentru permutarile x si y de dimensiune n
def constr_tabel(x, y, n):
    # creaza o lista cu n elemente, toate 0
    muchii = [0] * n

    # pentru usurinta, bordeaza x cu ultimul/primul element
    x1 = np.zeros(n + 2, dtype='int')
    x1[1:n + 1] = x[:]
    x1[0] = x[n - 1]
    x1[n + 1] = x[0]

    y1 = np.zeros(n + 2, dtype='int')
    y1[1:n + 1] = y[:]
    y1[0] = y[n - 1]
    y1[n + 1] = y[0]

    for i in range(1, n + 1):
        a = x1[i]
        r = np.where(y == a)
        j = r[0][0] + 1

        # gaseste vecinii lui a in x si y utilizand x1 si y1 si memoreaza ca multimi pentru - si intersectie
        vx = {x1[i - 1], x1[i + 1]}
        vy = {y1[j - 1], y1[j + 1]}
        dx = vx - vy
        dy = vy - vx
        cxy = vx & vy

        # trecem de la set la list
        lcxy = list(cxy)
        dx = list(dx)
        dy = list(dy)

        # lucram cu tip str
        for j in range(len(lcxy)):
            lcxy[j] = str(lcxy[j]) + '+'
        for j in range(len(dx)):
            dx[j] = str(dx[j])
        for j in range(len(dy)):
            dy[j] = str(dy[j])
        muchii[a] = lcxy + list(dx) + list(dy)

    return muchii


# sterge un element dintr-o lista - cu chei unice, daca apare in lista
# altfel, lasa lista nemodficata
def sterge(x, a):
    # cauta aparitia - poate fi doar una
    p = [i for i in range(len(x)) if x[i] == a]
    if len(p):
        del (x[p[0]])
    return x


# alege alela de plasat, daca lp are mai mult de o valoare
def alege(lp, muchii, n):
    dim = len(lp)
    # cauta daca exista in lista muchiilor 'lp[k]+'
    # calculeaza lungimile listelor, in caz ca nu gaseste 'lp[k]'
    lliste = np.zeros(dim)
    gata = 0
    k = 0
    while k < dim and not gata:
        a = str(lp[k]) + '+'
        i = 0
        while i < n and not gata:
            l = muchii[i]
            p = [j for j in range(len(l)) if l[j] == a]
            if len(p):
                gata = 1
                alela = lp[k]
            else:
                p = [j for j in range(len(l)) if l[j] == str(lp[k])]
                i = i + 1
                lliste[k] = len(l)
        if not gata:
            k = k + 1
    if not gata:
        # calculeaza lungimea minima si pentru ce alele se atinge
        x = [j for j in range(dim) if lliste[j] == min(lliste)]
        # alege prima alela de lungime minima
        # daca sunt mai multe, alege-o pe prima
        alela = lp[x[0]]
    return alela


# ECX - Edge crossover
def ECX(x, y, n):
    muchii = constr_tabel(x, y, n)
    # permutarea rezultata
    z = np.zeros(n, dtype='int')
    # alege initial prima alela - varianta:selecteaza aleator ap in 0...n-1
    # lp - lista alelelor posibile
    # ales - vectorul flag al alelelor alese
    ales = np.zeros(n)
    lp = [x[0]]
    for i in range(n):
        print(muchii)
        if len(lp) == 0:
            # alege aleator o alela
            a = np.random.randint(n)
            while ales[a]:
                a = np.random.randint(n)
        else:
            if len(lp) > 1:
                a = alege(lp, muchii, n)
            else:
                a = lp[0]
        # atribuie alela aleasa
        z[i] = a
        ales[a] = 1
        print(a)
        # sterge alela din tabela de muchii
        for k in range(n):
            sterge(muchii[k], str(a))
            sterge(muchii[k], str(a) + '+')
        # alege lista posibilitatilor la urmatorul moment
        lp = [int(muchii[a][i][0]) for i in range(len(muchii[a]))]
    return z


# APEL ECX
# import numpy as np
# import FunctiiCrossoverIndivizi as c
# n=10
# x=np.random.permutation(n)
# y=np.random.permutation(n)
# z=c.ECX(y,x,10)


# ------------ Real value representation ------------


# Arithmetic recombination - new value = alpha * parent_x[i] + (1 - alpha) * parent_y[i]

# Single arithmetic recombination (one element)
def single_arithmetic_crossover(parent_1, parent_2, alpha):
    # randomly generates the element in which the crossover is made
    parent_size = len(parent_1)
    i = np.random.randint(0, parent_size)

    child_1 = parent_1.copy()
    child_2 = parent_2.copy()

    child_1[i] = (alpha * parent_1[i] + (1 - alpha) * parent_2[i])
    child_2[i] = (alpha * parent_2[i] + (1 - alpha) * parent_1[i])

    return child_1, child_2


# Simple arithmetic recombination (from a random element to the last one)
def simple_arithmetic_crossover(parent_1, parent_2, alpha):
    # randomly generates the element from which the crossover is made
    parent_size = len(parent_1)
    i = np.random.randint(0, parent_size)

    child_1 = parent_1.copy()
    child_2 = parent_2.copy()

    for j in range(i, parent_size):
        child_1[j] = (alpha * parent_1[j] + (1 - alpha) * parent_2[j])
        child_2[j] = (alpha * parent_2[j] + (1 - alpha) * parent_1[j])

    return child_1, child_2


# Total arithmetic recombination (all elements are changed)
def crossover_total(parent_1, parent_2, alpha):
    parent_size = len(parent_1)
    child_1 = parent_1.copy()
    child_2 = parent_2.copy()

    for j in range(parent_size):
        child_1[j] = (alpha * parent_1[j] + (1 - alpha) * parent_2[j])
        child_2[j] = (alpha * parent_2[j] + (1 - alpha) * parent_1[j])

    return child_1, child_2
