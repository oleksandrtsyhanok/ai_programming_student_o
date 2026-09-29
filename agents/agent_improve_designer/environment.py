class TicTacToe:
    def __init__(self):
        self.board = [" "] * 9

    def copy(self):
        new = TicTacToe()
        new.board = self.board[:]
        return new

    def available_actions(self):
        return [i for i, v in enumerate(self.board) if v == " "]

    def make_move(self, action, player):
        if self.board[action] == " ":
            self.board[action] = player
            return True
        return False

    def check_winner(self):
        wins = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,b,c in wins:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return self.board[a]
        if " " not in self.board:
            return "draw"
        return None