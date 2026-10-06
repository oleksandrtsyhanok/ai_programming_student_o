"""
Oefening 3: Maze met DFS
=========================
Implementeer DFS om een weg door het maze te vinden.
"""

import numpy as np
from collections import deque


class Node:
    def __init__(self, state: tuple, parent: "Node | None" = None):
        self.state = state
        self.parent = parent


class Maze:
    def __init__(self, size, start, end, walls):
        self.size = size
        self.start = start
        self.end = end
        self.maze = np.zeros(size, dtype=str)
        self.maze[:, :] = "."
        self.maze[start] = "S"
        self.maze[end] = "E"
        self.walls = walls
        for wall in walls:
            self.maze[wall] = "#"

    def valid_moves(self, current):
        # TODO: geef lijst van (rij,kolom)-coördinaten die geldig zijn
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        valid = []
        for move in moves:
            new = (current[0] + move[0], current[1] + move[1])
            if new[0] not in range(self.size[0]) or new[1] not in range(self.size[1]):
                continue
            if new in self.walls:
                continue
            valid.append(new)
        return valid

    def extract_path(self, stack: Node):
        # TODO: haal het pad uit de stack van start tot end
        path = []
        while stack is not None:
            path.append(stack.state)
            stack = stack.parent

        path.reverse()
        return path, len(path) - 1

    def print_maze(self):
        for row in self.maze:
            print(" ".join(row))


def find_path(maze: Maze):
    # TODO: implementeer DFS met een stack
    init_node: Node = Node(maze.start)

    explored = set()
    frontier = deque([init_node])

    while frontier:
        node = frontier.pop()

        if node.state == maze.end:
            a = maze.extract_path(node)
            return a

        explored.add(node)
        possible_moves = maze.valid_moves(node.state)
        # print(f"{possible_moves} \n")
        # print(explored)
        for move in possible_moves:
            if move not in [n.state for n in explored]:
                new = Node(move)
                frontier.append(new)
                if new.parent is None:
                    new.parent = node

    return None, 0


if __name__ == "__main__":
    maze_size = (10, 10)
    start_point = (0, 0)
    end_point = (9, 9)
    walls = [
        (2, 1),
        (2, 2),
        (2, 3),
        (4, 6),
        (6, 6),
        (7, 6),
        (8, 6),
        (4, 7),
        (4, 8),
        (2, 2),
        (5, 2),
        (6, 2),
        (4, 2),
        (3, 2),
        (8, 0),
        (9, 6),
        (1, 8),
        (2, 8),
        (6, 9),
        (7, 9),
        (3, 6),
        (3, 7),
        (4, 1),
        (5, 1),
    ]

    my_maze = Maze(maze_size, start_point, end_point, walls)
    # my_maze.valid_moves(start_point)
    pad, stappen = find_path(my_maze)

    my_maze.print_maze()
    print("Pad:", pad)
    print("Stappen:", stappen)
