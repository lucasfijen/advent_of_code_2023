# %%
from utilities.collect_data import get_data, get_example_data
import numpy as np

import re

day = 11


final_data = get_data(day)

example_data = get_example_data(day)
example_data
# %%
data = example_data
arr = np.array([[i for i in line] for line in example_data])
points = np.array(np.where(arr == "#")).T
points


# %%
def add_pentalties(points, penalty=1):
    """Adds penalty to each empty row in the DF"""
    new_points = points.copy()
    for col in (0, 1):
        range_list = np.arange(new_points[:, col].max())
        pen_list = range_list[np.in1d(range_list, new_points[:, col], invert=True)]
        # Has to happen backwards, otherwise you push points in a range
        # Which it isn't originally in
        for empty_nr in pen_list[::-1]:
            new_points[new_points[:, col] > empty_nr, col] += penalty
    return new_points


penalty_points = add_pentalties(points)
penalty_points


# %%
def get_pairs(points):
    """
    Makes all posible pairs for an array
    note this returns an (N,2,2) shaped matrix,
    where (NPairs, npoints, dimpoint)
    """
    pairs = np.empty((0, 2, 2), dtype=int)
    for i in range(len(points) - 1):
        points_matches = points[i + 1 :, :]
        startpoints = np.repeat(points[i, np.newaxis], points_matches.shape[0], axis=0)
        newpairs = np.stack((startpoints, points_matches), axis=1)
        pairs = np.concatenate((pairs, newpairs), axis=0)
    return pairs


pairs = get_pairs(penalty_points)
pairs


# %%
def handle_question(data, penalty=1):
    arr = np.array([[i for i in line] for line in data])
    points = np.array(np.where(arr == "#")).T
    penalty_points = add_pentalties(points, penalty)
    pairs = get_pairs(penalty_points)

    # Calculate manhattan distance
    return np.abs((pairs[:, 0, :] - pairs[:, 1, :])).sum()


handle_question(example_data)
# %%
handle_question(final_data)

# %%
handle_question(example_data, 99)
# %%
handle_question(example_data, 9)
# %%
# distance is already 1, so need to subtract 1 from the added value
handle_question(final_data, 1000000 - 1)
# %%
