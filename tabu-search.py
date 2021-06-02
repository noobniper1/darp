#SMTWTP: Single Machine Total Weighted Tardiness Problem

import pandas as pd
import random as rd
from itertools import combinations

def input_data(Path):
	return pd.read_excel(Path, names=['Job', 'weight', "processing_time", "due_date"], index_col = 0, engine='openpyxl').to_dict('index')
	
instance_dict = input_data('Instance_10.xlsx')

print(instance_dict)

def Objfun(instance_dict, solution, show = False):
	dict = instance_dict
	t = 0
	objfun_value = 0
	for job in solution:
		C_i = t + dict[job]["processing_time"]
		d_i = dict[job]["due_date"]
		T_i = max(0, C_i - d_i)
		W_i = dict[job]["weight"]
		objfun_value += W_i * T_i
		t = C_i

	if show == True:
		print("\n", "#"*8, "The Objective function value for {} solution schedule is: {}".format(solution, objfun_value), "#"*8)
		return objfun_value

solution_1 = [1, 2, 5, 6, 8, 9, 10, 3, 4, 7]
solution_2 = [2, 3, 5, 10, 6, 8, 9, 4, 7, 1]

fitness_1 = Objfun(instance_dict, solution_1, show = True)
fitness_2 = Objfun(instance_dict, solution_2, show = True)

def get_InitialSolution(instance_dict, seed, show = False):
	n_jobs = len(instance_dict)
	initial_solution = list(range(1, n_jobs + 1))
	rd.seed(seed)
	rd.shuffle(initial_solution)
	if show == True:
		print("initial Random Solution: {}".format(initial_solution))
	return initial_solution


def SwapMove(solution, i, j):
	solution = solution.copy()
	
	i_index = solution.index(i)
	j_index = solution.index(j)
	
	solution[i_index], solution[j_index] = solution[j_index], solution[i_index]
	return solution

initial_solution = get_InitialSolution(instance_dict, 2021, show = True)
print('Neighbor solution: {}'.format(SwapMove(initial_solution, 10, 5)))























