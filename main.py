import os
import csv
import argparse
# Components & Constants
from constants import REPORT_FOLDER, TERMINATION_CRITERION
from experimentation import Experimentation

if __name__ == '__main__':
    if not os.path.exists(REPORT_FOLDER):
        os.mkdir(REPORT_FOLDER)
    # Add options as parameters to the code
    parser = argparse.ArgumentParser(description="Evolutionary Algorithm: The Travelling Salesman Problem")
    parser.add_argument("--data", "-d", help="Path to dataset file", default="datasets/burma14.xml")
    parser.add_argument("--experimentation", "-e", help="Number of experimentation", default=1)
    parser.add_argument("--test_best_population", "-tbp", help="Test best population", action='store_true')
    args = parser.parse_args()

    report = []
    report_name = None
    # Run N experimentation (Finding the best route)
    for i in range(int(args.experimentation)):
        # Initial random population of solutions
        exp = Experimentation(args.data, args.test_best_population)
        print(f'\nExperimentation {i + 1}')
        print(exp)
        # Execute EA
        exp.run()
        last_record = exp.record_best_solution[-1]
        if last_record['generation'] == 0 and args.test_best_population:
            continue
        # Generate report - record process of selection, crossover, mutation, and replacement
        exp.report_generate()
        # Generate image visualize best optimized route and Top 10 best fitness of the population
        exp.visualise()
        # Record data of current experimentation
        exp_data = [i + 1, 
                    exp.population_size,
                    exp.tournament_size,
                    exp.replacement_function,
                    exp.mutation_function,
                    exp.crossover_funciton ,
                    str(last_record["solution"].route),
                    last_record["solution"].fitness,
                    last_record['generation']]
        print('--> Best solution:', last_record["solution"].fitness)
        print('--> Route:', last_record["solution"].route)
        print('--> Get the best fitness at generation:', f"{last_record['generation']} of {TERMINATION_CRITERION}")
        report.append(exp_data)
        report_name = exp.ea.city

    if os.path.exists(f'{REPORT_FOLDER}/final_report_{report_name}.csv'):
        with open(f'{REPORT_FOLDER}/final_report_{report_name}.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            row_count = -1
            for _ in reader:
                row_count += 1
            for i, row in enumerate(report):
                if i != 0:
                    row[0] = row[0] + row_count

        with open(f'{REPORT_FOLDER}/final_report_{report_name}.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            flag = True
            for row in reader:
                # Pass first row
                if flag:
                    flag = False
                    continue
                row[-1] = float(row[-1])
                row[-2] = float(row[-2])
                report.append(row)

    # Write all record data of experimentations into csv file (sort by Fitness & Generation that achieve best fitness)
    with open(f'{REPORT_FOLDER}/final_report_{report_name}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # Final report columns
        writer.writerow(['No.',
                         'Population Size',
                         'Tournament Size',
                         'Replacement Function',
                         'Mutation Function',
                         'Crossover Function',
                         'Optimize route',
                         'Best Fitness' ,
                         'Generation that achieve best fitness'])
        # Open and read the CSV file
        report.sort(key=lambda data: (data[-2], data[-1]))
        writer.writerows(report)
