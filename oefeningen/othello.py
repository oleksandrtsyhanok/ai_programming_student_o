
import random
import colorama
import art

class Othello():
    def __init__(self) -> None:
        self.board = [[" " for _ in range(8)] for _ in range(8)]
        self.initialize_board()
        self.player = 'X' # je kan dit aanpassen zodat jij begint en niet de computer

    def print_colored_board(self):
        colorama.init()
        for row in self.board:
            colored_row = [colorama.Fore.GREEN + cell + colorama.Fore.RESET if cell == "X" else colorama.Fore.RED + cell + colorama.Fore.RESET if cell == "O" else cell for cell in row]
            print(" ".join(colored_row))

    def print_board(self):
            horizontal_line = "+---+---+---+---+---+---+---+---+"
            print(horizontal_line)
            for row in self.board:
                print("| {} | {} | {} | {} | {} | {} | {} | {} |".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                print(horizontal_line)

    def initialize_board(self):
        

        # dit creërt de startpositie
        self.board[3][3] = self.board[4][4] = "O"
        self.board[3][4] = self.board[4][3] = "X"

    def is_valid_move(self, row, col, player=None):
        if (player == None):
            player = self.player
        if self.board[row][col] != " ":
            return False

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        # in alle richtingen rond het punt kijken
        for dr, dc in directions:
            r, c = row, col
            r += dr
            c += dc
            if not (0 <= r < 8) or not (0 <= c < 8):
                continue
            # als de steen in deze richting van de tegenspeler is, checken of er ergens verder een eigen steen ligt
            if self.board[r][c] == self.opponent():
                r += dr
                c += dc
                while (0 <= r < 8) and (0 <= c < 8):
                    # de reeks is onderbroken, geen goede plaats om te leggen
                    if self.board[r][c] == " ":
                        break
                    # hier ligt een eigen steen
                    if self.board[r][c] == player:
                        return True
                    r += dr
                    c += dc
        return False

    def opponent(self):
        if self.player == "X":
            return "O"
        else:
            return "X"
        
    def change_player(self):
        #print('changed_player')
        self.player = self.opponent()

    def make_move(self, row, col, player):
        if self.is_valid_move(row, col, player):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            #steen leggen
            self.board[row][col] = player

            #en alle tussenliggende stenen omdraaien
            for dr, dc in directions:
                r, c = row, col
                r += dr
                c += dc
                while (0 <= r < 8) and (0 <= c < 8):
                    if self.board[r][c] == " ":
                        break
                    # steen van eigen kleur
                    if self.board[r][c] == player:
                        #achterwaarts teruglopen en stenen omdraaien
                        while (r != row) or (c != col):
                            r -= dr
                            c -= dc
                            self.board[r][c] = player
                        break
                    r += dr
                    c += dc
        self.change_player()

    def count_pieces(self):
        x_count = sum(row.count("X") for row in self.board)
        o_count = sum(row.count("O") for row in self.board)
        return x_count, o_count
    
    def check_end(self):
        if not any(self.is_valid_move(row, col, self.player) for row in range(8) for col in range(8)):
            if not any(self.is_valid_move(row, col, self.opponent()) for row in range(8) for col in range(8)):
                return True
            else:
                return False
        else:
            return False

    def random_move(self):
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == ' ':
                    if self.is_valid_move(i,j, self.player):
                        possible_moves.append((i,j))
        
        random.shuffle(possible_moves)
        return possible_moves[0]
    
    def evaluate(self):
        # dit is onze utility functie
        x_count, o_count = self.count_pieces()
        if (self.check_end()):
            if x_count > o_count:
                return 1000
            elif x_count < o_count:
                return -1000
            else:
                return 0
        else:
            # simpele versie: dit werkt niet goed, omdat het spel net zoals Go veel over en weer kan gaan qua aantallen
            return (x_count - o_count)
        
            #geavanceerde versie
            #TODO

    #de volgende functies dienen om een slimme utility functie (evaluate) op te stellen
    #je wil in essentie stabiele coins
    # # je wil mogelijkheid om te 'bewegen' 
    # actual mobility: aantal mogelijke next moves: dit kun je rechtstreeks tellen
    # potential mobility: aantal moves over een aantal mogelijke stappen. sommige huidige illegale moves kunnen plots wel lukken
    # potential mobility wordt geteld als lege vakjes naast een opponents coin (ruwe telling!)
    # corners captured: dit geeft veel stabiliteit
    # stability van een corner (stable, semi stable, unstable (direct inneembaar))
    # 
        

    def minimax(self, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        # dit implementeert het minimax algoritme
        score = self.evaluate()

        if self.check_end():
            return score
        elif (depth == 0):
            return score

        if is_maximizing:
            best = float('-inf') # laag genoeg beginnen
            for i in range(8):
                for j in range(8):
                    if (self.board[i][j] == ' ' and self.is_valid_move(i,j)):
                        # X invullen en checken wat er dan precies zou gebeuren, recursieve definitie
                        new_move = self.copy()
                        new_move.make_move(i,j, 'X')
                        best = max(best, new_move.minimax(depth - 1, not is_maximizing, alpha, beta)) #tegengestelde positie
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            break # alpha pruning
            return best
        else:
            best = float('inf') # hoog genoeg beginnen
            for i in range(8):
                for j in range(8):
                    if (self.board[i][j] == ' ' and self.is_valid_move(i,j)):
                        new_move = self.copy()
                        new_move.make_move(i,j, 'O')
                        best = min(best, new_move.minimax(depth - 1, not is_maximizing, alpha, beta))
                        beta = min(beta, best)
                        if beta < alpha:
                            break # beta pruning
            return best
        
    def find_best_move(self):
        best_val = float('-inf')
        best_move = (-1, -1)
        
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == ' ':
                    if self.is_valid_move(i, j, self.player):
                        new_move = self.copy()
                        new_move.make_move(i,j, self.player)
                        move_val = new_move.minimax(5, False)
                        if move_val > best_val:
                            best_move = (i, j)
                            best_val = move_val
        return best_move
        
    def copy(self):
        game = Othello()
        for i in range(8):
            for j in range(8):
                game.board[i][j] = self.board[i][j]
        return game

def play():
    # Create ASCII art
    ascii_art = art.text2art("Othello")
    print(ascii_art)
    game = Othello()

    while True:
        game.print_colored_board()
        x_count, o_count = game.count_pieces()
        print(f"X: {x_count}, O: {o_count}")

        if not any(game.is_valid_move(row, col, game.player) for row in range(8) for col in range(8)):
            print("Geen geldige zetten meer voor de huidige speler.")
            game.change_player()
            if not any(game.is_valid_move(row, col, game.player) for row in range(8) for col in range(8)):
                print("Geen enkele geldige zet meer. Game over.")
                x_count, o_count = game.count_pieces()
                if x_count > o_count:
                    print("X wint!")
                elif x_count < o_count:
                    print("O wint!")
                else:
                    print("Gelijkstand!")
                break

        while True:
            #check of het aan de computer is
            if (game.player == 'X'):
                print("Computer gaat een zet doen:")
                
                row, col = game.find_best_move()
                game.make_move(row, col, game.player)
                game.print_board()
            else:
                print("Manuele speler gaat een zet doen:")
                try:
                    print("Speler " + game.player + ", kies een zet.")
                    row, col = map(int, input("Enter je zet (rij SPATIE kolom): ").split())
                    if game.is_valid_move(row, col, game.player):
                        game.make_move(row, col, game.player)
                        break
                    else:
                        print("Ongeldige input.")
                except ValueError:
                    print("Ongeldige input. Geef twee getallen in zoals 0 0 voor het item helemaal linksbovenaan.")

if __name__ == "__main__":
    play()
