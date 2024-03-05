# Bicing Station Optimization Project

## Project Overview
This project aims to optimize the distribution of bicycles across bicing stations in a city to meet expected demand using local search algorithms, specifically Hill Climbing and Simulated Annealing. The goal is to minimize transportation costs while ensuring that all possible bicycles are moved according to predictions for each station.

## Setup Instructions

### Prerequisites
- Python 3.x
- Pygame (for route visualization)
- The `abia_bicing.py` file (containing `Estacion` and `Estaciones` classes) must be in the same folder as `main.py`.

### Running Experiments
1. Open `main.py`. This file contains the main logic for executing experiments.
2. Starting from line 70, you'll find commented-out function calls for experiment execution, formatted as `experimentoX()`, where X is the experiment number.
3. To run an experiment, uncomment the desired function call. Make sure to leave other lines (variable declarations, etc.) as they are, since they contain experiment results and parameters used in other experiments.
4. For Experiment 5, execute it twice, once for each heuristic:
   - Open `parameters_bicing.py`.
   - Modify the `params` object's `coste_transporte` parameter to `False` for heuristic 1 or `True` for heuristic 2.

### Individual Algorithm Execution
After completing the experiments, you can run individual instances of the Hill Climbing algorithm with a single replica to observe the route visualization in Pygame and check the `__repr__()/__str__()` outputs for both the initial and final states.
- To switch heuristics for any run, adjust the `coste_transporte` parameter in `parameters_bicing.py` as mentioned above.

## Visualization
Utilize Pygame to visualize the routes and distributions created by the algorithms, providing an interactive way to observe the optimization process in action.

## Contributions
This project showcases the application of local search algorithms to real-world logistics and urban planning problems, demonstrating the potential of AI in improving city services and infrastructure.
