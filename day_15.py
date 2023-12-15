# %%
import itertools
import re
from collections import defaultdict

import numpy as np
import tqdm
from more_itertools import distinct_permutations as idp

from utilities.collect_data import get_data, get_example_data

day = 15


final_data = get_data(day)

example_data = get_example_data(day)
example_data
# %%
data = example_data


def answer_question_1(data):
    data = data[0].split(",")
    line = data[0]
    scores = []
    for line in data:
        current_val = 0
        for char in line:
            current_val = ((current_val + ord(char)) * 17) % 256
        scores.append(current_val)
    print(scores)
    return np.sum(scores)


answer_question_1(example_data)
# %%
answer_question_1(final_data)


# %%
def answer_question_2(data):
    data = data[0].split(",")
    line = data[0]
    boxes = defaultdict(list)
    for line in data:
        line
        current_val = 0
        splitline = re.split(r"-|=", line)
        for char in splitline[0]:
            current_val = ((current_val + ord(char)) * 17) % 256
        box = current_val
        if re.match(r".*-", line):
            if len(boxes[box]) > 0:
                boxes[box] = [i for i in boxes[box] if i[0] != splitline[0]]
        else:
            if splitline[0] in set([i[0] for i in boxes[box]]):
                boxes[box] = [
                    i if i[0] != splitline[0] else [splitline[0], splitline[1]]
                    for i in boxes[box]
                ]
            else:
                boxes[box].append([splitline[0], splitline[1]])

    strengths = []
    for box, vals in boxes.items():
        for i, item in enumerate(vals):
            strengths.append((int(box) + 1) * (i + 1) * int(item[1]))

    return np.sum(strengths)


answer_question_2(example_data)

# %%
answer_question_2(final_data)
# %%
