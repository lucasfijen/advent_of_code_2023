# %%
from utilities.collect_data import get_data, get_example_data
import numpy as np

import re

day = 10


final_data = get_data(day)

example_data = get_example_data(day)

example_data_2 = get_example_data(day, '_2')
example_data_3 = get_example_data(day, '_3')
example_data_4 = get_example_data(day, '_4')
example_data

# ─│┌┐└┘
# %%

def perform_step(scores, legit_steps, current_pos, steps, i):
    pos_steps = legit_steps & (scores == 0)
    nextscore = i + 1
    if 'S' in steps:
        scores[1:, :][current_pos[:-1, :] & pos_steps[1:, :]] = nextscore
    if 'N' in steps:
        scores[:-1, :][current_pos[1:, :] & pos_steps[:-1, :]] = nextscore
    if 'E' in steps:
        scores[:, 1:][current_pos[:, :-1] & pos_steps[:, 1:]] = nextscore
    if 'W' in steps:
        scores[:, :-1][current_pos[:, 1:]& pos_steps[:, :-1]] = nextscore

def add_colour(val, number, maxnr):
    if (0 < number < 2000) and (maxnr > number):
        val = f"\033[32m{val}\033[37m"
    elif 2000 < number < 4000:
        val = f"\033[33m{val}\033[37m"
    elif 4000 < number < maxnr:
        val = f"\033[31m{val}\033[37m"
    elif maxnr <= number:
        val = f"\033[35m{val}\033[37m"

    return val

def plot_array(orig_arr, scores):
    maxnr = scores.max()-1
    print('\n'.join([''.join([add_colour(i,j, maxnr) for i,j in zip(rows[0], rows[1])]) for rows in zip(orig_arr, scores)]))
    print(orig_arr)

def perform_question_1(data):

    replacedict = {
        '|': '│',
        '-': '─',
        'L': '└',
        'J': '┘',
        '7': '┐',
        'F': '┌',
        '.': ' '
    }
    orig_arr = np.array([[replacedict.get(i, i) for i in j] for j in data])
    # print(orig_arr)
    # print('\n'.join([''.join([i for i in j]) for j in orig_arr]))
    scores = np.zeros(orig_arr.shape, dtype = int)
    legit_steps = (orig_arr != ' ') & (orig_arr != 'S')
    # Populate starting points:
    
    stepsdict = {
        '│' : ['N', 'S'],
        '─' : ['W', 'E'],
        '└' : ['N', 'E'],
        '┘' : ['N', 'W'],
        '┐' : ['S', 'W'],
        '┌' : ['S', 'E'],
        'S' : ['N', 'E', 'S', 'W']
    }

    maxscore = scores.max()
    maxiters = 1000000
    for i in range(maxiters):
        # print(scores)
        if i == 0:
            # Small bug here, I dont check whether they are actually connectable
            current_pos = orig_arr == 'S'
        else:
            current_pos = scores == i
        for simb in np.unique(orig_arr[current_pos]):
            # print(simb, i)
            current_symb_pos = current_pos & (orig_arr == simb)
            perform_step(scores, legit_steps, current_symb_pos, stepsdict[simb], i)
            # print(np.concatenate((scores, orig_arr), axis=1))
        newmax = scores.max()
        if newmax == maxscore:
            print(f'done in iteration {i}')
            break
        maxscore = newmax
    plot_array(orig_arr, scores)
    # with np.printoptions(threshold=np.inf):
    #     print(scores)
    return maxscore, orig_arr, scores
maxscore, orig_arr, scores = perform_question_1(example_data_3)
maxscore
# %%
maxscore, orig_arr, scores = perform_question_1(final_data)
# %%
# Answers given:
# 6940
# 6941
# 6942 is the right answer

# %%
for i in zip([[1,2,3], [2,3,4]]):
    print(i)
# %%


#%%
def count_crossings(arr):
    return len(re.findall(r"(┌─*┘)|(│)|(└─*┐)", "".join(arr)))

#%% Uggly iterate over all points, 

def add_colour_new(val, number, maxnr):
    if number > 0:
        val = 'X'
    if (0 < number < 2000) and (maxnr > number):
        val = f"\033[32m{val}\033[37m"
    elif 2000 < number < 4000:
        val = f"\033[33m{val}\033[37m"
    elif 4000 < number < maxnr:
        val = f"\033[31m{val}\033[37m"
    elif maxnr <= number:
        val = f"\033[35m{val}\033[37m"

    return val

def plot_array_new(orig_arr, scores):
    maxnr = scores.max()-1
    print('\n'.join([''.join([add_colour_new(i,j, maxnr) for i,j in zip(rows[0], rows[1])]) for rows in zip(orig_arr, scores)]))
    print('x filled ')
    print(orig_arr)

def calc_encapsuled(orig_arr, scores, sreplacement):
    # sreplacement = '┌' # Hard example
    # sreplacement = '┘' #final
    new_arr = np.char.replace(orig_arr.copy(), 'S', sreplacement)
    locked_locs = np.zeros(new_arr.shape, dtype=int)
    on_the_line = (scores > 0) | (orig_arr == 'S')
    for row_nr in range(new_arr.shape[0]):
        for col_nr in range(new_arr.shape[1]):
            # Skip if points doesnt count
            if not on_the_line[row_nr, col_nr]:
                # All loop parts to left
                currentslice = new_arr[row_nr, :col_nr]
                all_points = currentslice[on_the_line[row_nr, :col_nr]]
                lcrossings = count_crossings(all_points)
                locked_locs[row_nr, col_nr] = lcrossings
    plot_array_new(new_arr, locked_locs %2)
    return (locked_locs % 2).sum(), locked_locs 



maxscore, orig_arr, scores = perform_question_1(example_data_4)
calc_encapsuled(orig_arr, scores, '┐')


#%%

maxscore, orig_arr, scores = perform_question_1(final_data)
# yes that replacement symbol could be automated, 
# but I want my weekend day back:)
calc_encapsuled(orig_arr, scores, '┘')


#%%