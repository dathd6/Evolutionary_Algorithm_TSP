import os
import random
import matplotlib.pyplot as plt
import seaborn as sns
from time import time
# Components & Constants
from evolutionary_algorithm import EA
from constants import BRAZIL, REPORT_FOLDER, \
                      TERMINATION_CRITERION, \
                      POPULATION_RANGE, \
                      TOURNAMENT_DIVIDE_RANGE, \
                      VISUAL_MAP_DATA_RANGE
from utils import list_mutations, list_crossovers, list_replacements

class Experimentation:
    def __init__(self, dataset, exploit_evolutionary_algorithm=None):
        # Create EA instance to initialise population of solutions
        # Random the parameters to add randomness to each execution
        self.ea = EA(dataset)
        self.population_size = random.randint(*POPULATION_RANGE)
        self.ea.generate_random_population_p(self.population_size)
        if exploit_evolutionary_algorithm:
            self.ea.generate_best_population()
            self.population_size = len(self.ea.population)
        self.tournament_size =  round(self.population_size / random.randint(*TOURNAMENT_DIVIDE_RANGE))
        self.replacement_operator = random.choice(list_replacements)
        self.mutation_operator = random.choice(list_mutations)
        self.crossover_operator = random.choice(list_crossovers)
        # Add sample data (random) to visualise cities & route
        self.visualise_data = [
            (random.randint(*VISUAL_MAP_DATA_RANGE), random.randint(*VISUAL_MAP_DATA_RANGE))
            for _ in range(self.ea.vertex_count)
        ]
        # Create report directory
        # Check if report folder for current country is created
        self.report_dir = f'{REPORT_FOLDER}/report_{self.ea.country}'
        if not os.path.exists(self.report_dir):
            os.mkdir(self.report_dir)
        # Generate a new filename for current experimentation's report
        # including name for csv & png files
        self.report_name = f'report_{round(len(os.listdir(self.report_dir))) + 1}'
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
- Crossover operator: {self.crossover_operator}
- Mutation operator: {self.mutation_operator}
- Replacement operator: {self.replacement_operator}"""

    def visualise(self):
        # Only visualize the last record (Best fitness)
        record = self.record_best_solution[-1]
        best_solution = record['solution']
        # Create 2x2 plot
        fig, ax = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f"TSP - Experimentation {self.report_name}", wrap=True)

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
        sns.lineplot(
            x=[x1, x2],
            y=[y1, y2],
            color=colors[-1],
            linewidth=2,
            marker='o',
            markersize=15,
            markeredgecolor='black',
            ax=ax[0,0])
        for i in range(len(self.visualise_data) - 1):
            x1, y1 = self.visualise_data[best_solution.route[i]]
            x2, y2 = self.visualise_data[best_solution.route[i + 1]]
            sns.lineplot(
                x=[x1, x2],
                y=[y1, y2],
                color=colors[i],
                linewidth=2,
                marker='o',
                markersize=15,
                markeredgecolor='black',
                ax=ax[0,0])
        # Add label, title and annotates
        ax[0,0].set_title(f'Route of best solution {best_solution.fitness}')
        ax[0,0].set_xlabel(f'Population Size of {self.population_size}')
        ax[0,0].set_ylabel(f'Tournament Size of {self.tournament_size}')

        # convergence curves
        list_best_fitness = [record['solution'].fitness for record in self.record_best_solution]
        sns.lineplot(
            x=range(TERMINATION_CRITERION),
            y=list_best_fitness,
            color='#3274A1',
            ax=ax[0,1])
        sns.scatterplot(x=[record['generation']], y=[best_solution.fitness], ax=ax[0,1], color='#E1812C')
        ax[0,1].annotate(
            best_solution.fitness,
            (record['generation'], best_solution.fitness),
            textcoords="offset points",
            xytext=(10, 5),
            ha='center',
            color='#E1812C')
        y_offset = 5000 if self.ea.country == BRAZIL else 500
        # Add a vertical line (from the x-axis to the point)
        ax[0,1].vlines(x=record['generation'], color='#919AA1', linestyle='--', ymin=best_solution.fitness - y_offset, ymax=best_solution.fitness)
        # Add a horizontal line (from the y-axis to the point)
        ax[0,1].hlines(y=best_solution.fitness, color='#919AA1', linestyle='--', xmin=0 ,xmax=record['generation']) 
        # Add label, title
        ax[0,1].set_xlabel(f'Generations')
        ax[0,1].set_ylabel(f'Fitness of the best solution')
        ax[0,1].set_title('Convergence curves')

        # Visualise execution time
        sns.lineplot(
            x=range(0, len(self.record_best_solution)),
            y=[record['execution_time'] for record in self.record_best_solution],
            color='#cc241d',
            ax=ax[1,0])
        ax[1,0].set_xlabel('Generations')
        ax[1,0].set_ylabel('Duration (s)')
        ax[1,0].set_title(f'Execution Time {record["execution_time"]}s')

        # More annotation
        ax[1,1].set_title('Parameters')
        route = str(best_solution.route)[1:-1].replace(",", " >")
        txt = ax[1,1].text(.5,.5,
                       f'{route}',
                       ha='center',
                       wrap=True)
        txt._get_wrap_line_width = lambda : 400.
        ax[1,1].annotate(f'Crossover operator: {self.crossover_operator}',
                       xy=(0.5, 0.4),
                       xycoords='axes fraction',
                       ha='center')
        ax[1,1].annotate(f'Replacement operator: {self.replacement_operator}',
                       xy=(0.5, 0.3),
                       xycoords='axes fraction',
                       ha='center')
        ax[1,1].annotate(f'Mutation operator: {self.mutation_operator}',
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

            # Tournament Selection
            parent_a, parent_b = self.ea.tournament_selection(self.tournament_size)

            if parent_a and parent_b:
                # Crossover
                child_c, child_d = parent_a.crossover(parent_b, operator=self.crossover_operator)

                # Mutation
                new_solution_e = child_c.mutation(operator=self.mutation_operator) # Record new solution E
                new_solution_f = child_d.mutation(operator=self.mutation_operator) # Record new solution F

                # Replacement
                self.ea.replace(new_solution_e, operator=self.replacement_operator)
                self.ea.replace(new_solution_f, operator=self.replacement_operator)
            
            # Record best solution, execution time and period/generation to achieve such solution
            best_solution = self.ea.best_solution()
            end_time = time()
            if best_solution >= self.record_best_solution[i - 1]['solution']:
                self.record_best_solution.append({
                    'generation': self.record_best_solution[i - 1]['generation'],
                    'solution': self.record_best_solution[i - 1]['solution'],
                    'execution_time': self.record_best_solution[i - 1]['execution_time'] + (end_time - start_time)
                })
            else:
                self.record_best_solution.append({
                    'generation': i,
                    'solution': best_solution,
                    'execution_time': self.record_best_solution[i - 1]['execution_time'] + (end_time - start_time)
                })
