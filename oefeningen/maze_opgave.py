import numpy as np

class Maze:
    def __init__(self, size, start, end, walls):
        self.size = size
        self.start = start
        self.end = end
        self.maze = np.zeros(size, dtype=str)
        self.maze[:, :] = '.'
        self.maze[start] = 'S'
        self.maze[end] = 'E'
        for wall in walls:
            self.maze[wall] = '#'


    def valid_moves(self, current):
        pass

    def extract_path(self, stack):
        pass

    def print_maze(self):
        for row in self.maze:
            print(' '.join(row))

def find_path(maze):
    pass

# Voorbeeld gebruik:
maze_size = (10, 10)
start_point = (0, 0)
end_point = (9, 9)
walls = [(2, 1), (2, 2), (2, 3), (4, 6), (6, 6), (7, 6), (8, 6), (4, 7), (4, 8),
         (2,2), (5,2), (6,2), (4,2), (3,2), (8,0), (9, 6), (1,8), (2,8), (6,9), (7,9),
         (3,6), (3,7), (4,1), (5,1)]

my_maze = Maze(maze_size, start_point, end_point, walls)
path, steps = find_path(my_maze)

my_maze.print_maze()
print("Path:", path)
print("Steps:", steps)