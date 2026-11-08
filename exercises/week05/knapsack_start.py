"""
Oefening 2: Knapsack Probleem met pygad
=========================================
Los het knapsack probleem op met een genetisch algoritme.
"""

import pygad
import numpy as np

# Data
capaciteit = 10
gewichten = np.array([5, 4, 6, 3])
waarden = np.array([10, 40, 30, 50])
n_voorwerpen = len(gewichten)


def fitness_func(ga_instance, solution, solution_idx):
    # TODO: bereken totale waarde, straf als gewicht > capaciteit
    print(solution)

    tot_weight = sum(solution * gewichten)
    tot_value = sum(solution * waarden)

    if tot_weight <= capaciteit:
        return tot_value
    return tot_value - 1000


# TODO: configureer pygad.GA (zie OneMax.py uit de cursus)
ga_instance = pygad.GA(
    num_generations=20,
    num_parents_mating=10,
    fitness_func=fitness_func,
    sol_per_pop=30,
    num_genes=n_voorwerpen,
    gene_space=[0, 1],
    gene_type=int,
    mutation_percent_genes=10,
)
ga_instance.run()

# Oplossing tonen
solution, solution_fitness, _ = ga_instance.best_solution()
print("Gekozen voorwerpen:", solution)
print("Totale waarde:", solution_fitness)
