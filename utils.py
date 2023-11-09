import csv
import os
import random
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
from constants import PARTIALLY_MAPPED_CROSSOVER, ORDERED_CROSSOVER, SEQUENTIAL_CONSTRUCTIVE_CROSSOVER
from constants import REPLACE_FIRST_WEAKEST, REPLACE_WEAKEST
from constants import SINGLE_SWAP_MUTATION, INVERSION

list_crossovers = [
    PARTIALLY_MAPPED_CROSSOVER,
    ORDERED_CROSSOVER,
    SEQUENTIAL_CONSTRUCTIVE_CROSSOVER
]

list_replacements = [
    REPLACE_WEAKEST,
    REPLACE_FIRST_WEAKEST
]

list_mutations = [
    SINGLE_SWAP_MUTATION,
    INVERSION
]

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

def visualize_population_and_tournament_size_comparision(file, report):
    # Only filtered combination of operators to compare:
    # - Sequential Constructive Crossover
    # - Inversion Mutation
    # - Replace Weakest
    filtered_report = [row for row in report if row[3] == REPLACE_WEAKEST and row[4] == INVERSION and row[5] == SEQUENTIAL_CONSTRUCTIVE_CROSSOVER]
    if len(filtered_report) == 0:
        return
    fig, ax = plt.subplots(1, 2, figsize=(15, 10))
    fig.suptitle(f'Population/Tournament size trade-offs\n \
                 {REPLACE_WEAKEST} - {INVERSION} - {SEQUENTIAL_CONSTRUCTIVE_CROSSOVER}')
    execution_time = [float(row[-4]) for row in filtered_report]
    fitness = [int(row[-2]) for row in filtered_report]
    population_size = [int(row[1]) for row in filtered_report]
    tournament_size = [int(row[2]) for row in filtered_report]

    sns.scatterplot(x=population_size,
                    y=tournament_size,
                    hue=execution_time,
                    palette="flare",
                    legend=False,
                    ax=ax[0])
    sns.scatterplot(x=population_size,
                    y=tournament_size,
                    hue=fitness,
                    palette="flare",
                    legend=False,
                    ax=ax[1])

    ax[0].set_title("Correlation between execution time\n and population/tournament size")
    ax[0].set_xlabel("population size")
    ax[0].set_ylabel("tournament size")
    ax[1].set_title("Correlation between fitness\n and population/tournament size")
    ax[1].set_xlabel("population size")
    ax[1].set_ylabel("tournament size")

    # Create a colorbar axis and add colorbar
    cax1 = plt.cm.ScalarMappable(cmap="flare", norm=plt.Normalize(vmin=min(execution_time), vmax=max(execution_time)))
    cax1.set_array([])
    cax2 = plt.cm.ScalarMappable(cmap="flare", norm=plt.Normalize(vmin=min(fitness), vmax= max(fitness)))
    cax2.set_array([])
    cbar1 = plt.colorbar(cax1, ax=ax[0])
    cbar2 = plt.colorbar(cax2, ax=ax[1])
    cbar1.set_label("Execution Time (s)")
    cbar2.set_label("Fitness")

    plt.savefig(file)
    plt.close()

def visualize_summary_graph(file, report):
    fig, ax = plt.subplots(1, 2, figsize=(12, 8))
    fig.suptitle(f"Final Summary", wrap=True)

    # Best fitness from each experiment
    best_solution = report[0]
    execution_time = 0
    for row in report:
        execution_time += float(row[-4])

    sns.lineplot(
        x=[int(row[0]) for row in report],
        y=[row[-2] for row in report],
        color='#3274A1',
        label='fitness',
        ax=ax[0])
    sns.scatterplot(x=[int(best_solution[0])], y=[best_solution[-2]], ax=ax[0], color='#E1812C')
    ax[0].annotate(best_solution[-2], (int(best_solution[0]), best_solution[-2]), textcoords="offset points", xytext=(0, -10), ha='center', fontsize=6, color='#E1812C', weight='bold')
    ax[0].set_ylabel(f'Fitness')
    ax[0].set_xlabel(f'Experiments')
    ax[0].set_title(f'Best fitness from each Experiment')

    # Execution time each experiment
    sns.lineplot(
        x=[int(row[0]) for row in report],
        y=[float(row[-4]) for row in report],
        color='#CC241D',
        label='time',
        ax=ax[1])
    ax[1].set_ylabel(f'Execution time (s)')
    ax[1].set_xlabel(f'Experiments')
    ax[1].set_title(f'Execution Time each experiments {execution_time} seconds')

    plt.savefig(file)
    plt.close()
    

