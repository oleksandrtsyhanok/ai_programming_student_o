import heapq

def astar(problem):
    open_list = []
    heapq.heappush(open_list, (0, problem.start, []))
    visited = set()

    while open_list:
        cost, state, path = heapq.heappop(open_list)

        if problem.is_goal(state):
            return path + [state]

        if state in visited:
            continue
        visited.add(state)

        for neighbor in problem.neighbors(state):
            g = len(path) + 1
            h = problem.heuristic(neighbor)
            heapq.heappush(open_list, (g + h, neighbor, path + [state]))

    return None