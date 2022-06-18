import sys
import itertools
global answer
import time


def brute_force(graph):   # naive brute force
    '''

    Args:
        graph: which is the 2d path length matrix

    Returns: optimal path between all the scan locations

    '''
    s = time.time()
    vertex = []
    for i in range(len(graph)):
        if i != 0:
            vertex.append(i)
    # print(vertex)

    min_path = sys.maxsize
    next_permutation = itertools.permutations(vertex)
    # next_permutation = [perm for perm in permutations(vertex)]
    # print(next_permutation)
    for i in next_permutation:
        # print(i)
        current_length = 0
        k = 0
        for j in i:
            current_length += graph[k][j]
            k = j
        current_length += graph[k][0]

        min_path = min(min_path, current_length)

    e = time.time()
    print(f'The time for brute force is {e-s}')
    return min_path


def held_karp(dists):
    """
    Implementation of Held-Karp, an algorithm that solves the Traveling
    Salesman Problem using dynamic programming with memoization.

    Parameters:
        dists: distance matrix

    Returns:
        A tuple, (cost, path).
    """
    s = time.time()
    n = len(dists)

    # Maps each subset of the nodes to the cost to reach that subset, as well
    # as what node it passed before reaching this subset.
    # Node subsets are represented as set bits.
    C = {}

    # Set transition cost from initial state
    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)

    # Iterate subsets of increasing length and store intermediate results
    # in classic dynamic programming manner
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            # Set bits for all nodes in this subset
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            # Find the lowest cost to get to this subset
            for k in subset:
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)

    # We're interested in all bits but the least significant (the start state)
    bits = (2**n - 1) - 1

    # Calculate optimal cost
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)

    # Backtrack to find full path
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    # Add implicit start state
    path.append(0)
    e = time.time()
    print(f'Time for held karp is {e-s}')
    return opt, list(reversed(path)), e-s
