"""
Oefening 2: Sliding Puzzle (8-puzzle)
======================================
Implementeer de sliding puzzle en los hem op met BFS/DFS.
"""

import numpy as np
from collections import deque


class SlidingPuzzle:
    GRIDSIZE = 3
    EMPTY = 0

    GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def __init__(self, game):
        self.Game = np.array(game)

    def verschuiven(self, dy, dx):
        copy = self.Game.copy()
        null_pos = self.locate_empty()
        temp = copy[null_pos[0] + dy][null_pos[1] + dx]
        copy[null_pos[0] + dy][null_pos[1] + dx] = 0
        copy[null_pos[0]][null_pos[1]] = temp
        return copy

    def possible_new_configurations(self):
        # TODO: geef alle nieuwe configuraties door het lege vakje te verschuiven
        new_configs = []
        UP = (-1, 0)
        DOWN = (1, 0)
        LEFT = (0, -1)
        RIGHT = (0, 1)

        null_pos = self.locate_empty()
        if null_pos[0] < 2:
            down = self.verschuiven(DOWN[0], DOWN[1])  # DOWN
            new_configs.append(down)

        if null_pos[0] > 0:
            up = self.verschuiven(UP[0], UP[1])  # UP
            new_configs.append(up)

        if null_pos[1] < 2:
            right = self.verschuiven(RIGHT[0], RIGHT[1])  # RIGHT
            new_configs.append(right)

        if null_pos[1] > 0:
            left = self.verschuiven(LEFT[0], LEFT[1])  # LEFT
            new_configs.append(left)

        return new_configs

    def locate_empty(self):
        for row in range(self.GRIDSIZE):
            for col in range(self.GRIDSIZE):
                if self.Game[row][col] == self.EMPTY:
                    return (row, col)
        raise Exception("Geen leeg vakje!")

    def manhattan_distance(self):
        # TODO: bereken de Manhattan-afstand tot de goal-configuratie
        null_poss = self.locate_empty()
        cost = abs(2 - null_poss[0]) + abs(2 - null_poss[1])
        return cost

    def is_goal(self):
        return np.array_equal(self.Game, self.GOAL)

    def duplicate(self):
        return SlidingPuzzle(
            [
                [self.Game[r][c] for c in range(self.GRIDSIZE)]
                for r in range(self.GRIDSIZE)
            ]
        )

    def log(self):
        print("---")
        for row in self.Game:
            print(", ".join(str(int(x)) for x in row))
        print("---")


def solve_puzzle(start_puzzle: SlidingPuzzle):
    # TODO: los de puzzel op met BFS
    puzzle = start_puzzle
    frontier = deque([start_puzzle])
    explored = set()
    while frontier:
        node = frontier.popleft()
        if node.is_goal():
            return node
        explored.add(tuple(node.Game.flat))
        for config in node.possible_new_configurations():
            config = SlidingPuzzle(config)
            check = tuple(config.Game.flat)
            if check not in explored:
                frontier.append(config)

    return None


if __name__ == "__main__":
    game = [[1, 2, 3], [4, 5, 0], [7, 8, 6]]
    puzzle = SlidingPuzzle(game)
    print("Startconfiguratie:")
    puzzle.log()

    oplossing = solve_puzzle(puzzle)
    print("Oplossing:", oplossing.log())
