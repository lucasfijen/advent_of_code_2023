# %%
from utilities.collect_data import get_data, get_example_data
import numpy as np
import itertools
from more_itertools import distinct_permutations as idp
import re
import tqdm

day = 12


final_data = get_data(day)

example_data = get_example_data(day)
example_data

# %%


# Old approach i used for question 1, brute force
def calc_options(line, values):
    options = len(re.findall(r"\?", line))
    scores = [int(i) for i in values.split(",")]
    hash_needed = np.sum(scores) - len(re.findall(r"\#", line))

    # Regexpression to check if valid answer/permutation
    regexcheck = f"^\\.*#{{{scores[0]}}}"
    if len(scores) > 1:
        for i in scores[1:]:
            regexcheck += f"\\.+#{{{i}}}"
    regexcheck += "\\.*$"
    # Lets go through all permutations, we need a fixed amount of # so:
    fillstring = "#" * hash_needed + "." * (options - hash_needed)
    perms = set(idp(fillstring))
    valid_options = 0
    for perm in perms:
        poplist = list(perm)
        permstring = re.sub(r"\?", lambda x: poplist.pop(0), line)
        if re.match(regexcheck, permstring):
            valid_options += 1
    return valid_options


def answer_question_1(data):
    data = [i.split(" ") for i in data]
    arrangements = [calc_options(line[0], line[1]) for line in tqdm.tqdm(data)]
    return np.sum(arrangements)


answer_question_1(example_data)
# %%
# answer_question_1(final_data)
# %%


def expand(line, times, sep):
    return f"{sep}".join([line for _ in range(times)])


def answer_question_2(data):
    expandval = 2
    data = [i.split(" ") for i in data]
    data = [(expand(i[0], expandval, "?"), expand(i[1], expandval, ",")) for i in data]
    arrangements = [calc_options(line[0], line[1]) for line in tqdm.tqdm(data)]
    return np.sum(arrangements)


# Old method is impossible in human time
answer_question_2(example_data)

# %%
# That wont work, I'll need DP and memorization for this,
# Redefine the problem
# Splits in treesearch on ?
# from left to right, walk
# (.???X.?X??..)
# split into:
# (.#??#.?#??..)
# (..??#.?#??..)


# %%
from functools import cache


@cache
def findsolutions(line: str, valsleft: tuple[int], counter: int) -> int:
    """Here comes in dynamic programming with pruning tables that
    are already known

    Args:
        line (str): rest of text needing parsing
        valsleft (tuple[int]): values left in that line
        counter (int): how many #'s have preceded directly

    Returns:
        int: returns an int how many options there are
    """
    optionscount = len(re.findall(r"#", line))

    if len(valsleft) == 0:
        if (optionscount == 0) & (counter == 0):
            return 1
        return 0

    if len(line) == 0:
        if (len(valsleft) == 0) & (counter == 0):
            return 1
        if (len(valsleft) == 1) & (valsleft[0] == counter):
            return 1
        return 0

    if counter > valsleft[0]:
        return 0

    char = line[0]
    if char == ".":
        if counter == 0:
            return findsolutions(line[1:], valsleft, 0)
        elif counter == valsleft[0]:
            return findsolutions(line[1:], valsleft[1:], 0)
        else:
            return 0

    if char == "#":
        return findsolutions(line[1:], valsleft, counter + 1)

    if char == "?":
        if counter == 0:
            return findsolutions(line[1:], valsleft, 0) + findsolutions(
                line[1:], valsleft, 1
            )
        elif counter == valsleft[0]:
            # Hashtag wont be good, only dot an option
            return findsolutions(line[1:], valsleft[1:], 0)
        elif counter < valsleft[0]:
            return findsolutions(line[1:], valsleft, counter + 1)
        else:
            return 1

    print(line, valsleft, counter)
    print("Somehow we got to the end without result")
    return 0


findsolutions("?###????????", (3, 2, 1), 0)
# %%


findsolutions("???.###", (1, 1, 3), 0)
# %%


def expand(line, times, sep):
    return f"{sep}".join([line for _ in range(times)])


def answer_question_2(data):
    expandval = 5
    data = [i.split(" ") for i in data]
    data = [(expand(i[0], expandval, "?"), expand(i[1], expandval, ",")) for i in data]
    data = [(i[0], tuple([int(j) for j in i[1].split(",")])) for i in data]
    # print(data)
    arrangements = [findsolutions(line[0], line[1], 0) for line in tqdm.tqdm(data)]
    print(arrangements)
    return np.sum(arrangements)


answer_question_2(final_data)


# %%
