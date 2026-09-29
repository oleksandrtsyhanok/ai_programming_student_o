import random
import math

def simulated_annealing(problem, max_iter=1000):
    current = problem.start
    current_cost = problem.heuristic(current)

    path = [current]

    for t in range(1, max_iter):
        T = max(0.01, min(1.0, 1.0 - t / max_iter))

        neighbors = problem.neighbors(current)
        if not neighbors:
            return path

        next_state = random.choice(neighbors)
        next_cost = problem.heuristic(next_state)

        delta = current_cost - next_cost

        if delta > 0 or random.random() < math.exp(delta / T):
            current = next_state
            current_cost = next_cost
            path.append(current)

        if problem.is_goal(current):
            return path

    return path
