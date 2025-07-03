"""
CLI Minesweeper game in Python

1. Add time counter
"""

import os
import random


class GameBoard:
    def __init__(self, size_x, size_y, num_of_mines):
        self.size_x = size_x
        self.size_y = size_y
        self.board_size = size_x * size_y
        self.num_of_mines = num_of_mines
        self.__mine_coords = set()
        self.board_data = {}
        self.played = set()

    def initialize(self):
        self._place_mines()
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.board_data[(x, y)] = self._check_for_mines(x, y)

    def _place_mines(self):
        while len(self.__mine_coords) < self.num_of_mines:
            x = random.randint(0, self.size_x - 1)
            y = random.randint(0, self.size_y - 1)
            if (x, y) not in self.played:
                self.__mine_coords.add((x, y))

    def _check_for_mines(self, x, y):
        if (x, y) in self.__mine_coords:
            return "X"
        count = 0
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                if (i, j) in self.__mine_coords:
                    count += 1
        return str(count)

    def draw(self, end=False, win=None):
        """Clear the screen and (re)draw the board - emulate screen refresh"""
        os.system("cls" if os.name == "nt" else "clear")
        for y in range(0, self.size_y):
            for x in range(0, self.size_x):
                if (x, y) in self.played:
                    print(
                        f"[{self.board_data[(x, y)] if self.board_data[(x, y)] else ' '}]",
                        end="",
                    )
                else:
                    if end and (x, y) in self.__mine_coords:
                        print("[.]" if win else "[M]", end="")
                    else:
                        print("[ ]", end="")
            else:
                print()

    def select_square(self, coord: tuple[int, int]):
        """This is the entry point for player's move.
        self.played keeps track of selected squares."""
        self.played.add(coord)
        if len(self.played) == 1:  # This is only activated on player's first move
            self.initialize()

        if self.board_data[coord] == "X":
            self.draw(end=True, win=False)
            print("You stepped on a mine!")
            return 0
        elif len(self.played) + self.num_of_mines == self.board_size:
            self.draw(end=True, win=True)
            return 2
        else:
            self.draw()
            return 1


def main():
    # Initialize board
    board_x, board_y = 10, 10
    max_mines = round(board_x * board_y * 0.2)
    while True:
        num_of_mines = input("Number of mines: ").strip()
        try:
            num_of_mines = int(num_of_mines)
            if 0 > num_of_mines or num_of_mines > max_mines:
                print(f"Number of mines has to be between 0 and {max_mines}")
                continue
            break
        except ValueError as e:
            print(f"Enter a valid whole number: {e}")
    board = GameBoard(board_x, board_y, num_of_mines)
    board.draw()

    # Play game
    while True:
        select = input("Select a coordinate (x,y): ").strip()
        select = select.split(",")
        if len(select) > 2:
            print("Input a valid coordinate format (x,y)")
            continue
        try:
            x = int(select[0])
            y = int(select[1])
            coord = x, y
        except ValueError as e:
            print(f"x and y values must be whole numbers: {e}")
            continue
        if not 0 <= x < board_x or not 0 <= y < board_y:
            print(
                f"Coordinates must be in the range of (0,0) to ({board_x - 1},{board_y - 1})"
            )
            continue

        # Check game state
        result = board.select_square(coord)
        if not result:
            break
        if result == 2:
            print("Congratulations! You've sweeped all the mines!")
            break


if __name__ == "__main__":
    main()
