"""
CLI Minesweeper game in Python

1. Open adjacent squares if safe
2. Add time counter
"""

# import os
import random


class GameBoard:
    def __init__(self, size_x, size_y, num_of_mines):
        self.size_x = size_x
        self.size_y = size_y
        self.board_size = size_x * size_y
        self.num_of_mines = num_of_mines
        self.__mine_coords = set()
        self.board_data = {}
        self.displayed = set()

    def initialize(self):
        self._place_mines()
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.board_data[(x, y)] = self._fill_mine_count(x, y)

    def _place_mines(self):
        while len(self.__mine_coords) < self.num_of_mines:
            x = random.randint(0, self.size_x - 1)
            y = random.randint(0, self.size_y - 1)
            if (x, y) not in self.displayed:
                self.__mine_coords.add((x, y))

    def _fill_mine_count(self, x, y):
        if (x, y) in self.__mine_coords:
            return -1
        count = 0
        # min() and max() to restrict range to valid coordinates
        for j in range(max(0, y - 1), min(y + 2, self.size_y)):
            for i in range(max(0, x - 1), min(x + 2, self.size_x)):
                if (i, j) in self.__mine_coords:
                    count += 1
        return count

    def draw(self, end=False, win=False):
        """Clear the screen and (re)draw the board - emulate screen refresh"""
        # os.system("cls" if os.name == "nt" else "clear")
        for y in range(0, self.size_y):
            for x in range(0, self.size_x):
                if (x, y) in self.displayed and (x, y) in self.__mine_coords:
                    print("[X]", end="")
                elif (x, y) in self.displayed:  # Needed to draw previous moves as well
                    print(
                        f"[{int(self.board_data[(x, y)]) if self.board_data[(x, y)] >= 0 else ' '}]",
                        end="",  # Need to change to int() in case of float values created by get_safe_squares function
                    )
                else:
                    if end and (x, y) in self.__mine_coords:
                        print("[.]" if win else "[M]", end="")
                    else:
                        print("[ ]", end="")  # Default behaviour
            else:
                print()

    def select_square(self, coord: tuple[int, int]):
        """This is the entry point for player's move.
        self.displayed keeps track of selected squares."""
        # Guard clause to check for player's first move
        if len(self.displayed) == 0:
            self.displayed.add(coord)
            self.initialize()
        elif coord in self.displayed:
            print("Square already selected")
            return 1
        else:
            self.displayed.add(coord)

        if self.board_data[coord] == -1:
            self.draw(end=True)
            print("You stepped on a mine!")
            return 0
        elif len(self.displayed) + self.num_of_mines == self.board_size:
            self.draw(end=True, win=True)
            return 2
        elif self.board_data[coord] == 0:
            self.get_safe_squares(coord)
            self.draw()
            return 1
        else:
            self.draw()
            return 1

    def get_safe_squares(self, coord):
        """Recursive flood fill algorithm for linking safe squares
        if selected square has no mines in adjacent squares.
        Used float() type to exclude previously visited squares from recursion."""

        def check(x, y):
            if (
                (x, y) in self.__mine_coords
                or not 0 <= x < self.size_x
                or not 0 <= y < self.size_y
            ):
                return
            if isinstance(self.board_data[(x, y)], float):
                return
            if 0 <= self.board_data[(x, y)]:
                self.displayed.add((x, y))
                self.board_data[(x, y)] = float(self.board_data[(x, y)])
            if self.board_data[(x, y)] == 0:
                check(x - 1, y - 1)
                check(x - 1, y)
                check(x - 1, y + 1)
                check(x, y + 1)
                check(x, y - 1)
                check(x + 1, y - 1)
                check(x + 1, y)
                check(x + 1, y + 1)

        check(*coord)


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
        except IndexError as e:
            print(
                f"x and y values must be between 0 and {board_x - 1, board_y - 1}: {e}"
            )
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
