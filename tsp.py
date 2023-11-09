import random
from constants import PARTIALLY_MAPPED_CROSSOVER, \
                      SEQUENTIAL_CONSTRUCTIVE_CROSSOVER, \
                      ORDERED_CROSSOVER, \
                      SINGLE_SWAP_MUTATION, \
                      INVERSION
from utils import swap_gene

class TSP:
    route = []
    map_matrix = []
    vertex_count = 0

    def __init__(self, map_matrix, route=None):
        self.map_matrix = map_matrix
        self.vertex_count = len(map_matrix)
        if route:
            self.route = route # Add route
        else:
            self.generate_random_solution() # Generate random solution (route)
        self.calculate_fitness() # Calculate fitness

    def __str__(self):
        route = str(self.route)[1:-1].replace(',', ' ->')
        return f'Solution {route} - fitness {self.fitness}'

    def __gt__(self, other):
        # Compare fitness between solution >
        return self.fitness > other.fitness

    def __ge__(self, other):
        # Compare fitness between solution: >=
        return self.fitness >= other.fitness

    def generate_random_solution(self):
        self.route = []
        # Stop when travelling through all vertices
        while len(self.route) < self.vertex_count:
            random_vertex = random.randint(0, self.vertex_count - 1)
            # If vertex is not visited, add vertex to the solution
            if not (random_vertex in self.route):
                self.route.append(random_vertex)

    def calculate_fitness(self):
        self.fitness = 0
        for i in range(1, self.vertex_count):
            # Add edge cost to the fitness
            self.fitness += self.map_matrix[self.route[i - 1]][self.route[i]]

        self.fitness += self.map_matrix[self.route[-1]][self.route[0]]
        return self.fitness

    def mutation(self, operator):
        new_solution = []
        # Single swap mutation
        if operator == SINGLE_SWAP_MUTATION:
            new_solution = swap_gene(self.route) # Swap two random vertices
        # Inversion mutation
        elif operator == INVERSION:
            # Choose two random indices
            first_index = random.randint(0, self.vertex_count - 2)
            second_index = random.randint(first_index + 1, self.vertex_count - 1)

            try:
                if first_index < second_index:
                    # Reverse route from first index to second index
                    inverse = self.route[first_index:second_index]
                    inverse.reverse()
                    new_solution = self.route[:first_index] + inverse + self.route[second_index:]
            except:
                # Exception -> reverse the whole solution
                new_solution = self.route.copy()
                new_solution.reverse()

        return TSP(self.map_matrix, new_solution)

    def crossover(self, other_tsp, operator=PARTIALLY_MAPPED_CROSSOVER):
        parent_a = self.route.copy()
        parent_b = other_tsp.route.copy()
        child_c = None
        child_d = None
        first_point_subset = random.randint(1, self.vertex_count - 1)
        second_point_subset = random.randint(first_point_subset, self.vertex_count - 1) + 1
        # Partially matched crossover
        if operator == PARTIALLY_MAPPED_CROSSOVER:
            child_c = parent_a.copy()
            child_d = parent_b.copy()
            for i in range(first_point_subset, second_point_subset):
                # Partially mapped crossover (PMX)
                swap_gene(child_c, child_c.index(parent_b[i]), i)
                swap_gene(child_d, child_d.index(parent_a[i]), i)
                # cross data
                child_c[i] = parent_b[i]
                child_c[child_c.index(child_c[i])] = parent_a[i]
                # cross data
                child_d[i] = parent_a[i]
                child_d[child_d.index(child_d[i])] = parent_b[i]
        # Sequential constructive crossover
        elif operator == SEQUENTIAL_CONSTRUCTIVE_CROSSOVER:
            flag = [False for _ in range(self.vertex_count)]
            index = 0
            flag[index] = True
            while not flag[parent_a.index(parent_b[index])]:
                index = parent_a.index(parent_b[index])
                flag[index] = True
            child_c = []
            child_d = []
            for i in range(self.vertex_count):
                if flag[i]:
                    child_c.append(parent_a[i])
                    child_d.append(parent_b[i])
                else:
                    child_c.append(parent_b[i])
                    child_d.append(parent_a[i])


        # Ordered crossover
        elif operator == ORDERED_CROSSOVER:    
            subset_parent_a = parent_a[first_point_subset:second_point_subset]
            subset_parent_b = parent_b[first_point_subset:second_point_subset]

            before_subset_a = []
            before_subset_b = []

            for i in range(self.vertex_count):
                if not parent_b[i] in subset_parent_a:
                    if len(before_subset_a) < first_point_subset:
                        before_subset_a.append(parent_b[i])
                    else:
                        subset_parent_a.append(parent_b[i])

                if not parent_a[i] in subset_parent_b:
                    if len(before_subset_a) < first_point_subset:
                        before_subset_b.append(parent_a[i])
                    else:
                        subset_parent_b.append(parent_a[i])

            child_c = before_subset_a + subset_parent_a
            child_d = before_subset_b + subset_parent_b

        return TSP(self.map_matrix, child_c), TSP(self.map_matrix, child_d)
