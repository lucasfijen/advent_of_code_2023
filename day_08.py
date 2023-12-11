# %%
from utilities.collect_data import get_data, get_example_data
import numpy as np

import re

day = 8


final_data = get_data(day)

example_data = get_example_data(day)
example_data_2 = get_example_data(day, "_2")
example_data_3 = get_example_data(day, "_3")
example_data_3

# %%
example_data_2
# %%
def linelookup(line):
    matcher = re.search(r"(\w+) = \((\w+), (\w+)\)",  line)
    if matcher:
        key, v1, v2 =  matcher.groups()
        return key, (v1, v2)
    else:
        return None

def dataloader(data):
    # Filter out any potential non-allowed characters
    instructions = "".join(re.findall(r"[LR]", data[0]))

    inbetween = [linelookup(line) for line in data]
    # Now we'll make lookup dict:
    maps = {i[0]: i[1] for i in [linelookup(line) for line in data] if i is not None}
    return instructions, maps

instr, maps = dataloader(example_data)
maps
# %%
def handle_question_1(data):
    
    instr, maps = dataloader(data)
    lr_dict = {'L': 0, 'R': 1}
    location = 'AAA'
    counter = 0
    maxiters = 100000000
    while (location != 'ZZZ') and (counter < maxiters):
        # Allows for repeating
        leftright = instr[counter % len(instr)]
        # Can start with step, as you'll never start on ZZZ
        location = maps[location][lr_dict[leftright]]
        counter += 1
    if counter >= maxiters:
        print('Ran out of iterations')

    print('finished')
    return counter

handle_question_1(example_data)

# %%

handle_question_1(example_data_2)
# %%
handle_question_1(final_data)
# %%
def gcd(a, b):
    if a == 0:
        return b
    else:
        return gcd(b % a, a)

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def calculate_lcm(numbers):
    result_lcm = 1
    for number in numbers:
        result_lcm = lcm(result_lcm, number)
    return result_lcm

def handle_question_2(data):
    
    instr, maps = dataloader(data)
    lr_dict = {'L': 0, 'R': 1}

    # Note, if can't find locatin in maps, it will remain at destination, 
    # so ZZZ will remain at ZZZ eternally
    vecfunc = np.vectorize(lambda x, left: maps.get(x, [x, x])[lr_dict[left]])

    # Select start locations ending with A
    locs = np.array([ i for i in maps.keys() if re.search(r"A$", i)])
    counter = 0
    maxiters = 1000000000
    stepscount = len(instr)
    visit_count = np.zeros((len(locs),), dtype=int)
    loop_starts =  np.zeros((len(locs),), dtype=int)
    loop_durations = np.zeros((len(locs),), dtype=int)

    # So we have async loops, i checked, all are closed and seperate
    # So basically, we just need to have the startpoints, and the durations
    # To know those, we need all points to have visited xxZ at least twice.
    while (not (visit_count > 1).all()) and (counter < maxiters):
        leftright = instr[counter % stepscount]
        # Can start with step, as you'll never start on ZZZ
        locs = vecfunc(locs, leftright)
        
        counter += 1
        anyfinish = np.char.endswith(locs, 'Z')
        if anyfinish.any():
            visit_count[anyfinish] += 1
            loop_durations[anyfinish] = counter - loop_starts[anyfinish]
            loop_starts[anyfinish] = counter

    if counter >= maxiters:
        print('Ran out of iterations')

    # Aparently all the start points % duration are 0, this uggly 
    # Feature of the data makes calculating it easier, but still
    # IMO this is a nasty bit of this exercise would have been more
    # Fun with non round loops, now all XXZ's point to their XXA's
    # So these camels really are walking rounds in the desert, and 
    # not towards a loop to there end up in a loop
    return calculate_lcm(loop_durations)

handle_question_2(final_data)

