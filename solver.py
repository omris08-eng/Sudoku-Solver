import random
import copy    

DIFFICULTY_TO_HIDDEN_PERCENT = {'1': 0.5, '2': 0.55, '3': 0.6, '4': 0.65}  


class Sudoku:
    def __init__(self, size, difficulty):
        """
        Initializes a new Sudoku game object.

        Args:
            size (int): The size of the board must be a perfect square.
            difficulty (str): the desired difficulty level, as a string from '1' to '4'. 
        Raises:
            ValueError: If the size is not a perfect square or if the difficulty level is invalid.
        """
        if int(size ** 0.5) ** 2 != size:
            raise ValueError("The size of the board must be a square number (like 4, 9, 16)")
        if DIFFICULTY_TO_HIDDEN_PERCENT.get(difficulty) is None:
            raise ValueError("The difficulity must be a number from 1 - 4")
        
        self._size = size
        self._block_size = int(size ** 0.5)
        self._hidden_percentage = DIFFICULTY_TO_HIDDEN_PERCENT[difficulty]

        self._board = [[0 for _ in range(self._size)] for _ in range(self._size)]
        self._hidden_board = [[0 for _ in range(self._size)] for _ in range(self._size)]
        self.create_rtp_board()

    def create_rtp_board(self):
        """
        This function will create a board that is 'ready to play'.
        A board will be considered 'ready to play' if:
        1. It is a ly genarted board.
        2. It is a solvable board.
        3. The desired number of cells are hidden, depending on the difficulty level.
        """
        self.generate_solution()

        self._hidden_board = copy.deepcopy(self._board)

        num_to_hide = int((self._size **2) * self._hidden_percentage)

        self.hiding_cells_unique(num_to_hide)

        
    def find_empty(self, board):
        """
        This function will find the next empty cell(a cell that contion a zero) in the sudoku board.
        Returns:
            tuple[int, int] | None: A tuple of the first empty cell found,
                                    or None if the board is full.
        """
        for i in range(self._size):
            for j in range(self._size):
                if board[i][j] == 0:
                    return (i, j)
        return None
        
    def generate_solution(self):
        """
        This function is the core engine of the generator. It fills the board by trying 
        random valid Numbers for each empty cell.

        Returns:
            bool: True if a solution was found, False if the current path is
                a dead end and needs to backtrack. 
        """
        find_next = self.find_empty(self._board)
        if find_next is None:
            return True
        else:
            row,col = find_next

        numbers = list(range(1, self._size + 1))
        random.shuffle(numbers)

        for num in numbers:
            if self.is_valid(self._board, num, find_next):
                self._board[row][col]  = num

                if self.generate_solution():
                    return True
                
                self._board[row][col] = 0

        return False
    
    
    def count_solutions(self,board, limit = 2):
        """
        This function checks that the hidden board has exactly one solution.
        Args:
            limit (int): The limit of the amount of special forces that the function looks for
        """
        find_next = self.find_empty(board)
        if find_next is None:
            return 1
        
        row,col = find_next
        count = 0

        for num in range(1, self._size + 1):
            if self.is_valid(board, num, find_next):
                board[row][col] = num
                
                count += self.count_solutions(board, limit)

                if count >= limit:
                    board[row][col] = 0
                    return limit
                
                board[row][col] = 0

        return count
    def hiding_cells_unique(self, num_to_hide):
        """
        This function hides from the user the number of cells requested 
        depending on the difficulty level of the Sudoku.
        While keeping a single-solution puzzle.
        Args:
            num_to_hide (int): Represents the number of cells to hide.  
        """
        hide_cells = list(range(self._size ** 2))
        random.shuffle(hide_cells)
        i = 0

        while num_to_hide > 0 and i < len(hide_cells):
            hide_cell_row = hide_cells[i] // self._size
            hide_cell_col = hide_cells[i] % self._size


            if self._hidden_board[hide_cell_row][hide_cell_col] != 0:

                saved = self._hidden_board[hide_cell_row][hide_cell_col]
                self._hidden_board[hide_cell_row][hide_cell_col] = 0
                tmp = copy.deepcopy(self._hidden_board)

                if self.count_solutions(tmp, limit= 2) == 1:
                    num_to_hide -= 1
                else:
                    self._hidden_board[hide_cell_row][hide_cell_col] =saved
            i += 1

    def is_valid(self, board, num, location):
        """
        A helper function for the generate solution function 
        whose purpose is to check with rules that the desired number will enter the desired cell 
        according to the Sudoku conditions. 
        """
        row, col = location
        for i in range(self._size):
            if board[row][i] == num:
                return False
        
        for j in range(self._size):
            if board[j][col] == num:
                return False
        
        box_start_row = (row // self._block_size) * self._block_size
        box_start_col = (col // self._block_size) * self._block_size

        for i in range(box_start_row, box_start_row + self._block_size):
            for j in range(box_start_col, box_start_col + self._block_size):
                if board[i][j] == num:
                    return False
        
        return True

    def print_board(self, board):
        """
        Prints the current state of the Sudoku board to the console
        in a readable, grid-like format.
        """
        cell_w = max(1, len(str(self._size))) # 9->1, 16->2, 25->2, 100->3
        line_length = (self._size * (cell_w + 1)) + ((self._block_size - 1)  * 2)

        for i in range(len(board)):
            if i % self._block_size == 0 and i != 0:
                print('-' * line_length)
                
            for j in range(len(board[i])):
                if j % self._block_size == 0 and j != 0:
                    print('| ', end = "")
                
                v = board[i][j]
                if v == 0:
                    print(" ", end=" ")
                else:
                    print(f'{v:>{cell_w}d}', end=' ')
            print()

        
    def player_play(self, location, num):
        """
        Processes a player's move. Checks if the move is valid and updates 
        the player's board if the guess is correct.
        Args:
            location (tuple [int, int]): The (row, col) tubpke for the cell.
            num (int): The number the player wants to place in the cell.
        """
        row, col = location
        if not (0 <= row < self._size and 0 <= col < self._size):
            print("Row/column out of bounds.")
        elif not (1 <= num <= self._size):
            print(f"Number must be 1..{self._size}.") 
        elif self._hidden_board[row][col] != 0:
            print("This cell is already shown. Please choose an empty cell.")   
        elif self._board[row][col] == num:
            self._hidden_board[row][col] = num
            print("Correct choise!")
        else:
            print("Incorrect choise, please try again")

    def player_win(self):
        """
        Checks if the player has won the game.

        Returns:
            bool: True if the player's board matches the solution board, 
                  False otherwise.
        """
        return self._hidden_board == self._board 
       
    def get_hidden_board(self):
        return self._hidden_board
    def get_solved_board(self):
        return self._board
def main():
    while True:
        print("\n--- Sudoku Main menu ---")
        print("1. Generate a new Sudoku puzzle")
        print("2. Exit")

        choise = input('Enter your choise (1 - 2):')
        if choise == '1':
            try:
                size_input = int(input("Enter board size(Must be a square number e.g., 9 or 4)"))
                difficulty_input = str(input("Enter difficulty (1-4): "))

                game = Sudoku(size_input, difficulty_input)

                print("\n Sudoku Puzzel")
                game.print_board(game.get_hidden_board())
                while not game.player_win():
                    
                    print("\nWhat is your next move?")
                    print("1. Guess a number")
                    print("2. Show a solution")
                    print("3. Give up and return to main menu")
                    choise1 = input("Enter your choise (1 - 3): ")
                        
                    if choise1 == '1':
                        try:
                            row = int(input(f"Enter row (1-{game._size}): ")) - 1
                            col = int(input(f"Enter column (1-(1-{game._size}):): ")) - 1
                            num = int(input(f"Enter your guessed number (1-{game._size}): "))

                            game.player_play((row, col), num)
                            game.print_board(game.get_hidden_board())
                        except ValueError:
                            print("\nInvalid input. Please enter numbers only.")
                        except IndexError:
                            print("\nInvalid location. Row/Column out of bounds.")
                    elif choise1 == '2':
                        game.print_board(game.get_solved_board())
                        print("Returning to main menu.")
                        break
                    elif choise1 == '3':
                        print("Returning to main menu.")
                        break

                    else:
                        print("\nInvalid choice. Please enter 1 or 2.")

            except ValueError as e:
                print(f"\n Error: {e}. Please try again")
        
        elif choise == '2':
            print("Thank you for playing. goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter 1 or 2.")
                
if __name__ == "__main__":
    main()
