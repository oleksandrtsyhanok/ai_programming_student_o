
# Miniùmaal voorbeeld van een agent die verschillende zoekalgoritmen kan gebruiken om problemen op te lossen.
from bfs import bfs
from dfs import dfs
from astar import astar
from annealing import simulated_annealing

class Agent:
    def __init__(self):
        self.tools = {
            "bfs": bfs,
            "dfs": dfs,
            "astar": astar,
            "annealing": simulated_annealing
        }

    # meta-reasoning: kies een tool op basis van probleemkenmerken
    def choose_tool(self, problem):
        # simpele strategie: kies op basis van grootte van het probleem; dit kunnen we nog verbeteren
        size = problem.width * problem.height

        if size <= 25:
            return "bfs"
        elif size <= 100:
            return "astar"
        else:
            return "annealing"

    # Agent loop
    def solve(self, problem, method=None):
        if method is None:
            method = self.choose_tool(problem)

        print(f"[Agent] Using method: {method}")
        return self.tools[method](problem)
