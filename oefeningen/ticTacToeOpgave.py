import copy

class Node:
    def __init__(self):
        self.TurnPlayer1 = None
        self.Actions = []

    def Utility(self):
        pass

    def MaximinValue(self):
        pass

    def MinimaxValue(self):
        pass

    def PossibleMoves(self):
        pass

    def TerminalTest(self):
        pass

    def GameFinishedWithoutWinner(self):
        pass

    def Log(self):
        pass

class Edge:
    def __init__(self, from_node, to_node):
        self.FromNode = from_node
        self.ToNode = to_node

class Problem:
    def __init__(self):
        self.InitialState = None

class TicTacToeBoard(Node):
    EMPTY = " "
    PLAYER1 = "X"
    PLAYER2 = "O"

    def __init__(self, initial_board, turn_player1):
        super().__init__()
        self.Board = initial_board
        self.TurnPlayer1 = turn_player1

    def PossibleMoves(self):
        pass

    def Duplicate(self):
        new_game = copy.deepcopy(self.Board)
        return new_game

    def TerminalTest(self):
        for row in range(3):
            if self.Board[row][0] == self.Board[row][1] == self.Board[row][2] and self.Board[row][0] != self.EMPTY:
                return True

        for col in range(3):
            if self.Board[0][col] == self.Board[1][col] == self.Board[2][col] and self.Board[0][col] != self.EMPTY:
                return True

        if self.Board[0][0] == self.Board[1][1] == self.Board[2][2] and self.Board[0][0] != self.EMPTY:
            return True

        if self.Board[0][2] == self.Board[1][1] == self.Board[2][0] and self.Board[0][2] != self.EMPTY:
            return True

        return False

    def GameFinishedWithoutWinner(self):
        if self.TerminalTest():
            return False  # There is a winner

        for row in range(3):
            for col in range(3):
                if self.Board[row][col] == self.EMPTY:
                    return False  # Game not finished

        return True

    def Log(self):
        print("---")
        for row in self.Board:
            print(",".join(row))
        print("---")

class MinimaxSearch:
    def MinimaxDecision(self, possible_moves):
        pass

class Program:
    @staticmethod
    def Main():
        algorithm = MinimaxSearch()

        initial_board = [
            [TicTacToeBoard.EMPTY, TicTacToeBoard.EMPTY, TicTacToeBoard.EMPTY],
            [TicTacToeBoard.EMPTY, TicTacToeBoard.EMPTY, TicTacToeBoard.EMPTY],
            [TicTacToeBoard.EMPTY, TicTacToeBoard.EMPTY, TicTacToeBoard.EMPTY]
        ]

        curr_state = TicTacToeBoard(initial_board, True)
        while not curr_state.TerminalTest() and not curr_state.GameFinishedWithoutWinner():
            curr_state = algorithm.MinimaxDecision(curr_state.PossibleMoves())

            curr_state.Log()

            if curr_state.TerminalTest() or curr_state.GameFinishedWithoutWinner():
                break

            print("Give row,column:")
            row, col = map(int, input().split(","))

            curr_board_config = curr_state.Duplicate()
            curr_board_config[row][col] = TicTacToeBoard.PLAYER2

            curr_state = TicTacToeBoard(curr_board_config, True)
            curr_state.Log()

        print("Game done")

if __name__ == "__main__":
    Program.Main()
