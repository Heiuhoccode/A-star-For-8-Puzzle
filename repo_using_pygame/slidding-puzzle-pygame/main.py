import pygame
import random
import time
from sprite import *
from settings import *
from astar_solver import solve_puzzle

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.shuffle_time = 0
        self.start_shuffle = False
        self.previous_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        self.high_score = float(self.get_high_scores()[0])
        
        # Solution variables
        self.solution_path = []
        self.solution_index = -1
        self.show_solution = False
        self.current_heuristic = "manhattan"  # Default heuristic
        
        # A* execution time tracking
        self.astar_execution_time = 0
        
        # Manual input variables
        self.input_mode = False
        self.input_matrix = [[0 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
        self.input_goal_matrix = [[0 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
        self.current_input_pos = [0, 0]  # Row, Col for current input
        self.input_error = ""
        self.used_numbers = set()
        self.input_matrix_active = True  # True for initial matrix, False for goal matrix
        
        # Terminal for solution steps
        self.terminal = Terminal(0, GAME_SIZE * TILESIZE + 200, WIDTH / 3, TERMINAL_HEIGHT)

    def get_high_scores(self):
        with open("high_score.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    def save_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score))

    def create_game(self):
        grid = [[x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
        # grid = [[1,2,3],[4,5,6],[8,7,0]]
        grid[-1][-1] = 0
        return grid

    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                                                                       self.tiles_grid[row][col]
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                                                                       self.tiles_grid[row][col]

    def solve_with_astar(self):
        # Get the target state (completed grid)
        goal_state = self.tiles_grid_completed
        
        # Clear previous solution steps
        self.terminal.clear()
        self.terminal.add_line("Starting A* search with heuristic: " + self.current_heuristic)
        
        # Measure execution time
        start_time = time.time()
        
        # Use A* solver to find solution with selected heuristic
        self.solution_path = solve_puzzle(self.tiles_grid, goal_state, self.current_heuristic)
        
        # Calculate execution time
        self.astar_execution_time = time.time() - start_time
        
        self.solution_index = 0
        self.show_solution = True
        
        # Output solution info to terminal
        if len(self.solution_path) > 0:
            self.terminal.add_line(f"Solution found with {len(self.solution_path)} steps!")
            self.terminal.add_line(f"Execution time: {self.astar_execution_time:.6f} seconds")
            self.terminal.add_line("Use Next/Previous buttons to navigate through solution")
            self.terminal.add_line("-" * 50)
            
            # Display the initial state
            self.terminal.add_line("Initial state:")
            self._add_state_to_terminal(self.tiles_grid)
        else:
            self.terminal.add_line("No solution found!")
        
        # Save the results to a file (keep this intact)
        self.save_solve_data(self.tiles_grid, goal_state, self.current_heuristic, self.astar_execution_time, len(self.solution_path))
        
        # If solution found, return True
        return len(self.solution_path) > 0
        
    def save_solve_data(self, initial_state, goal_state, heuristic, exec_time, steps_number):
        # Convert 2D matrices to 1D arrays for saving
        initial_flat = []
        for row in initial_state:
            initial_flat.extend(row)
            
        goal_flat = []
        for row in goal_state:
            goal_flat.extend(row)
            
        # Format the data as: heuristic,execution_time,initial_state,goal_state
        data_line = f"{heuristic},{exec_time:.6f},{steps_number},{initial_flat},{goal_flat}\n"
        
        # Append to file
        with open("astar_results.txt", "a") as file:
            file.write(data_line)
            
    def _add_state_to_terminal(self, state):
        """Add a formatted state representation to the terminal"""
        for row in state:
            line = "| " + " | ".join([str(cell) if cell != 0 else " " for cell in row]) + " |"
            self.terminal.add_line(line)
        self.terminal.add_line("")  # Add empty line after state

    def apply_solution_step(self, step_index):
        if 0 <= step_index < len(self.solution_path):
            # Apply the solution state at the given index
            move, state = self.solution_path[step_index]
            self.tiles_grid = [row[:] for row in state]  # Deep copy
            self.draw_tiles()
            
            # Add move info to terminal
            self.terminal.add_line(f"Step {step_index + 1}: Move '{move}'")
            self._add_state_to_terminal(state)
            
    def next_solution_step(self):
        if self.solution_index < len(self.solution_path) - 1:
            self.solution_index += 1
            self.apply_solution_step(self.solution_index)
            
    def previous_solution_step(self):
        if self.solution_index > 0:
            self.solution_index -= 1
            self.apply_solution_step(self.solution_index)

    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))

    def validate_input_matrix(self):
        """Validate if the input matrix is solvable"""
        # Validate initial matrix
        flat_input = []
        for row in self.input_matrix:
            for val in row:
                flat_input.append(val)
        
        # Validate goal matrix
        flat_goal = []
        for row in self.input_goal_matrix:
            for val in row:
                flat_goal.append(val)
        
        # Check if all numbers from 0 to N²-1 are present exactly once in each matrix
        expected_numbers = set(range(GAME_SIZE * GAME_SIZE))
        actual_numbers_input = set(flat_input)
        actual_numbers_goal = set(flat_goal)
        
        if expected_numbers != actual_numbers_input:
            self.input_error = "Invalid initial: must contain numbers 0 to 8"
            return False
        
        if expected_numbers != actual_numbers_goal:
            self.input_error = "Invalid goal: must contain numbers 0 to 8"
            return False
        
        self.input_error = ""
        return True

    def apply_input_matrix(self):
        """Apply the manual input matrix if valid"""
        if self.validate_input_matrix():
            self.tiles_grid = [row[:] for row in self.input_matrix]  # Deep copy
            self.tiles_grid_completed = [row[:] for row in self.input_goal_matrix]  # Use custom goal state
            self.draw_tiles()
            self.input_mode = False
            self.start_game = True
            self.start_timer = True
            # Reset solution when applying new matrix
            self.show_solution = False
            self.solution_path = []
            self.solution_index = -1
            return True
        return False
    
    def handle_matrix_input(self, event):
        """Handle keyboard input for the matrix"""
        if event.type == pygame.KEYDOWN:
            row, col = self.current_input_pos
            
            # Switch between initial and goal matrix with Tab
            if event.key == pygame.K_TAB:
                self.input_matrix_active = not self.input_matrix_active
                self.current_input_pos = [0, 0]
                return
            
            # Get active matrix based on which one is being edited
            active_matrix = self.input_matrix if self.input_matrix_active else self.input_goal_matrix
            
            # Handle navigation keys
            if event.key == pygame.K_UP and row > 0:
                self.current_input_pos[0] -= 1
            elif event.key == pygame.K_DOWN and row < GAME_SIZE - 1:
                self.current_input_pos[0] += 1
            elif event.key == pygame.K_LEFT and col > 0:
                self.current_input_pos[1] -= 1
            elif event.key == pygame.K_RIGHT and col < GAME_SIZE - 1:
                self.current_input_pos[1] += 1
            # Handle number input
            elif event.key in range(pygame.K_0, pygame.K_9 + 1):
                num = event.key - pygame.K_0
                if num < GAME_SIZE * GAME_SIZE:
                    # If number already exists elsewhere, remove it
                    for r in range(GAME_SIZE):
                        for c in range(GAME_SIZE):
                            if active_matrix[r][c] == num:
                                active_matrix[r][c] = -1  # Mark as empty temporarily
                    
                    active_matrix[row][col] = num
                    
                    # Move to next position
                    if col < GAME_SIZE - 1:
                        self.current_input_pos[1] += 1
                    elif row < GAME_SIZE - 1:
                        self.current_input_pos[0] += 1
                        self.current_input_pos[1] = 0
            
            # Enter to finish input
            elif event.key == pygame.K_RETURN:
                self.apply_input_matrix()
            
            # ESC to cancel input
            elif event.key == pygame.K_ESCAPE:
                self.input_mode = False

    def draw_input_matrix(self):
        """Draw the matrix input interface"""
        # Draw background for both matrices
        pygame.draw.rect(self.screen, DARKGREY, (0, 0, GAME_SIZE * TILESIZE, GAME_SIZE * TILESIZE))  # Initial matrix
        pygame.draw.rect(self.screen, DARKGREY, (GAME_SIZE * TILESIZE + 50, 0, GAME_SIZE * TILESIZE, GAME_SIZE * TILESIZE))  # Goal matrix
        
        # Draw grid for initial matrix
        for row in range(GAME_SIZE + 1):
            pygame.draw.line(self.screen, LIGHTGREY, (0, row * TILESIZE), 
                            (GAME_SIZE * TILESIZE, row * TILESIZE), 2)
        for col in range(GAME_SIZE + 1):
            pygame.draw.line(self.screen, LIGHTGREY, (col * TILESIZE, 0), 
                            (col * TILESIZE, GAME_SIZE * TILESIZE), 2)
        
        # Draw grid for goal matrix
        offset_x = GAME_SIZE * TILESIZE + 50
        for row in range(GAME_SIZE + 1):
            pygame.draw.line(self.screen, LIGHTGREY, (offset_x, row * TILESIZE), 
                            (offset_x + GAME_SIZE * TILESIZE, row * TILESIZE), 2)
        for col in range(GAME_SIZE + 1):
            pygame.draw.line(self.screen, LIGHTGREY, (offset_x + col * TILESIZE, 0), 
                            (offset_x + col * TILESIZE, GAME_SIZE * TILESIZE), 2)
        
        # Draw numbers for initial matrix
        font = pygame.font.SysFont("Consolas", 50)
        for row in range(GAME_SIZE):
            for col in range(GAME_SIZE):
                value = self.input_matrix[row][col]
                if value >= 0:  # Valid values only
                    text = str(value)
                    text_surf = font.render(text, True, WHITE)
                    text_rect = text_surf.get_rect(center=(
                        col * TILESIZE + TILESIZE // 2,
                        row * TILESIZE + TILESIZE // 2
                    ))
                    self.screen.blit(text_surf, text_rect)
                    
        # Draw numbers for goal matrix
        for row in range(GAME_SIZE):
            for col in range(GAME_SIZE):
                value = self.input_goal_matrix[row][col]
                if value >= 0:  # Valid values only
                    text = str(value)
                    text_surf = font.render(text, True, WHITE)
                    text_rect = text_surf.get_rect(center=(
                        offset_x + col * TILESIZE + TILESIZE // 2,
                        row * TILESIZE + TILESIZE // 2
                    ))
                    self.screen.blit(text_surf, text_rect)
        
        # Highlight current position on active matrix
        row, col = self.current_input_pos
        if self.input_matrix_active:
            matrix_x_offset = 0
            border_color = (0, 255, 0)  # Green for initial matrix
        else:
            matrix_x_offset = offset_x
            border_color = (0, 165, 255)  # Orange for goal matrix
            
        pygame.draw.rect(self.screen, border_color, (
            matrix_x_offset + col * TILESIZE + 2, row * TILESIZE + 2, 
            TILESIZE - 4, TILESIZE - 4
        ), 3)
        
        # Draw labels above matrices
        label_font = pygame.font.SysFont("Consolas", 30)
        init_label = label_font.render("Initial State", True, WHITE)
        goal_label = label_font.render("Goal State", True, WHITE)
        self.screen.blit(init_label, (TILESIZE, TILESIZE * GAME_SIZE + 20))
        self.screen.blit(goal_label, (offset_x + TILESIZE, TILESIZE * GAME_SIZE + 20))
        
        # Draw instructions
        instructions = [
            "Use arrow keys to navigate",
            "Numbers 0-8 to input values",
            "Tab to switch between matrices",
            "Enter to confirm both matrices",
            "ESC to cancel"
        ]
        small_font = pygame.font.SysFont("Consolas", 20)
        for i, text in enumerate(instructions):
            text_surf = small_font.render(text, True, WHITE)
            self.screen.blit(text_surf, (500, 450 + i * 30))
            
        # Draw active matrix indicator
        active_text = "Editing: " + ("Initial State" if self.input_matrix_active else "Goal State")
        active_surf = small_font.render(active_text, True, WHITE)
        self.screen.blit(active_surf, (500, 420))
            
        # Draw error message if any
        if self.input_error:
            error_surf = small_font.render(self.input_error, True, (255, 0, 0))
            self.screen.blit(error_surf, (500, 580))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.input_mode = False
        self.input_error = ""
        self.input_matrix_active = True
        self.buttons_list = []
        self.buttons_list.append(Button(500, 100, 200, 50, "Shuffle", WHITE, BLACK))
        self.buttons_list.append(Button(500, 170, 200, 50, "Reset", WHITE, BLACK))
        self.buttons_list.append(Button(500, 240, 200, 50, "Solve", WHITE, BLACK))
        self.buttons_list.append(Button(500, 310, 200, 50, "Manual Input", WHITE, BLACK))
        
        # Add dropdown for heuristic selection
        self.heuristic_dropdown = Dropdown(
            500, 380, 200, 30, 
            ["manhattan", "euclidean", "misplaced"],
            "Heuristic"
        )
        self.current_heuristic = self.heuristic_dropdown.selected_option
        
        # Solution navigation buttons (initially hidden)
        self.solution_buttons = []
        self.solution_buttons.append(Button(500, 430, 200, 50, "Previous", WHITE, BLACK))
        self.solution_buttons.append(Button(500, 500, 200, 50, "Next", WHITE, BLACK))
        
        # Reset solution variables
        self.solution_path = []
        self.solution_index = -1
        self.show_solution = False
        self.astar_execution_time = 0
        
        # Initialize the input matrices
        self.input_matrix = [[-1 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
        self.input_goal_matrix = [[-1 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
        self.current_input_pos = [0, 0]
        
        # Initialize terminal with welcome message
        self.terminal.clear()
        self.terminal.add_line("Welcome to Sliding Puzzle Solver")
        self.terminal.add_line("Use 'Solve' button to find solution with A* algorithm")
        
        self.draw_tiles()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                if self.high_score > 0:
                    self.high_score = self.elapsed_time if self.elapsed_time < self.high_score else self.high_score
                else:
                    self.high_score = self.elapsed_time
                self.save_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer

        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 120:
                self.start_shuffle = False
                self.start_game = True
                self.start_timer = True

        self.all_sprites.update()

    def draw_grid(self):
        for row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, GAME_SIZE * TILESIZE))
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (GAME_SIZE * TILESIZE, col))

    def draw(self):
        self.screen.fill(BGCOLOUR)
        
        if self.input_mode:
            self.draw_input_matrix()
        else:
            self.all_sprites.draw(self.screen)
            self.draw_grid()
            
            for button in self.buttons_list:
                button.draw(self.screen)
                
            # Draw the heuristic dropdown
            self.heuristic_dropdown.draw(self.screen)
                
            # Draw solution navigation buttons if solution is available
            if self.show_solution and len(self.solution_path) > 0:
                for button in self.solution_buttons:
                    button.draw(self.screen)
                
                # Show solution status
                solution_text = f"Step {self.solution_index + 1}/{len(self.solution_path)}"
                UIElement(500, 570, solution_text).draw(self.screen)
                
                # Show A* execution time
                astar_time_text = f"A* time: {self.astar_execution_time:.6f}s"
                UIElement(500, 600, astar_time_text).draw(self.screen)
            
            UIElement(550, 35, "%.3f" % self.elapsed_time).draw(self.screen)
            UIElement(430, 300, "High Score - %.3f" % (self.high_score if self.high_score > 0 else 0)).draw(self.screen)
            
            # Draw terminal
            self.terminal.draw(self.screen)
        
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            # Handle terminal scrolling events
            self.terminal.handle_event(event)

            # Handle matrix input mode
            if self.input_mode:
                self.handle_matrix_input(event)
                continue
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Handle dropdown click
                if self.heuristic_dropdown.click(mouse_x, mouse_y):
                    self.current_heuristic = self.heuristic_dropdown.selected_option
                    continue
                
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

                            self.draw_tiles()

                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Shuffle":
                            self.shuffle_time = 0
                            self.start_shuffle = True
                            # Reset solution when shuffling
                            self.show_solution = False
                            self.solution_path = []
                            self.solution_index = -1
                            # Add message to terminal
                            self.terminal.clear()
                            self.terminal.add_line("Shuffling puzzle...")
                        if button.text == "Reset":
                            self.new()
                        if button.text == "Solve":
                            if self.solve_with_astar():
                                # Apply first solution step
                                self.apply_solution_step(0)
                        if button.text == "Manual Input":
                            # Enter matrix input mode
                            self.input_mode = True
                            # Initialize with -1 (empty)
                            self.input_matrix = [[-1 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
                            self.input_goal_matrix = [[-1 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
                            self.current_input_pos = [0, 0]
                
                # Handle solution navigation buttons
                if self.show_solution and len(self.solution_path) > 0:
                    for button in self.solution_buttons:
                        if button.click(mouse_x, mouse_y):
                            if button.text == "Previous":
                                self.previous_solution_step()
                            if button.text == "Next":
                                self.next_solution_step()


game = Game()
while True:
    game.new()
    game.run()
