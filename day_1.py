# %%
from utilities.collect_data import get_data, get_example_data
import numpy as np

import re

day = 1


final_data = get_data(day)

example_data = get_example_data(day)
example_data

example_2_data = get_example_data(day, "_2")


# %%
def process_line(line):
    filterset = re.findall(
        r"(?=(\d))",
        line,
    )
    return int(f"{filterset[0]}{filterset[-1]}")


# %%
def replace_written_numbers(word):
    replace_dict = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    if word in replace_dict:
        return replace_dict[word]
    else:
        return word


def process_2_line(line):
    filterset = re.findall(
        r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line
    )
    filterset = [replace_written_numbers(i) for i in [filterset[0], filterset[-1]]]
    return int(f"".join(filterset))


def handle_all_data(data, allow_written_numbers=False):
    if allow_written_numbers:
        new_data = [process_2_line(i) for i in data]
    else:
        new_data = [process_line(i) for i in data]
    return np.sum(new_data)


print(f"Example result = {handle_all_data(example_data)}")
print(f"final result = {handle_all_data(final_data)}")
# %%

print(f"result second part{handle_all_data(final_data, True)}")
# %%
