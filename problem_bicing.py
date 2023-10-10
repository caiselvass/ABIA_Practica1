from aima.search import Problem, hill_climbing, simulated_annealing

class ProblemaBicing(Problem):
    def __init__(self, initial_state: EstadoBicing):
        self.expanded_nodes = 0
        super.__init__(initial_state)
        pass


    def actions(self, state: EstadoBicing):
        pass

    def result(self, state: EstadoBicing, action):
        pass

    def path_cost(self, c, state1, action, state2):
        pass
    
    def h(self, node):
        return node.state.heuristic()