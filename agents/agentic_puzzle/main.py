from problem import GridProblem
from agent import Agent

def print_path(path):
    if path is None:
        print("No solution found")
    else:
        print("Path length:", len(path))
        print(path)


if __name__ == "__main__":
    # create problem
    obstacles = {(1,1), (1,2), (2,1)}
    problem = GridProblem(
        width=5,
        height=5,
        start=(0,0),
        goal=(4,4),
        obstacles=obstacles
    )

    agent = Agent()

    # --- Test each algorithm explicitly ---
    for method in ["bfs", "dfs", "astar", "annealing"]:
        print(f"\n=== {method.upper()} ===")
        path = agent.solve(problem, method=method)
        print_path(path)

    # --- Let agent decide automatically ---
    print("\n=== AGENT CHOICE ===")
    path = agent.solve(problem)
    print_path(path)