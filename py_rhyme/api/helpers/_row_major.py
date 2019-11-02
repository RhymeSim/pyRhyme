from functools import reduce


def _indices_to_id(indices, grid):
    offsets = [
        reduce(lambda x, y: x * y, grid[i+1:], 1) for i in range(len(grid))
    ]

    return sum([ i * o for i, o in zip(indices, offsets) ])
