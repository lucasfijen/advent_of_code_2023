# %%
import itertools
import re
from collections import defaultdict

import numpy as np
import tqdm
from more_itertools import distinct_permutations as idp

from utilities.collect_data import get_data, get_example_data

day = 17

final_data = get_data(day)


example_data = get_example_data(day)
example_data

#%%
import heapq
# %%

def get_oposite(dir):
    match dir:
        case '>':
            return '<'
        case '<':
            return '>'
        case '^':
            return 'v'
        case 'v':
            return '^'

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
        


def all_steps(loc, dir, stepcount):
    steps = {'v', '<', '^', '>'}
    steps.discard(get_oposite(dir))
    if loc[0] == 0: 
        steps.discard('<')
        
    if stepcount == 0:
        steps.discard(dir)
    return [(straight_step(step, loc), step, stepcount - 1) for step in steps]



steps = {'v', '<', '^', '>'}
steps.discard('v')
# steps.discard('v')
steps
# %%
