import os
import argparse
import warnings
from time import time
# Components & Constants
from constants import REPORT_FOLDER, TERMINATION_CRITERION
from experimentation import Experimentation
from utils import generate_summary_report, \
                  visualize_summary_graph, \
                  visualize_operators_comparision, \
                  visualize_population_and_tournament_size_comparision

warnings.filterwarnings("ignore", category=UserWarning)

if __name__ == '__main__':
    # Create report folder if not existed
    if not os.path.exists(REPORT_FOLDER):
        os.mkdir(REPORT_FOLDER)
    # Add options as parameters to the code
    parser = argparse.ArgumentParser(description="Evolutionary Algorithm: The Travelling Salesman Problem")
    parser.add_argument("--data", "-d", help="Path to dataset file", default="datasets/burma14.xml")
    parser.add_argument("--experimentation", "-e", help="Number of experimentation", default=1)
    parser.add_argument("--exploit", "-ex", help="Exploit EA by utilizing recorded solution", action='store_true')
    args = parser.parse_args()

    report = []
    report_name = None
    # Run N experimentation (Finding the best route)
    for i in range(int(args.experimentation)):
        start_time = time()
        # Initial random population of solutions
        exp = Experimentation(args.data, args.exploit)
        print(f'\nExperimentation {i + 1}')
        print(exp)
        # Execute EA
        exp.run()
        last_record = exp.record_best_solution[-1]
        # If EA can't find the best solution while running exploit the fittest -> not record the solution
        if last_record['generation'] == 0 and args.exploit:
            continue
        # Generate image visualize best optimized route and Top 10 best fitness of the population
        exp.visualise()
        # Record data of current experimentation
        no = round(len(os.listdir(exp.report_dir))) - 1
        exp_data = [no, 
                    exp.population_size,
                    exp.tournament_size,
                    exp.replacement_operator,
                    exp.mutation_operator,
                    exp.crossover_operator ,
                    time() - start_time,
                    str(last_record["solution"].route),
                    last_record["solution"].fitness,
                    last_record['generation']]
        print('--> Best solution:', last_record["solution"].fitness)
        print('--> Route:', last_record["solution"].route)
        print('--> Get the best fitness at generation:', f"{last_record['generation']} of {TERMINATION_CRITERION}")
        report.append(exp_data)
        report_name = exp.ea.country

    if report_name:
        generate_summary_report(f'{REPORT_FOLDER}/report_{report_name}.csv', report)
        visualize_operators_comparision(f'{REPORT_FOLDER}/operators_comparision_{report_name}.png', report)
        visualize_summary_graph(f'{REPORT_FOLDER}/summary_graph_{report_name}.png', report)
        visualize_population_and_tournament_size_comparision(
            f'{REPORT_FOLDER}/population_and_tournament_size_comparision_{report_name}.png', 
            report
        )
