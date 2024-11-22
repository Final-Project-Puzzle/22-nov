import random
from typing import Dict, List, Tuple, Set, Optional

def generate_sudoku() -> Dict[Tuple[int, int], int]:
    #Generate a random valid Sudoku puzzle and return it as a dictionary
    def fill_board() -> List[List[int]]:
        #fill the rest + valid check
        board = [[0] * 9 for _ in range(9)]
        rows, cols, boxes = [set() for _ in range(9)], [set() for _ in range(9)], [set() for _ in range(9)]
        
        def is_valid(num: int, row: int, col: int) -> bool:
            box_index = (row // 3) * 3 + (col // 3)
            return (num not in rows[row] and num not in cols[col] and num not in boxes[box_index])

        def fill() -> bool:
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        random_nums = list(range(1, 10))
                        random.shuffle(random_nums)
                        for num in random_nums:
                            if is_valid(num, i, j):
                                board[i][j] = num
                                rows[i].add(num)
                                cols[j].add(num)
                                boxes[(i // 3) * 3 + (j // 3)].add(num)
                                if fill():
                                    return True
                                board[i][j] = 0
                                rows[i].remove(num)
                                cols[j].remove(num)
                                boxes[(i // 3) * 3 + (j // 3)].remove(num)
                        return False
            return True

        fill()
        return board

    def remove_numbers(board: List[List[int]], clues: int = 40):
        cells_to_remove = 81 - clues
        positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(positions)
        for r, c in positions[:cells_to_remove]:
            board[r][c] = 0

    filled_board = fill_board()
    remove_numbers(filled_board)
    return {(i, j): filled_board[i][j] for i in range(9) for j in range(9)}

def solve_sudoku(board_dict: Dict[Tuple[int, int], int], use_backtracking: bool = True) -> Optional[List[List[int]]]:
    #fault tolerant algorithm

    def initialize_sets() -> Tuple[Dict[int, Set[int]], Dict[int, Set[int]], Dict[int, Set[int]], List[Tuple[int, int]]]:
        rows = {i: set() for i in range(9)}
        cols = {i: set() for i in range(9)}
        boxes = {i: set() for i in range(9)}
        empty_cells = []
        
        for (i, j), num in board_dict.items():
            if num != 0:
                rows[i].add(num)
                cols[j].add(num)
                boxes[(i // 3) * 3 + (j // 3)].add(num)
            else:
                empty_cells.append((i, j))
        
        return rows, cols, boxes, empty_cells
    

    rows, cols, boxes, empty_cells = initialize_sets()
    
    def naked_singles():
        
        changed = True
        while changed:
            changed = False
            for (i, j) in empty_cells[:]:  # iterate over a copy of empty cells
                possible_values = {
                    num for num in range(1, 10)
                    if num not in rows[i] and num not in cols[j] and num not in boxes[(i // 3) * 3 + (j // 3)]
                }
                if len(possible_values) == 1:  # Only one possible value
                    num = possible_values.pop()
                    board_dict[(i, j)] = num
                    rows[i].add(num)
                    cols[j].add(num)
                    boxes[(i // 3) * 3 + (j // 3)].add(num)
                    empty_cells.remove((i, j))
                    changed = True
        return not empty_cells  # Return True if solved

    def constraint_propagation() -> bool:
        changed = True
        try:
            while changed:
                changed = False
                for (i, j) in empty_cells[:]:
                    possible_values = {
                        num for num in range(1, 10)
                        if num not in rows[i] and num not in cols[j] and num not in boxes[(i // 3) * 3 + (j // 3)]
                    }
                    if len(possible_values) == 1:
                        num = possible_values.pop()
                        board_dict[(i, j)] = num
                        rows[i].add(num)
                        cols[j].add(num)
                        boxes[(i // 3) * 3 + (j // 3)].add(num)
                        empty_cells.remove((i, j))
                        changed = True
            return not empty_cells
        except Exception as e:
            print(f"Error during constraint propagation: {e}")
            return False

    def backtracking(i: int, empty_cells: List[Tuple[int, int]], rows: Dict[int, Set[int]], 
                     cols: Dict[int, Set[int]], boxes: Dict[int, Set[int]], board_dict: Dict[Tuple[int, int], int]) -> bool:
        if i == len(empty_cells):
            return True

        row, col = empty_cells[i]
        box_index = (row // 3) * 3 + (col // 3)
        for num in range(1, 10):
            if num not in rows[row] and num not in cols[col] and num not in boxes[box_index]:
                board_dict[(row, col)] = num
                rows[row].add(num)
                cols[col].add(num)
                boxes[box_index].add(num)
                if backtracking(i + 1, empty_cells, rows, cols, boxes, board_dict):
                    return True
                board_dict[(row, col)] = 0
                rows[row].remove(num)
                cols[col].remove(num)
                boxes[box_index].remove(num)
        return False

    if constraint_propagation():
        print("Solved using constraint propagation.")
    elif use_backtracking and backtracking(0, empty_cells, rows, cols, boxes, board_dict):
        print("Solved using backtracking.")
    else:
        print("Failed to solve.")
        return None

    return [[board_dict[(i, j)] for j in range(9)] for i in range(9)]

# Generate a random Sudoku puzzle
sudoku_board_dict = generate_sudoku()

# User choice for enabling backtracking
while True:
    user_input = input("Enable backtracking if constraint propagation fails? (0 for off, 1 for on): ").strip()
    if user_input in {'0', '1'}:
        use_backtracking = user_input == '1'
        break
    else:
        print("Invalid input. Please enter either 0 or 1.")

# Solve the puzzle
solved_board = solve_sudoku(sudoku_board_dict, use_backtracking=use_backtracking)
if solved_board:
    for row in solved_board:
        print(row)

#to add: 1. naked pairs, 2. user choice for which method to use or either can be used, 3. for app to show with which method it has been solved if "either" has been chosen

