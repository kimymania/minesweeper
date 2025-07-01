"""
CLI Minesweeper game in Python

1. OOP
2. Reloading view every turn
3. Random deployment of mines
4. Deployment rules
"""

import random


class GameBoard:
    def __init__(self, size_x, size_y, num_of_mines):
        self.size_x = size_x
        self.size_y = size_y
        self.num_of_mines = num_of_mines
        self.mine_coords = set()
        self.played = set()
        self.place_mines()

    def place_mines(self):
        while len(self.mine_coords) < self.num_of_mines:
            x = random.randint(0, self.size_x - 1)
            y = random.randint(0, self.size_y - 1)
            self.mine_coords.add((x, y))
        print(self.mine_coords)  # for debugging purposes

    def draw(self, dead=False):
        for y in range(0, self.size_y):
            for x in range(0, self.size_x):
                if (x, y) in self.played:
                    print(
                        f"[{self.get_hint(x, y)}]",
                        end="",
                    )
                else:
                    print(
                        "[M]" if dead and (x, y) in self.mine_coords else "[ ]", end=""
                    )
            else:
                print()

    def select_square(self, coord: tuple[int, int]):
        self.played.add(coord)
        if coord in self.mine_coords:
            self.draw(dead=True)
            print("You stepped on a mine!")
            return False
        else:
            self.draw()
            return True

    def get_hint(self, x, y):
        if (x, y) in self.mine_coords:
            return "X"
        count = 0
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if (i, j) in self.mine_coords:
                    count += 1
        return count


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

        # Check for mine in selected coordinate
        if not board.select_square(coord):
            break


if __name__ == "__main__":
    main()
