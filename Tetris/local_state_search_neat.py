from game import Game
from grid import Grid
from tetrominos import *
from collections import deque

class LocalStateSearch(Game):
    def __init__(self):
        super().__init__()

    def get_all_possible_positions(self):
        possible_positions = {}  # Maps (row, col, rotation) -> move sequence
        visited = set()
        
        # Store original piece state
        original_row = self.current_block.rowoffset
        original_col = self.current_block.coloffset
        original_rotation = self.current_block.rotated
        
        # BFS queue: (row, col, rotation, move_sequence)
        queue = deque([(original_row, original_col, original_rotation, [])])
        visited.add((original_row, original_col, original_rotation))

        while queue:
            row, col, rotation, moves = queue.popleft()

            # Move piece to current state being explored
            self.current_block.rowoffset = row
            self.current_block.coloffset = col
            self.current_block.rotated = rotation

            # Try left/right movements
            for dcol, move in [(-1, "Left"), (1, "Right")]:
                new_row, new_col = row, col + dcol
                new_rotation = rotation
                
                if (new_row, new_col, new_rotation) not in visited:
                    self.current_block.rowoffset = new_row
                    self.current_block.coloffset = new_col
                    self.current_block.rotated = new_rotation
                    
                    if self.is_within_play() and self.allowed_to_move():
                        visited.add((new_row, new_col, new_rotation))
                        queue.append((new_row, new_col, new_rotation, moves + [move]))

            # Try rotations
            max_rotations = len(self.current_block.cells)
            new_rotation = (rotation + 1) % max_rotations
            if (row, col, new_rotation) not in visited:
                self.current_block.rowoffset = row
                self.current_block.coloffset = col
                self.current_block.rotated = new_rotation
                
                if self.is_within_play() and self.allowed_to_move():
                    visited.add((row, col, new_rotation))
                    queue.append((row, col, new_rotation, moves + ["Rotate"]))

            # Try moving down
            new_row = row + 1
            if (new_row, col, rotation) not in visited:
                self.current_block.rowoffset = new_row
                self.current_block.coloffset = col
                self.current_block.rotated = rotation
                
                if self.is_within_play() and self.allowed_to_move():
                    visited.add((new_row, col, rotation))
                    queue.append((new_row, col, rotation, moves + ["Down"]))
                elif (row, col, rotation) not in possible_positions:
                    # Found a final position - piece can't move down anymore
                    possible_positions[(row, col, rotation)] = moves

        # Restore original piece state
        self.current_block.rowoffset = original_row
        self.current_block.coloffset = original_col 
        self.current_block.rotated = original_rotation

        return possible_positions

    def evaluate_move(self, row, col, rotation, weights=[50, -50, -50, -500]):
        """
        Evaluates a potential move based on:
        1. Score from line clears
        2. Number of gaps (empty cells with blocks above)
        3. Mean height of the board
        4. Height deviation across columns
        """
        # Save current state
        original_row = self.current_block.rowoffset
        original_col = self.current_block.coloffset
        original_rotation = self.current_block.rotated
        original_grid = [row[:] for row in self.grid.grid]
        original_score = self.score

        # Move piece to position to evaluate
        self.current_block.rowoffset = row
        self.current_block.coloffset = col
        self.current_block.rotated = rotation

        # Try to place the piece
        cells = self.current_block.get_cell_positions()
        for cell in cells:
            self.grid.grid[cell.row][cell.col] = self.current_block.id
        
        # Calculate evaluation metrics
        gaps = 0
        mean_height = 0.0
        
        # Calculate gaps and mean height
        for col in range(self.grid.col_ct):
            found_block = False
            for row in range(self.grid.row_ct):
                if found_block and self.grid.grid[row][col] == 0:
                    gaps += 1
                if not found_block and self.grid.grid[row][col]:
                    found_block = True
                    mean_height += self.grid.row_ct - row
        
        mean_height /= self.grid.col_ct

        # Calculate height deviation
        height_dev = 0.0
        for col in range(self.grid.col_ct):
            for row in range(self.grid.row_ct):
                if self.grid.grid[row][col]:
                    height_dev += abs(mean_height - (self.grid.row_ct - row))
                    break
        height_dev /= self.grid.col_ct

        # Calculate lines that would be cleared
        lines_cleared = 0
        for row in range(self.grid.row_ct):
            if all(self.grid.grid[row][col] != 0 for col in range(self.grid.col_ct)):
                lines_cleared += 1

        # Calculate score based on lines cleared
        score = 0
        if lines_cleared == 1:
            score = 40
        elif lines_cleared == 2:
            score = 100
        elif lines_cleared == 3:
            score = 300
        elif lines_cleared == 4:
            score = 1200

        # Calculate weighted sum
        fitness = (weights[0] * score + 
                  weights[1] * gaps + 
                  weights[2] * mean_height + 
                  weights[3] * height_dev)

        # Restore original state
        self.current_block.rowoffset = original_row
        self.current_block.coloffset = original_col
        self.current_block.rotated = original_rotation
        self.grid.grid = [row[:] for row in original_grid]
        self.score = original_score

        return fitness

    def get_best_move(self, weights=[50, -500, -50, -600]):
        """
        Finds the best possible move based on position evaluation.
        Returns: (best_position, move_sequence, best_score)
        """
        possible_positions = self.get_all_possible_positions()
        best_score = float('-inf')
        best_position = None
        best_moves = None

        for (row, col, rotation), moves in possible_positions.items():
            score = self.evaluate_move(row, col, rotation, weights)
            if score > best_score:
                best_score = score
                best_position = (row, col, rotation)
                best_moves = moves

        return best_position, best_moves, best_score

    def make_best_move(self):
        """
        Makes a single move from the best move sequence.
        Returns: True if move was made, False if no moves possible
        """
        # Store moves as instance variable if not already present
        if not hasattr(self, 'current_moves') or not self.current_moves:
            _, moves, _ = self.get_best_move()
            if not moves:
                return False
            # Add extra down moves to ensure piece reaches final position
            self.current_moves = moves

        # Execute next move in sequence
        if self.current_moves:
            next_move = self.current_moves.pop(0)
            if next_move == "Left":
                self.move_left()
            elif next_move == "Right":
                self.move_right()
            elif next_move == "Down":
                self.move_down()
                self.score += 1
            elif next_move == "Rotate":
                self.rotate()
            return True
    
        self.current_moves = None
        
        return False