import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self):
        self.current_player = "X"
        self.board = [" " for _ in range(9)]
        self.computer = "O"
        self.player = "X"

        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.root, text=" ", font=("Arial", 50), width=10, height=4,
                                command=lambda x=i, y=j: self.handle_click(x, y))
                button.grid(row=i, column=j, padx=10, pady=10)
                row.append(button)
            self.buttons.append(row)

        self.status_label = tk.Label(
            self.root, text=f"Current player: {self.current_player}", font=("Arial", 14))
        self.status_label.grid(row=3, column=0, columnspan=3, pady=20)


    def start(self):
        self.root.mainloop()

    def handle_click(self, x, y):
        if self.board[x*3+y] == " ":
            self.board[x*3+y] = self.current_player
            self.buttons[x][y].configure(text=self.current_player)
            if self.check_win():
                print(f"{self.current_player} wins!")
                quit()
            elif self.check_tie():
                print("Its a Tie")
                quit()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.configure(
                    text=f"Current player: {self.current_player}")
                if self.current_player == self.computer:
                    self.compMove()

    def check_win(self):
        # Check rows
        for i in range(3):
            if self.board[i*3] == self.board[i*3+1] == self.board[i*3+2] != " ":
                return True
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != " ":
                return True
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != " ":
            return True
        if self.board[2] == self.board[4] == self.board[6] != " ":
            return True
        return False

    def check_tie(self):
        return " " not in self.board
    
    


    def compMove(self):
        bestScore = -1000
        bestMove = 0

        if self.board[4] == ' ':
            self.update_board(4, self.computer)
            return

        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = self.computer
                score = self.minimax(self.board, 0, False)
                self.board[i] = ' '
                if score > bestScore:
                    bestScore = score
                    bestMove = i

        self.update_board(bestMove, self.computer)
        return
    
    def minimax(self, board, depth, isMaximizing):
        winner = self.check_winner()
        draw = self.check_draw()
                
        if winner == self.computer:
            return 1 
        elif winner == self.player:
            return -1 
        elif draw:
            return 0 
                
        if isMaximizing:
            bestScore = -1000000000000

            for i in range(len(board)):
                if board[i] == ' ':
                    board[i] = self.computer
                    score = self.minimax(board, depth+1, False)
                    board[i] = ' '
                    if score > bestScore:
                        bestScore = score

            return bestScore
                
        else:
            bestScore = 100000000000
            bestMove = 0 
                
            for i in range(len(board)):
                if board[i] == ' ':
                    board[i] = self.player
                    score = self.minimax(board, depth+1, True)
                    board[i] = ' '
                    if score < bestScore:
                        bestScore = score

            return bestScore



    def update_board(self, position, mark):
        self.board[position] = mark
        self.buttons[position//3][position%3].config(text=mark)
        self.check_game_over()

    def check_winner(self):
        # Check rows
        for i in range(3):
            if self.board[i*3] == self.board[i*3+1] == self.board[i*3+2] != " ":
                return self.board[i*3]
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != " ":
                return self.board[i]
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != " ":
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != " ":
            return self.board[2]
        return None

    def check_draw(self):
        return " " not in self.board and not self.check_winner()

    def check_game_over(self):
        if self.check_win():
            print(f"{self.current_player} wins!")
            quit()
        elif self.check_tie():
            print("It's a tie!")

            quit()
        else:
            if self.current_player == self.player:
                self.current_player = self.computer
                self.status_label.configure(text=f"Current player: {self.current_player}")
                self.compMove()
            else:
                self.current_player = self.player
                self.status_label.configure(text=f"Current player: {self.current_player}")

    def play(self):
        print("Welcome to Tic Tac Toe!")

        while not self.game_over:
            # Player's move
            self.player_move()
            self.print_board()
            if self.check_game_over():
                break

            # Computer's move
            print("Computer is thinking...")
            best_score = -1000000000000
            best_move = None
            for i in range(len(self.board)):
                if self.board[i] == ' ':
                    self.board[i] = self.computer
                    score = self.minimax(0, False)
                    self.board[i] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = i

            self.board[best_move] = self.computer
            print(f"Computer played on {best_move}")
            self.print_board()
            if self.check_game_over():
                break

        print("Game over!")
        self.print_board()
        if self.winner == 'draw':
            print("It's a draw!")
        else:
            print(f"{self.winner} won!")

if __name__ == '__main__':
    game = TicTacToe()
    game.start()
