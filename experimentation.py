import os
import csv
import random
import matplotlib.pyplot as plt
import seaborn as sns
from time import time
# Components & Constants
from evolutionary_algorithm import EA
from constants import REPORT_FOLDER, TERMINATION_CRITERION
from constants import CROSSOVER_WITH_FIX, ORDERED_CROSSOVER
from constants import REPLACE_FIRST_WEAKEST, REPLACE_WEAKEST
from constants import SINGLE_SWAP_MUTATION, MULTIPLE_SWAP_MUTATION, INVERSION

list_crossovers = [
    CROSSOVER_WITH_FIX,
    ORDERED_CROSSOVER,
]

list_replacements = [
    REPLACE_WEAKEST,
    REPLACE_FIRST_WEAKEST
]

list_mutations = [
    SINGLE_SWAP_MUTATION,
    MULTIPLE_SWAP_MUTATION,
    INVERSION
]

class Experimentation:
    def __init__(self, dataset, test_best_population=None):
        # Initialise experimentation parameters
        # Random the value to add randomness to each execution
        # Create report directory
        self.ea = EA(dataset)
        self.report_dir = f'{REPORT_FOLDER}/report_{self.ea.city}'
        if not os.path.exists(self.report_dir):
            os.mkdir(self.report_dir)
        if test_best_population:
            self.ea.generate_best_population()
            self.population_size = len(self.ea.population)
        else:
            self.population_size = random.randint(100, 10000)
            # Create EA instance to initialise population of solutions
            self.ea.generate_random_population_p(self.population_size)
        self.tournament_size =  round(self.population_size / random.randint(4, 100))
        self.replacement_function = list_replacements[random.randint(0, 1)]
        self.mutation_function = list_mutations[random.randint(0, 2)]
        self.crossover_funciton = list_crossovers[random.randint(0, 1)]
        # Add sample data to visualise cities & route
        self.visualise_data = [(random.randint(0, 10000), random.randint(0, 10000)) for _ in range(self.ea.vertex_count)]
        # Detail process report columns
        self.report_data = [['Generation', 
                             'Tournament selection - parent A',
                             'Tournament selection - parent B',
                             'Crossover - Child C',
                             'Crossover - Child D',
                             'Mutation - New solution E',
                             'Mutation - New solution F',
                             'Best solution',
                             'Best solution from generation ?']]
        # Generate a new filename for current experimentation's report
        # including name for csv & png files
        self.report_name = f'report_{round(len(os.listdir(self.report_dir)) / 2)}'
        # Array of data records the solution and 
        # generation achieving the best fitness at that current generation
        self.record_best_solution = [{
            'generation': 0,
            'solution': self.ea.best_solution(),
            'execution_time': 0
        }]

    def __str__(self):
        return f"""- Population size: {self.population_size}
- Tournament size: {self.tournament_size}
- Crossover function: {self.crossover_funciton}
- Mutation function: {self.mutation_function}
- Replacement function: {self.replacement_function}"""

    def report_generate(self):
        with open(f'{self.report_dir}/{self.report_name}.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.report_data)

    def visualise(self):
        # Only visualize the last record (Best fitness)
        record = self.record_best_solution[-1]
        best_solution = record['solution']
        # Create 2x2 plot
        fig, ax = plt.subplots(2, 2, figsize=(12, 8))
        title = fig.suptitle(f"TSP - ${self.report_name}", wrap=True)
        title.set_position((0.5, 0))

        # Visualise route of best solution
        x, y = zip(*self.visualise_data)
        colors = sns.color_palette("husl", self.ea.vertex_count)
        sns.scatterplot(
            x=x,
            y=y,
            ax=ax[0,0],
            hue=colors,
            palette=colors,
            legend=False,
            s=100
        )
        # Create a scatter plot with sample data points (visualising the map/cities)
        for i, (x, y) in enumerate(self.visualise_data):
            ax[0,0].annotate(i, (x, y), textcoords="offset points", xytext=(0, -3), ha='center')
        # Add route between cities
        # Draw edges (lines) between data points
        x1, y1 = self.visualise_data[best_solution.route[0]]
        x2, y2 = self.visualise_data[best_solution.route[-1]]
        sns.lineplot(x=[x1, x2], y=[y1, y2], color=colors[-1], linewidth=2, marker='o', markersize=15, markeredgecolor='black', ax=ax[0,0])
        for i in range(len(self.visualise_data) - 1):
            x1, y1 = self.visualise_data[best_solution.route[i]]
            x2, y2 = self.visualise_data[best_solution.route[i + 1]]
            sns.lineplot(x=[x1, x2], y=[y1, y2], color=colors[i], linewidth=2, marker='o', markersize=15, markeredgecolor='black', ax=ax[0,0])
        # Add label, title and annotates
        ax[0,0].set_title(f'Route of best solution')
        ax[0,0].set_xlabel(f'Population Size of {self.population_size}')
        ax[0,0].set_ylabel(f'Tournament Size of {self.tournament_size}')

        # convergence curves
        divergence = [abs(best_solution.fitness - record['solution'].fitness) for record in self.record_best_solution]
        sns.lineplot(
            x=range(TERMINATION_CRITERION),
            y=divergence,
            color='green',
            ax=ax[0,1])
        for i, value in enumerate(divergence[::1000]):
            sns.scatterplot(x=[i * 1000], y=[value], ax=ax[0,1], color='green')
            ax[0,1].annotate(value, (i * 1000, value), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=6)
        sns.scatterplot(x=[TERMINATION_CRITERION], y=[0], ax=ax[0,1], color='green')
        ax[0,1].annotate(divergence[-1], (TERMINATION_CRITERION, divergence[-1]), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=6)
        # Add label, title and annotates
        ax[0,1].set_xlabel(f'Generation')
        ax[0,1].set_ylabel(f'Divergence')
        ax[0,1].set_title('Convergence curves')

        # Visualise execution time
        sns.lineplot(
            x=range(len(self.record_best_solution)),
            y=[record['execution_time'] for record in self.record_best_solution],
            color='red',
            ax=ax[1,0])
        ax[1,0].set_xlabel('Generation')
        ax[1,0].set_ylabel('Duration (seconds)')
        ax[1,0].set_title(f'Execution Time')

        # More annotation
        ax[1,1].set_title('Parameters')
        txt = ax[1,1].text(.5,.5,
                       f'{best_solution}',
                       ha='center',
                       wrap=True)
        txt._get_wrap_line_width = lambda : 400.
        ax[1,1].annotate(f'Crossover function: {self.crossover_funciton}',
                       xy=(0.5, 0.4),
                       xycoords='axes fraction',
                       ha='center')
        ax[1,1].annotate(f'Replacement function: {self.replacement_function}',
                       xy=(0.5, 0.3),
                       xycoords='axes fraction',
                       ha='center')
        ax[1,1].annotate(f'Mutation function: {self.mutation_function}',
                       xy=(0.5, 0.2),
                       xycoords='axes fraction',
                       ha='center')

        # Save plot
        plt.tight_layout()
        plt.savefig(f'{self.report_dir}/{self.report_name}.png')
        plt.close()

    def run(self):
        # Termination criterion: 10,000 fitness evaluations
        for i in range(1, TERMINATION_CRITERION):
            start_time = time()
            # Record current generation data
            self.report_data.append([])
            self.report_data[i].append(str(i)) # No. of generation

            # Tournament Selection
            parent_a, parent_b = self.ea.tournament_selection(self.tournament_size)

            if parent_a and parent_b:
                self.report_data[i].append(str(parent_a)) # Record parent A
                self.report_data[i].append(str(parent_b)) # Record parent B

                # Crossover
                child_c, child_d = parent_a.crossover(parent_b, operator=self.crossover_funciton)
                self.report_data[i].append(str(child_c)) # Record child C
                self.report_data[i].append(str(child_d)) # Record child D

                # Mutation
                new_solution_e = child_c.mutation(operator=self.mutation_function) # Record new solution E
                new_solution_f = child_d.mutation(operator=self.mutation_function) # Record new solution F

                # Replacement
                replace_index1 = self.ea.replace(new_solution_e, function=self.replacement_function)
                replace_index2 = self.ea.replace(new_solution_f, function=self.replacement_function)
                self.report_data[i].append(str(new_solution_e) + f'- Replace solution {replace_index1} in the population')
                self.report_data[i].append(str(new_solution_f) + f'- Replace solution {replace_index2} in the population')
            
            # Record best solution and period/generation to achieve such solution
            best_solution = self.ea.best_solution()
            if best_solution.fitness >= self.record_best_solution[i - 1]['solution'].fitness:
                self.record_best_solution.append({
                    'generation': self.record_best_solution[i - 1]['generation'],
                    'solution': self.record_best_solution[i - 1]['solution'],
                    'execution_time': time() - start_time
                })
            else:
                self.record_best_solution.append({
                    'generation': i,
                    'solution': best_solution,
                    'execution_time': time() - start_time
                })
            self.report_data[i].append(str(best_solution))
            self.report_data[i].append(str(self.record_best_solution[i]['generation']))
