# %%
from utilities.collect_data import get_data, get_example_data
import numpy as np

import re

day = 4


final_data = get_data(day)

example_data = get_example_data(day)
example_data
# %%

def process_line(line):
    card_id, win_numbers, my_numbers = re.findall(r"Card\s+(\d*):(.+)\|(.+)", line)[0]

    winset = set(re.findall(r"\d+", win_numbers))
    numberset = set(re.findall(r"\d+", my_numbers))
    wins = len(winset & numberset)
    if wins > 0:
        return 2**(wins-1)
    else:
        return 0



def counter_games(codelist):
    return np.sum([process_line(line) for line in codelist])


counter_games(example_data)
# %%

counter_games(final_data)
# %%

from collections import defaultdict

defaultdict(int)
def process_line_2(line):
    card_id, win_numbers, my_numbers = re.findall(r"Card\s+(\d*):(.+)\|(.+)", line)[0]

    winset = set(re.findall(r"\d+", win_numbers))
    numberset = set(re.findall(r"\d+", my_numbers))
    return int(card_id), len(winset & numberset)

def handle_game(data):

    cards = defaultdict(int)
    maxlen = len(data) + 1
    for line in data:
        card_id, wins = process_line_2(line)
        cards[card_id] += 1
    
        winval = cards[card_id]
        for i in range(wins):
            if i <= maxlen:
                cards[card_id+i+1] += winval


    return np.sum([val for _, val in cards.items()])

handle_game(final_data)

# %%
for i in range(5):
    print(i)
# %%
