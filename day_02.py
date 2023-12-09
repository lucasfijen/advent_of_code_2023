# %%
from utilities.collect_data import get_data, get_example_data
import numpy as np

import re

day = 2


final_data = get_data(day)

example_data = get_example_data(day)
example_data


# %%
def process_line(line):
    game_id, games = re.findall(r"Game (\d*):(.*)", line)[0]

    num_col_combi = re.findall(r" (\d*) (\w*)", games)

    for num, col in num_col_combi:
        if (
            (int(num) > 12)
            and (col == "red")
            or (int(num) > 13)
            and (col == "green")
            or (int(num) > 14)
            and (col == "blue")
        ):
            return 0
    return int(game_id)


def counter_games(codelist):
    return np.sum([process_line(line) for line in codelist])


print(f"the final result of day 2.1 is : {counter_games(example_data)}")
print(f"the final result of day 2.1 is : {counter_games(final_data)}")

from collections import defaultdict


def process_line_2(line):
    game_id, games = re.findall(r"Game (\d*):(.*)", line)[0]
    num_col_combi = re.findall(r" (\d*) (\w*)", games)

    colors = defaultdict(list)
    for num, col in num_col_combi:
        colors[col].append(int(num))
    return np.prod([np.max(i[1]) for i in colors.items()])


def counter_games_2(codelist):
    return np.sum([process_line_2(line) for line in codelist])


counter_games_2(final_data)
