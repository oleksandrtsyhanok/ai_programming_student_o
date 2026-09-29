from collections import deque

def bfs(problem):
    queue = deque([(problem.start, [])])
    visited = set()

    while queue:
        state, path = queue.popleft()

        if problem.is_goal(state):
            return path + [state]

        if state in visited:
            continue
        visited.add(state)

        for neighbor in problem.neighbors(state):
            queue.append((neighbor, path + [state]))

    return None