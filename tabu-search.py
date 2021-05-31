#SMTWTP: Single Machine Total Weighted Tardiness Problem

import pandas as pd
import random as rd
from itertools import combinations

def input_data(Path):
	return pd.read_excel(Path, names=['Job', 'weight', "processing_time", "due_date"], index_col = 0, engine='openpyxl').to_dict('index')
	
instance_dict = input_data('Instance_10.xlsx')

print(instance_dict)





























