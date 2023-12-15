# %%
from utilities.collect_data import get_data, get_example_data
import numpy as np
import itertools
from more_itertools import distinct_permutations as idp
import re
import tqdm

day = 14


final_data = get_data(day)

example_data = get_example_data(day)
example_data
# %%
data = example_data


def answer_question_1(data):
    data = np.array([[i for i in j] for j in data])

    # Reversed rows for scoring, starting with
    # 10 in example to 1
    scorerows = np.arange(data.shape[0])[::-1] + 1
    splitvals = np.array(np.where(data == "#"))
    splitvals = splitvals[:, splitvals[0, :].argsort()]
    # Binary_data will be used to quickly sum amount of occurences
    # Prevents lookup every time
    binary_data = (data == "O") * 1
    score = 0
    for col in range(data.shape[1]):
        lastrow = 0
        for row in splitvals[0, splitvals[1, :] == col]:
            # Get amount of stones in section
            amount = binary_data[lastrow:row, col].sum()
            # Move all of em to first rows
            score += scorerows[lastrow : lastrow + amount].sum()
            lastrow = row + 1
        row = data.shape[0]
        amount = binary_data[lastrow:row, col].sum()
        # Move all of em to first rows
        score += scorerows[lastrow : lastrow + amount].sum()
    return score


# %%
answer_question_1(example_data)
# %%
answer_question_1(final_data)
# %%
# Question 2 ideas:

# Add a populate in new zeros matrix where the blocks become 1
# Rotate the binary,
# Rotate the stationary, do that once 4 times and store

# Run 1000 long, might work


def answer_question_2(data, iterations):
    data = np.array([[i for i in j] for j in data])

    # Reversed rows for scoring, starting with
    # 10 in example to 1
    scorerows = np.arange(data.shape[0])[::-1] + 1
    matrices = [np.rot90(data, i, (1, 0)) for i in range(4)]
    all_splitvals = [np.array(np.where(matrix == "#")) for matrix in matrices]
    all_splitvals = [i[:, i[0, :].argsort()] for i in all_splitvals]
    shapes = [matrix.shape for matrix in matrices]
    binary_data = (data == "O") * 1
    scores = []
    for iter in tqdm.trange(iterations):
        for i in range(4):
            splitvals = all_splitvals[i]
            shape = shapes[i]
            new_binary = np.zeros(shape, dtype=int)
            # Binary_data will be used to quickly sum amount of occurences
            # Prevents lookup every time
            for col in range(shape[1]):
                lastrow = 0
                for row in splitvals[0, splitvals[1, :] == col]:
                    # Get amount of stones in section
                    amount = binary_data[lastrow:row, col].sum()
                    # place new ones on empty matrix
                    new_binary[lastrow : lastrow + amount, col] = 1
                    lastrow = row + 1

                # also perform onto end of df
                amount = binary_data[lastrow:, col].sum()
                new_binary[lastrow : lastrow + amount, col] = 1
            binary_data = np.rot90(new_binary, 1, (1, 0))

        score = (binary_data * scorerows).sum()
        scores.append(score)
        if score in set(scores[:-1]):
            print(np.where(np.array(scores) == score))
            print(iter)
            if iter > ((iter - 92) % 72) + 92:
                print(score, scores[((iter - 92) % 72) + 92])

    return scores


answer_question_2(example_data, 3)
# %%
scores = answer_question_2(final_data, 200)
scores
# %%
iter = 1000000000 + 1
score = scores[(iter - 92) % 72 + 92]
score
# %%
164 - 92
# %%
# Tried answers:
# loop 1000: 89590
# Loop 10000: 89590
# %%
(164 - 92) % 72 + 92
# %%
# loop 1000000: 89578
