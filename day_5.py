# %%
from utilities.collect_data import get_data, get_example_data
import numpy as np

import re

day = 5


final_data = get_data(day)

example_data = get_example_data(day)
example_data
# %%


def handle_question_1(data):
    all_startseeds = re.findall(r"\d+", data[0])

    val = np.array([], dtype=int)

    newval = np.array([int(i) for i in all_startseeds], dtype=int)

    for line in data[1:]:
        if re.search(r"map", line):
            # Init new set
            # print(line)
            newval = np.concatenate((newval, val))

            val = newval.copy()
            newval = np.array([], dtype=int)

        elif re.match(r"\d+ \d+ \d+", line):
            dest, start, rng = [
                int(i) for i in re.match(r"(\d+) (\d+) (\d+)", line).group(1, 2, 3)
            ]
            # print(f'{dest=}{start=}{rng=}')

            mask = (start <= val) & (val < start + rng)

            selection = val[mask]
            newval = np.concatenate((newval, selection + (dest - start)))

            val = val[~mask]

    newval = np.concatenate((newval, val))

    return newval.min()


handle_question_1(example_data)


# %%
handle_question_1(final_data)
# %%


def handle_question_2(data:list[str]) -> int:
    """In the second question, we'll get large numbers to process,
    which is too much to handle in memory, so we'll have to convert to 
    use of ranges, and calculating with those.

    I create 2d numpy arrays, in which the first col is the startnr
    and the second the length of the range.

    Args:
        data (list[str]): Data to be used

    Returns:
        int: lowest startnumber
    """
    rngs = re.findall(r"(\d+) (\d+)", data[0])
    all_startseeds = np.array(rngs, dtype=int)

    val = all_startseeds
    newval = np.empty([0, 2], dtype=int)

    for line in data[1:]:
        if re.search(r"map", line):
            # Init new set
            newval = np.concatenate((newval, val))
            val = newval.copy()
            newval = np.empty([0, 2], dtype=int)

        elif re.match(r"\d+ \d+ \d+", line):
            dest, start, rng = np.array(
                re.match(r"(\d+) (\d+) (\d+)", line).group(1, 2, 3), dtype=int
            )

            # selection only with overlap :
            overlap_mask = ~(
                ((start + rng) <= val[:, 0]) | (start >= (val.sum(axis=1)))
            )
            selection = val[overlap_mask]
            # left untouched
            l_untouched_mask = selection[:, 0] < start
            left_untouched = selection[l_untouched_mask].copy()
            left_untouched[:, 1] = start - left_untouched[:, 0]

            # right untouched
            r_untouched_mask = selection.sum(axis=1) > (start + rng)
            r_untouched_mask
            right_untouched = selection[r_untouched_mask].copy()
            right_untouched[:, 1] = right_untouched.sum(1) - (start + rng)
            right_untouched[:, 0] = start + rng

            # overlap
            startvals = np.maximum(selection[:, 0], start)
            endvals = np.minimum(selection.sum(axis=1), start + rng)
            overlap = np.column_stack((startvals, endvals - startvals))
            overlap[:, 0] += dest - start
            newval = np.concatenate((newval, overlap))

            val = np.concatenate((val[~overlap_mask], left_untouched, right_untouched))

    newval = np.concatenate((newval, val))

    # Here we can nvm the range aspect, as ranges only go up in numbers
    return newval[:, 0].min()


handle_question_2(example_data)
# %%
handle_question_2(final_data)
# %%
