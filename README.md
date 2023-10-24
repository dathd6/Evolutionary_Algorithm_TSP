# Evolutionary Algorithm: The Travelling Salesman Problem (TSP)

## Disclaimer
- The current code have quite broad range of population 100 to 10000 
  (have tried higher but very long running time and similar result)
  and is the same as tournament size
- We can lower the runnning time by fixed population size and tournament size
  at line 6 and 7 in file `experimentation.py`

## About the code

- Programming language: Python
- Version: 3.11.5

## Dependencies:
    - [matplotlib](https://matplotlib.org)

## File structure:

- main.py: contained the main code to execute the experimentation on finding the best fitness
- constant.py: constant variables
- utils.py: utility functions (find the best fitness, swap gene in chromosome)
- experimentation.py: Experimentation class
    + choose the population/tournament size, crossover/mutation/replacement function
    + Initialize EA and execute the crossover/mutation/replacement through 10,000 generations
    + Generate detail process report
    + Generate image visualise solution's route, convergence curves and execution time
- evolutionary_algorithm.py: EA class
    + Extract data from XML file
    + Generate population of N random solutions
    + Method of replacement function, tournament selection
    + Method of find the best fitness and the top 10 fitness
- tsp.py: TSP solution class
    + Attribute: fitness and route
    + Method of calculate fitness from route
    + Method of crossover/mutation function
- requirements: requirement's packages/libraries
- README.md: Documentation for the code
- datasets/: Folder (datasets) contains data of the map (vertices, edges, cost)
    + brazil58.xml
    + burma14.xml

## How to run

[Install Latest version of Python3](https://www.python.org/downloads/)
[Install virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)

Open terminal and `cd` to the code directory

Create virtualenv
```bash
virtualenv env
```

Activate virtual environment
```bash
source env/bin/activate
```
 
Install dependencies
```bash
pip install -r requirements.txt
```

(OPTIONAL) Printout help option
```bash
python3 main.py --help
```
--> Result:
```bash
usage: main.py [-h] [--data DATA] [--experimentation EXPERIMENTATION]

Evolutionary Algorithm: The Travelling Salesman Problem

options:
  -h, --help                                              show this help message and exit
  --data DATA, -d DATA                                    path to dataset file
  --experimentation EXPERIMENTATION, -e EXPERIMENTATION   number of experimentation
```

Execute the experimentation (change option according to preference)
DEFAULT: 
- data = burma14.xml
- experimentation = 1
```bash
python3 main.py
```
```bash
python3 main.py --data datasets/burma14.xml --experimentation 3
```
```bash
python3 main.py -d datasets/brazil58.xml -e 3
```
--> Result:
```bash
Experimentation 92
- Population size: 3607
- Tournament size: 240
- Crossover function: ordered_crossover
- Mutation function: inversion
- Replacement function: replace_first_weakest
--> Best solution: 28557.0
--> Route: [54, 47, 40, 46, 20, 28, 35, 18, 5, 13, 36, 14, 33, 45, 55, 44, 32, 27, 16, 25, 51, 50, 2, 9, 34, 48, 42, 22, 56, 11, 26, 4, 57, 23, 43, 17, 0, 8, 12, 39, 29, 24, 31, 19, 52, 49, 3, 7, 21, 15, 30, 6, 41, 37, 10, 38, 1, 53]
--> Get the best fitness at generation: 9674 of 10000
```

## Report structure
- reports/
  |
  |__ report_{ID}/
  |   |__ report_[0..N].csv: Details report of the process through out generations
  |   |__ report_[0..N].png: Image of solution's route, convergence curves and execution time
  |
  |__ report_{ID}.csv: Summary report of the best fitness of each experimentations
