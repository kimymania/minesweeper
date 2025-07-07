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
                self.board_data[(x, y)] = self._check_for_mines(x, y)
        # Safe squares with value of 0 will be changed to a list of coordinates for safe squares
        for k, v in self.board_data.items():
            if v == 0:
                self.board_data[k] = self._link_safe_squares(k)
        print(self.board_data)

    def _place_mines(self):
        while len(self.__mine_coords) < self.num_of_mines:
            x = random.randint(0, self.size_x - 1)
            y = random.randint(0, self.size_y - 1)
            if (x, y) not in self.displayed:
                self.__mine_coords.add((x, y))

    def _check_for_mines(self, x, y):
        if (x, y) in self.__mine_coords:
            return -1
        count = 0
        # min() and max() to restrict range to valid coordinates
        for j in range(max(0, y - 1), min(y + 2, self.size_y)):
            for i in range(max(0, x - 1), min(x + 2, self.size_x)):
                if (i, j) in self.__mine_coords:
                    count += 1
        return count

    def _link_safe_squares(self, coords):
        linked = []

        def _create_links(x, y):
            if (x, y) in self.__mine_coords or x < 0 or y < 0:
                return
            if 0 <= self.board_data[(x, y)]:
                linked.append((x, y))
            _create_links(x - 1, y - 1)
            _create_links(x - 1, y)
            _create_links(x - 1, y + 1)
            _create_links(x, y - 1)
            _create_links(x, y + 1)
            _create_links(x + 1, y - 1)
            _create_links(x + 1, y)
            _create_links(x + 1, y + 1)

        _create_links(coords[0], coords[1])

        return linked

    def draw(self, end=False, win=None):
        """Clear the screen and (re)draw the board - emulate screen refresh"""
        # os.system("cls" if os.name == "nt" else "clear")
        for y in range(0, self.size_y):
            for x in range(0, self.size_x):
                if (x, y) in self.displayed:  # Needed to draw previous moves as well
                    print(
                        f"[{self.board_data[(x, y)] if self.board_data[(x, y)] else ' '}]",
                        end="",
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
        self.displayed.add(coord)
        # Guard clause to check for player's first move
        if len(self.displayed) == 1:
            self.initialize()

        if self.board_data[coord] == -1:
            self.draw(end=True, win=False)
            print("You stepped on a mine!")
            return 0
        elif len(self.displayed) + self.num_of_mines == self.board_size:
            self.draw(end=True, win=True)
            return 2
        elif isinstance(self.board_data[coord], list):
            # 'Safe' squares (with value '0') contains a list of linked squares instead of a string
            for square in self.board_data[coord]:
                self.unpack_linked_square(square)
            # Return this square's value to 0 after unpacking list
            self.board_data[coord] = 0
            self.draw()
            return 1
        else:
            self.draw()
            return 1

    def unpack_linked_square(self, coord):
        """Unpacks linked squares with value of '0'
        This function was created to handle recursive unpacking of linked squares with value of '0'"""
        self.displayed.add(coord)
        # Recursive call to unpacked linked squares with value of '0'
        if isinstance(self.board_data[coord], list):
            for square in self.board_data[coord]:
                self.unpack_linked_square(square)
                self.board_data[coord] = 0


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
