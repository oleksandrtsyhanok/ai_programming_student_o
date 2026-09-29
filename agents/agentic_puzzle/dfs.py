def dfs(problem):
    stack = [(problem.start, [])]
    visited = set()

    while stack:
        state, path = stack.pop()

        if problem.is_goal(state):
            return path + [state]

        if state in visited:
            continue
        visited.add(state)

        for neighbor in problem.neighbors(state):
            stack.append((neighbor, path + [state]))

    return None