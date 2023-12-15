# %%
from utilities.collect_data import get_data, get_example_data
import numpy as np
import itertools
from more_itertools import distinct_permutations as idp
import re
import tqdm

day = 13


final_data = get_data(day)

example_data = get_example_data(day)
example_data

# %%


def dataloader(data):
    landscapes = []
    current_landscape = []
    for line in data:
        if line == "":
            landscapes.append(np.array(current_landscape))
            current_landscape = []
        else:
            current_landscape.append([i for i in line])

    if len(current_landscape) > 0:
        landscapes.append(np.array(current_landscape))
    return landscapes


data = dataloader(example_data)
data


# %%
# horizontal check
def calculate_mirror_score(df, multiplier, q2):
    for i in range(1, df.shape[0]):
        lookrange = np.min((i, df.shape[0] - i))
        top = df[i - lookrange : i, :]
        below = df[i : i + lookrange, :][::-1, :]
        if q2:
            if ((~(top == below)) * 1).sum() == 1:
                return i * multiplier
        else:
            if (top == below).all():
                return i * multiplier
    return 0


def perform_scoring(df, q2):
    colres = calculate_mirror_score(df, 100, q2)
    if colres > 0:
        return colres
    return calculate_mirror_score(df.T, 1, q2)


def answer_question(data, q2=False):
    data = dataloader(data)
    scores = []
    for df in data:
        scores.append(perform_scoring(df, q2))
    if (np.array(scores) == 0).any():
        print("Found a zero in scores")
    return np.sum(scores)


answer_question(example_data)
# %%
answer_question(final_data)
# %%

answer_question(example_data, q2=True)
# %%

answer_question(final_data, q2=True)
# %%
