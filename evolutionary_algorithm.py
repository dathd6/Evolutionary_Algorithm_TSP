import csv
import random
import xml.etree.ElementTree as ET
# Components & Constants
from tsp import TSP
from utils import best_fitness
from constants import REPLACE_WEAKEST, REPLACE_FIRST_WEAKEST, REPORT_FOLDER

class EA:
    def __init__(self, file: str) -> None:
        self.map_matrix = [] # 2D Array contains cost of the edges between vertices
        self.vertex_count = 0 # Count number of vertex
        self.population = [] # Population of solution

        ############################################
        # Extract data from xml file to map_matrix #
        ############################################
        tree = ET.parse(file)
        root = tree.getroot()
        self.city = root.find('name').text
        # Find all the vertex element
        for vertex in root.findall(".//vertex"):
            self.map_matrix.append([])
            flag = True
            # Iterate and add all edge's cost to map_matrix
            for edge in vertex.findall("./edge"):
                # Add edge's cost = 0, if it is the same vertex
                if flag and type(edge.text) == str and int(edge.text) > self.vertex_count:
                    self.map_matrix[self.vertex_count].append(0)
                    flag = False # Turn off the flag to run only once
                self.map_matrix[self.vertex_count].append(float(edge.attrib['cost']))
            self.vertex_count += 1 # Count vertex
        self.map_matrix[-1].append(0)

    def __str__(self):
        result = ''
        for i, solution in enumerate(self.population):
            result += f'{i + 1}: {solution}\n'
        return result

    def generate_random_population_p(self, p):
        self.population = []
        for _ in range(p):
            random_tsp = TSP(self.map_matrix)
            self.population.append(random_tsp)

    def generate_best_population(self):
        # Open and read the final report CSV file
        with open(f'{REPORT_FOLDER}/final_report_{self.city}.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    solution = [int(vertex) for vertex in row['Optimize route'][1:-1].split(',')]
                    tsp = TSP(self.map_matrix, solution)
                    self.population.append(tsp)
                except:
                    random_tsp = TSP(self.map_matrix)
                    self.population.append(random_tsp)

    def tournament_selection(self, tournament_size):
        # Select best fitness in tournament selection
        parent_a = best_fitness(random.sample(self.population, tournament_size))
        parent_b = best_fitness(random.sample(self.population, tournament_size))
        return parent_a, parent_b

    def replace(self, new_solution, function=REPLACE_WEAKEST):
        # Replace solution with the weakest fitness
        if function == REPLACE_WEAKEST:
            weakest_solution_index = None
            for i, solution in enumerate(self.population):
                if (not weakest_solution_index) or \
                   (self.population[i] > self.population[weakest_solution_index]):
                    weakest_solution_index = i
            if weakest_solution_index:
                self.population[weakest_solution_index] = new_solution
            return weakest_solution_index
        # Replace first solution with weaker fitness
        elif function == REPLACE_FIRST_WEAKEST:
            for i, solution in enumerate(self.population):
                if solution > new_solution:
                    self.population[i] = new_solution
                    return i
                
    def best_solution(self) -> TSP:
        result = best_fitness(self.population)
        if result:
            return result
        return TSP(map_matrix=self.map_matrix)
