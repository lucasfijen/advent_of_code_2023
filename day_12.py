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



def calc_options(line, values):
    options = len(re.findall(r'\?', line))
    scores = [int(i) for i in values.split(',')]
    hash_needed = np.sum(scores) - len(re.findall(r"\#", line))

    # Regexpression to check if valid answer/permutation
    regexcheck = f"^\\.*#{{{scores[0]}}}"
    if len(scores) > 1:
        for i in scores[1:]:
            regexcheck += f"\\.+#{{{i}}}"
    regexcheck += "\\.*$"
    # Lets go through all permutations, we need a fixed amount of # so:
    fillstring = "#"*hash_needed + '.' * (options - hash_needed)
    perms = set(idp(fillstring))
    valid_options = 0
    for perm in perms:
        poplist = list(perm)
        permstring = re.sub(r'\?', lambda x: poplist.pop(0), line)
        if re.match(regexcheck, permstring):
            valid_options+= 1
    return valid_options

def answer_question_1(data):
    
    data = [i.split(' ') for i in data]
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
    data = [i.split(' ') for i in data]
    data = [(expand(i[0], expandval, '?'), expand(i[1], expandval, ',')) for i in data]
    arrangements = [calc_options(line[0], line[1]) for line in tqdm.tqdm(data)]
    return np.sum(arrangements)

answer_question_2(example_data)

#%%
# That wont work, I'll need DP and memorization for this,
# Redefine the problem
# Split over .
# from left to right, walk
# (.???X.?X??..)
# split into:
# (.#??#.?#??..)
# (..??#.?#??..)



def findsolutions(line: str, valsleft: tuple[int]) -> int:
    amountleft = len(re.findall(r"[#?]", line)) - np.sum(valsleft)

    if amountleft == 0:
        # Hier zit bug in, alsnog checken of er . tussen zit
        return 1
    if amountleft < 0:
        return 0

    resultcount = 0
    # Go down
    counter = 0
    for i in range(len(line)):
        char = line[i]
        if char == '.':
            if counter == 0:
                continue
            elif counter == valsleft[0]:
                # Pop 1 from valsleft and continue
                return resultcount + findsolutions(line[i+1:], valsleft[1:])
            # Invalid
            return 0
            
        if char == '#':
            counter += 1
            if counter > valsleft[0]:
                return 0
            
        if char == '?':
            if counter == 0:
                # Dot option
                resultcount += findsolutions(line[i+1:], valsleft[1:])
            # After that explore the # approach
            counter += 1





    # If went through all characters, return 0?
    return 1

for i in range(5):
    if i == 2:
        continue
    print(i)
# %%
(1,2,3)[4:]
# %%
np.sum(())
# %%
