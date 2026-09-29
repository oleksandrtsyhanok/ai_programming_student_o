import random

class GridProblem:
    def __init__(self, width, height, start, goal, obstacles=None):
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal
        self.obstacles = set(obstacles or [])

    def neighbors(self, state):
        x, y = state
        candidates = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
        valid = []
        for nx, ny in candidates:
            if (0 <= nx < self.width and 0 <= ny < self.height 
                and (nx, ny) not in self.obstacles):
                valid.append((nx, ny))
        return valid

    def is_goal(self, state):
        return state == self.goal

    def heuristic(self, state):
        # Manhattan distance
        return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])