import random
import tkinter as tk
from tkinter import messagebox

class Minesweeper:
    def __init__(self, size=9, mines=10):
        self.size = size
        self.mines = mines
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.visible = [[False for _ in range(size)] for _ in range(size)]
        self.flags = [[False for _ in range(size)] for _ in range(size)]
        self._place_mines()
        self._calculate_numbers()
        self.game_over = False

    def _place_mines(self):
        positions = set()
        while len(positions) < self.mines:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            positions.add((x, y))
        for x, y in positions:
            self.board[x][y] = 'M'

    def _calculate_numbers(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == 'M':
                    continue
                count = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.size and 0 <= ny < self.size:
                            if self.board[nx][ny] == 'M':
                                count += 1
                self.board[x][y] = str(count) if count > 0 else ' '

    def reveal(self, x, y):
        if not (0 <= x < self.size and 0 <= y < self.size):
            return
        if self.game_over or self.visible[x][y] or self.flags[x][y]:
            return
        self.visible[x][y] = True
        if self.board[x][y] == 'M':
            self.game_over = True
            print("Game Over! You hit a mine.")
            self._reveal_all()
            return
        if self.board[x][y] == ' ':
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        if not self.visible[nx][ny]:
                            self.reveal(nx, ny)

    def flag(self, x, y):
        if not (0 <= x < self.size and 0 <= y < self.size):
            return
        if not self.visible[x][y]:
            self.flags[x][y] = not self.flags[x][y]

    def _reveal_all(self):
        for x in range(self.size):
            for y in range(self.size):
                self.visible[x][y] = True

    def print_board(self):
        print("   " + " ".join(str(i) for i in range(self.size)))
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if self.flags[i][j]:
                    row.append('F')
                elif not self.visible[i][j]:
                    row.append('.')
                else:
                    row.append(self.board[i][j])
            print(f"{i:2} " + " ".join(row))

    def check_win(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != 'M' and not self.visible[x][y]:
                    return False
        return True

class MinesweeperUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.buttons = [[None for _ in range(game.size)] for _ in range(game.size)]
        self.create_widgets()
        self.root.geometry(f"{self.game.size * 60}x{self.game.size * 60}")

    def create_widgets(self):
        for x in range(self.game.size):
            for y in range(self.game.size):
                btn = tk.Button(self.root, text='', width=4, height=2, command=lambda x=x, y=y: self.reveal_cell(x, y))
                btn.bind('<Button-3>', lambda e, x=x, y=y: self.toggle_flag(x, y))
                btn.grid(row=x, column=y)
                self.buttons[x][y] = btn

    def reveal_cell(self, x, y):
        self.game.reveal(x, y)
        self.update_board()
        if self.game.game_over:
            messagebox.showinfo("Game Over", "You hit a mine! Game Over!")
            self.reveal_all()
        elif self.game.check_win():
            messagebox.showinfo("Congratulations", "You win!")

    def toggle_flag(self, x, y):
        self.game.flag(x, y)
        self.update_board()

    def update_board(self):
        colors = {
            '1': '#0000FF',  # Blue
            '2': '#008000',  # Green
            '3': '#FF0000',  # Red
            '4': "#290383",  # Purple
            '5': '#800000',  # Maroon
            '6': '#40E0D0',  # Turquoise
            '7': "#FFFFFF",  # White
            '8': '#808080'   # Gray
        }
        for x in range(self.game.size):
            for y in range(self.game.size):
                btn = self.buttons[x][y]
                if self.game.flags[x][y]:
                    btn.config(text='F', state='normal', bg='white', fg='black', 
                             font=('Helvetica', 12, 'bold'), relief='solid', borderwidth=1)
                elif self.game.visible[x][y]:
                    value = self.game.board[x][y]
                    if value != ' ' and value != 'M':
                        color = colors.get(value, '#000000')
                        btn.config(text=value, state='disabled', bg='black', fg=color, 
                                 font=('Helvetica', 12, 'bold'), relief='solid', borderwidth=1)
                    elif value == 'M':
                        btn.config(text='M', state='disabled', bg='red', fg='black', 
                                 font=('Helvetica', 12, 'bold'), relief='solid', borderwidth=1)
                    else:
                        btn.config(text='', state='disabled', bg='black', fg='white', 
                                 font=('Helvetica', 12, 'bold'), relief='solid', borderwidth=1)
                else:
                    btn.config(text='', state='normal', bg='white', fg='black', 
                             font=('Helvetica', 12, 'bold'), relief='solid', borderwidth=1)

    def reveal_all(self):
        for x in range(self.game.size):
            for y in range(self.game.size):
                self.game.visible[x][y] = True
        self.update_board()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper()
    app = MinesweeperUI(root, game)
    root.mainloop()

#To run the game in a console, uncomment the following lines:

"""def main():
    game = Minesweeper()
    while not game.game_over:
        game.print_board()
        if game.check_win():
            print("Congratulations! You win!")
            break
        move = input("Enter move (r x y to reveal, f x y to flag): ").split()
        if len(move) != 3:
            print("Invalid input.")
            continue
        cmd, x, y = move
        try:
            x, y = int(x), int(y)
            if not (0 <= x < game.size and 0 <= y < game.size):
                print("Out of bounds.")
                continue
        except ValueError:
            print("Invalid coordinates.")
            continue
        if cmd == 'r':
            game.reveal(x, y)
        elif cmd == 'f':
            game.flag(x, y)
"""