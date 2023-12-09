# %%
from utilities.collect_data import get_data, get_example_data
import numpy as np

import re

day = 9


final_data = get_data(day)

example_data = get_example_data(day)
example_data
# %%
data = example_data
data[0]
# %%
def answer_question1(data):
    answers = []
    for line in data:
        line = np.array(re.findall(r"-?\d+", line), dtype=int)
        numlist = [line[-1],]
        while not (np.all(line == 0) | (line.shape[0] == 0)):
            line = line[1:]-line[:-1]
            numlist.append(line[-1])

        lastval = 0
        for i in numlist[::-1][1:]:
            lastval += i
        answers.append(lastval)
    return np.sum(answers)

answer_question1(example_data)
# %%
answer_question1(final_data)
# %%
def answer_question2(data):
    answers = []
    for line in data:
        line = np.array(re.findall(r"-?\d+", line), dtype=int)
        numlist = [line[0],]
        while not (np.all(line == 0) | (line.shape[0] == 0)):
            line = line[1:]-line[:-1]
            numlist.append(line[0])

        lastval = 0

        for i in numlist[::-1][1:]:
            lastval = i - lastval
        answers.append(lastval)
    return np.sum(answers)
answer_question2(example_data)
# %%
answer_question2(final_data)
# %%
