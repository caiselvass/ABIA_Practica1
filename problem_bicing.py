from aima.search import Problem
from state_bicing import EstadoBicing
from typing import Generator


class ProblemaBicing(Problem):
    def __init__(self, initial_state: EstadoBicing):
        self.solutions_checked = 0
        super().__init__(initial_state)

    def actions(self, state: EstadoBicing) -> Generator:
        return state.generate_actions()

    def result(self, state: EstadoBicing, action) -> EstadoBicing:
        return state.apply_action(action)

    def path_cost(self, c, state1, action, state2) -> int:
        return c + 1
    
    def value(self, state: EstadoBicing) -> float:
        self.solutions_checked += 1
        return state.heuristic()
    
    def goal_test(self, state: EstadoBicing) -> bool:
        return False