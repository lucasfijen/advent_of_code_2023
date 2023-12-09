# %%
from utilities.collect_data import get_data, get_example_data
import numpy as np

import re

day = 6


final_data = get_data(day)

example_data = get_example_data(day)
example_data
# %%

def data_parser(data: list[str]) -> list[tuple[str]]:
    data = np.array([re.findall(r"\d+", i) for i in data], dtype=int)
    return data.T

data_parser(example_data)
#%%

def data_parser_2(data: list[str]) -> list[tuple[str]]:
    data = np.array(["".join(re.findall(r"\d+", i)) for i in data], dtype=int)
    return data[:, np.newaxis].T

data_parser_2(example_data)
#%%

def answer_question(data, q2=False):
    if q2:
        input_data = data_parser_2(data)
    else:
        input_data = data_parser(data)

    loadtime = np.arange(0,input_data[:, 0].max()) + np.zeros((input_data.shape[0],1), dtype=int)
    loadtime 

    traveltimes = (input_data[:,0, np.newaxis] -loadtime) * loadtime
    traveltimes

    return (traveltimes > input_data[:,1, np.newaxis]).sum(axis=1).prod()


answer_question(example_data)
# %%
answer_question(final_data)
# %%
answer_question(final_data, q2=True)
# %%
