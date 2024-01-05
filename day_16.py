# %%
import itertools
import re
from collections import defaultdict

import numpy as np
import tqdm
from more_itertools import distinct_permutations as idp

from utilities.collect_data import get_data, get_example_data

day = 16

final_data = get_data(day)

example_data = get_example_data(day)
example_data
# %%
example_data
# %%
positions = set()
data = example_data
data = np.array([[i for i in j] for j in data])

#%%
def oposite_dir(dir):
    match dir:
        case 'v':
            return '^'
        case '^':
            return 'v'
        case '>':
            return '<'
        case '<':
            return '>'
        
def straight_step(dir, loc):
    match dir:
        case 'v':
            return (loc[0]+1, loc[1])
        case '^':
            return (loc[0]-1, loc[1])
        case '>':
            return (loc[0], loc[1]+1)
        case '<':
            return (loc[0], loc[1]-1)
        
def odd_step(dir, loc, current):
    steps = ['<', '^', 'v', '>']
    result = []
    match current:
        case '/':
            match dir:
                case '<':
                    result.append('v')
                case '^':
                    result.append('>')
                case '>':
                    result.append('^')
                case 'v':
                    result.append('<')
        case '\\':
            match dir:
                case '<':
                    result.append('^')
                case '^':
                    result.append('<')
                case '>':
                    result.append('v')
                case 'v':
                    result.append('>')

        case '|':
            match dir:
                case '<' | '>':
                    result.extend(['^', 'v'])
                case _:
                    result.append(dir)

        case '-':
            match dir:
                case '^' | 'v':
                    result.extend(['<', '>'])
                case _:
                    result.append(dir)
    
    return [(straight_step(i, loc), i) for i in result]






def perform_step(df, loc, dir, visited_positions):
    # Check if in range
    if (np.min(loc) < 0) or (loc[0] >= df.shape[0]) or (loc[1] >= df.shape[1]):
        return []
    
    # Check if not already visited either way
    if dir in visited_positions[loc]:
        return []
    if (oposite_dir in visited_positions[loc]) and (df[loc] not in ['\\', '/']):
        return []
    
    # Add step
    visited_positions[loc].append(dir)
    # print(df)
    # print(df[loc])
    # Find next positions
    if df[loc] == '.':
        return [(straight_step(dir, loc), dir),]

    # Check special character
    else:
        # print('else')
        # print(odd_step(dir, loc, df[loc]))
        return odd_step(dir, loc, df[loc])


def answer_question_1(data, startpoint = [((0,0), '>')]):
    data = np.array([[i for i in j] for j in data])
    visited_positions = defaultdict(list)
    steps = startpoint
    for iter in range(20000):
        newsteps = []
        if len(steps) == 0:
            break
        for step in steps:
            loc, dir = step
            newsteps.extend(perform_step(data, loc, dir, visited_positions))
        steps = newsteps

    return len(visited_positions)

answer_question_1(example_data)

# %%
answer_question_1(final_data)
# %%
def answer_question_2(data):
    data = np.array([[i for i in j] for j in data])
    maxval = 0
    for i in range(data.shape[0]):
        newscore = answer_question_1(data, [((i, 0), '>')])
        if newscore > maxval: 
            maxval = newscore
        
        newscore = answer_question_1(data, [((i, data.shape[1]), '<')])
        if newscore > maxval: 
            maxval = newscore
    
    for i in range(data.shape[1]):
        newscore = answer_question_1(data, [((0, i), 'v')])
        if newscore > maxval: 
            maxval = newscore
        
        newscore = answer_question_1(data, [((data.shape[0], i), '^')])
        if newscore > maxval: 
            maxval = newscore
    return maxval

answer_question_2(final_data)