def visualize_operators_comparision(file, report):
    fig = plt.figure(figsize=(10, 10))
    gs = gridspec.GridSpec(2, 2)
    ax1 = plt.subplot(gs[:, 1])
    ax2 = plt.subplot(gs[0, 0])
    ax3 = plt.subplot(gs[1, 0])
    fig.suptitle(f"Operators comparision", wrap=True)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    x = []
    y1 = []
    y2 = []
    for crossover in list_crossovers:
        for mutation in list_mutations:
            for replacement in list_replacements:
                # Filtered the combination of operators to compare the average
                filtered_report = [[rank + 1] + x for rank, x in enumerate(report) if x[3] == replacement and x[4] == mutation and x[5] == crossover]
                if len(filtered_report) == 0:
                    continue
                c = ""
                if crossover == PARTIALLY_MAPPED_CROSSOVER:
                    c = "PMX"
                elif crossover == SEQUENTIAL_CONSTRUCTIVE_CROSSOVER:
                    c = "SCX"
                elif crossover == ORDERED_CROSSOVER:
                    c = "OX"
                m = "".join([word[0] for word in mutation.split(' ')])
                r = "".join([word[0] for word in replacement.split(' ')])
                x.append(f'* {c} * {m} * {r} *')
                generation_average = 0
                fitness_average = 0
                for record in filtered_report:
                   generation_average +=  record[-1] 
                   fitness_average += record[-2]
                if len(filtered_report) == 0:
                    y1.append(0)
                    y2.append(0)
                else:
                    y1.append(round(generation_average / len(filtered_report)))
                    y2.append(round(fitness_average / len(filtered_report)))

                # Plot all the possible (best) solution from previous execution
                # using this specific crossover, mutation and replacement function
                sns.scatterplot(
                    x=[record[-1] for record in filtered_report],
                    y=[record[-2] for record in filtered_report],
                    ax=ax1,
                    s=[record[0] + 10 for record in filtered_report],
                    label=f'* {c} * {m} * {r} *'
                )
                best_solution = filtered_report[0]
                if best_solution[0] == 1:
                    ax1.annotate(f'{best_solution[0]} (best solution)', (best_solution[-1], best_solution[-2]), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=6, color='red')
                else:
                    ax1.annotate(best_solution[0], (best_solution[-1], best_solution[-2]), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=6)
                ax1.set_title(f'Objective space - solutions categorized by operators')
                ax1.set_xlabel('Generations')
                ax1.set_ylabel('Fitness')
    
    sns.barplot(x=x, y=y2, ax=ax2, label='fitness', color='#3274A1')
    sns.barplot(x=x, y=y1, ax=ax3, label='generation', color='#E1812C')
    ax3.set_ylabel('Generations')
    ax3.set_title('Comparision of the Average Generation to converge by Operators')
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, fontsize=8, ha='right')

    ax2.set_ylabel('Fitness')
    ax2.set_title('Comparision of the Average Best Fitness by Operators')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, fontsize=8, ha='right')

    custom_legend_labels = ['Solution']
    custom_legend_markers = [Line2D([0], [0], marker='o', color='w', label='Solution', markerfacecolor='g', markersize=10)]
    # Save plot
    fig.legend(custom_legend_markers, custom_legend_labels, loc='upper right')
    plt.tight_layout()
    plt.savefig(file)
    plt.close()

def generate_summary_report(file, report):
    if os.path.exists(file):
        with open(file, 'r', newline='') as f:
            reader = csv.reader(f)
            flag = True
            for row in reader:
                # Pass first row
                if flag:
                    flag = False
                    continue
                # Change data from string to float
                # to sort and plot graph
                row[-1] = float(row[-1])
                row[-2] = float(row[-2])
                report.append(row)


    # Write all record data of experimentations into csv file (sort by Fitness & Generation that achieve best fitness)
    with open(file, mode='w', newline='') as f:
        writer = csv.writer(f)
        # Final report columns
        writer.writerow(['No.',
                         'Population Size',
                         'Tournament Size',
                         'Replacement Function',
                         'Mutation Function',
                         'Crossover Function',
                         'Execution Time',
                         'Optimize route',
                         'Best Fitness' ,
                         'Generation that achieve best fitness'])
        # Open and read the CSV file
        report.sort(key=lambda data: (data[-2], data[-1]))
        writer.writerows(report)
