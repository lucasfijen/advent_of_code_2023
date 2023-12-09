# %%
from utilities.collect_data import get_data, get_example_data
import numpy as np

import re

day = 7


final_data = get_data(day)

example_data = get_example_data(day)
example_data

# %%
def dataloader(data, sortorder="AKQJT98765432"):
    # Small mapping of order
    sortdict = {val: i for i, val in enumerate(sortorder)}

    # Create empty frames for bets & cards
    countmatrix = np.zeros((len(data), len(sortorder)), dtype=int)
    bets = np.empty((len(data), 1), dtype=int)
    norm_cards = []

    # Ugly way of filling the countmatrix
    for i, val in enumerate(data):
        hand, score = re.findall(r"\w+", val)
        bets[i] = score
        newstring = ""
        for char in hand:
            countmatrix[i, sortdict[char]] += 1
            # Little trick with leftpadding to make the new values sortable
            newstring+= f"{len(sortorder)-sortdict[char]:02}"
        norm_cards.append(newstring)
    return countmatrix, bets, np.array(norm_cards, dtype=int)

def handle_question1(data: list[str]) -> int:
    
    card_count, bets, norm_cards = dataloader(data)

    five_kind = 6 * (card_count == 5).any(axis=1)
    four_kind = 5 * (card_count == 4).any(axis=1)
    full_house = 4 * ((card_count == 3).any(axis=1) & (card_count == 2).any(axis=1))
    three_kind = 3 * (card_count == 3).any(axis=1)
    two_pair = 2 * ((card_count == 2).sum(axis=1) == 2)
    one_pair = 1 * ((card_count == 2).sum(axis=1) == 1)
    card_scores = np.array([five_kind, four_kind, full_house, three_kind, two_pair, one_pair]).T.max(
        axis=1
    ) + 1
    card_scores

    scoring_board = np.concatenate((card_scores[:, np.newaxis], norm_cards[:, np.newaxis]), axis=1)
    # Lexsort sorts from last columns to first, so ::-1 needed, also gives sorted indices, 
    # needs argsort to convert to target indices
    ranks = np.lexsort(scoring_board[:,::-1].T).argsort() + 1

    return (bets * ranks[:, np.newaxis]).sum()

handle_question1(example_data)
#%%
handle_question1(final_data)
# %%
def handle_question2(data: list[str]) -> int:
    
    card_count, bets, norm_cards = dataloader(data, "AKQT98765432J")

    nonjokers = card_count[:, :-1]
    jokers = card_count[:, -1, np.newaxis]
    five_kind = 6 * ((nonjokers + jokers) == 5).any(axis=1)
    four_kind = 5 * ((nonjokers + jokers) == 4).any(axis=1)
    full_house = 4 * (((nonjokers == 3).any(axis=1) & (nonjokers == 2).any(axis=1))
                      | (((nonjokers == 2).sum(axis=1) == 2) & (jokers[:, 0] == 1)))
    three_kind = 3 * ((nonjokers + jokers) == 3).any(axis=1)
    # Or just 2 pairs, or 1 pair and 1 joker, making always 2 pairs at least
    two_pair = 2 * ((nonjokers == 2).sum(axis=1) == 2) 
    one_pair = 1 * (((nonjokers == 2).sum(axis=1) == 1) 
                    | (jokers[:, 0] == 1)) 
    card_scores = np.array([five_kind, four_kind, full_house, three_kind, two_pair, one_pair]).T.max(
        axis=1
    ) + 1
    card_scores

    scoring_board = np.concatenate((card_scores[:, np.newaxis], norm_cards[:, np.newaxis]), axis=1)
    # Lexsort sorts from last columns to first, so ::-1 needed, also gives sorted indices, 
    # needs argsort to convert to target indices
    ranks = np.lexsort(scoring_board[:,::-1].T).argsort() + 1

    return (bets * ranks[:, np.newaxis]).sum()

handle_question2(example_data)
# %%
handle_question2(final_data)

# %%
