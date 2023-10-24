import random

def best_fitness(population):
    if len(population) == 0:
        return None
    result = None
    # iterating through population to find solution with best fitness
    for solution in population:
        if not result:
            result = solution
        elif result > solution:
            result = solution
    return result

def swap_gene(chromosome, gene1=None, gene2=None):
    new_solution = chromosome.copy()
    # choose two random genes
    # If there are none given gene
    if not gene1:
        gene1 = random.randint(0, len(new_solution) - 1)
    if not gene2:
        gene2 = random.randint(0, len(new_solution)- 1)
    # Swap
    temp = new_solution[gene1]
    new_solution[gene1] = new_solution[gene2]
    new_solution[gene2] = temp
    return new_solution
