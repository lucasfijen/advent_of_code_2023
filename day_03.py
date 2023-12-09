# %%
from utilities.collect_data import get_data, get_example_data
import numpy as np

import re

day = 3


final_data = get_data(day)

example_data = get_example_data(day)
example_data
# %%
np.array([[i for i in j] for j in example_data])


# %%
def process_data(data):
    firstlastline = ["." * (len(data[0]) + 2)]
    extended_df = firstlastline + ["." + i + "." for i in data] + firstlastline
    extended_df

    totalsum = 0

    for row, line in enumerate(data):
        row += 1

        for m in re.finditer(r"\d+", line):
            span = m.span()
            span = [i + 1 for i in span]
            stringaround = (
                extended_df[row - 1][span[0] - 1 : span[1] + 1]
                + extended_df[row][span[0] - 1]
                + extended_df[row][span[1]]
                + extended_df[row + 1][span[0] - 1 : span[1] + 1]
            )
            if re.search(r"[^.]", stringaround) is not None:
                totalsum += int(m.group())
            # print(m)
            # print(m.group())
            # print(stringaround)
            # print(re.search(r"[^.]", stringaround) is not None)
            # print('------------------')
    return totalsum


process_data(example_data)
# %%
process_data(final_data)
# %%

from collections import defaultdict


def handle_matches(line):
    matches = []
    for m in re.finditer(r"\*", line):
        matches.append(m.start())
    return matches


def process_data_2(data):
    firstlastline = ["." * (len(data[0]) + 2)]
    extended_df = firstlastline + ["." + i + "." for i in data] + firstlastline
    extended_df

    starlist = defaultdict(list)

    for row, line in enumerate(data):
        row += 1

        for m in re.finditer(r"\d+", line):
            span = m.span()
            span = [i + 1 for i in span]
            hit = False

            for x in handle_matches(extended_df[row - 1][span[0] - 1 : span[1] + 1]):
                starlist[f"{row-1},{span[0]-1+x}"].append(int(m.group()))

            for x in handle_matches(extended_df[row + 1][span[0] - 1 : span[1] + 1]):
                starlist[f"{row+1},{span[0]-1+x}"].append(int(m.group()))

            if extended_df[row][span[0] - 1] == "*":
                starlist[f"{row},{span[0]-1}"].append(int(m.group()))

            if extended_df[row][span[1]] == "*":
                starlist[f"{row},{span[1]}"].append(int(m.group()))

    totalsum = 0
    for key, val in starlist.items():
        if len(val) == 2:
            totalsum += val[0] * val[1]

    return totalsum


process_data_2(final_data)
# %%
