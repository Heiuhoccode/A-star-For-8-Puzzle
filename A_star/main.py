import pygame
import random
import time
import threading
from sprite import *
from setting import *
import tkinter as tk
from tkinter import messagebox
from A_star_algorithm.test import a_star_search

class Game:
    def __init__(self):
        pygame.init()
        total_height = 50 + GAME_SIZE * TILESIZE + 50 + 50 + GAME_SIZE * TILESIZE + 50
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.selected_tile = None
        self.selected_grid = None  # để biết đang chọn từ lưới nào
        self.checked_parity = False
        self.selected_heuristic = False
        self.notification_text = ""
        self.notification_timer = 0
        self.parity_result_1 = ""
        self.parity_result_2 = ""
        self.result_data = None  # để chứa kết quả từ solver thread
        self.buttons = pygame.sprite.Group()
        self.current_screen = "main"  # Track current screen
        self.compare_heuristics = []  # List of selected heuristics for comparison
        self.compare_results = []  # Results from different heuristics
        self.compare_current_step = {}  # Current step for each heuristic
        self.running = True  # Flag to control all threads
        self.solver_threads = []  # Keep track of all solver threads
        self.create_buttons()

    def create_buttons(self):
        """Tạo các nút"""
        self.setup_button = Button(GAME_SIZE * TILESIZE + 50, 20, 100, 40, "Setup", self.setup)
        self.shuffle_button = Button(GAME_SIZE*TILESIZE + 50+ 120, 20, 100, 40, "Shuffle", self.shuffle)
        self.check_parity_button = Button(GAME_SIZE*TILESIZE + 50 + 120 + 120, 20, 140, 40, "Check Parity", self.check_parity)
        self.heuristic_dropdown = Dropdown(
            GAME_SIZE * TILESIZE + 50 + 120 + 120 + 160, 20, 120, 40,
            "Heuristic", [ "Misplaced", "Manhattan","Pattern DB", "Edge Match"],
            self.set_heuristic
        )
        self.solve_button = Button(GAME_SIZE*TILESIZE + 50 + 120 + 120 + 160 + 140, 20, 100, 40, "Solve", self.solve)
        self.compare_button = Button(GAME_SIZE*TILESIZE + 50, 70, 180, 40, "Compare Heuristic", self.show_compare_screen)
        
        # Thêm các nút vào group
        self.buttons.add(self.shuffle_button)
        self.buttons.add(self.check_parity_button)
        self.buttons.add(self.solve_button)
        self.buttons.add(self.setup_button)
        self.buttons.add(self.compare_button)
        
        # Buttons for compare screen
        self.compare_screen_buttons = pygame.sprite.Group()
        self.back_button = Button(20, 20, 100, 40, "Back", self.back_to_main)
        self.start_compare_button = Button(WIDTH - 150, HEIGHT - 60, 130, 40, "Start Compare", self.start_compare)
        self.compare_screen_buttons.add(self.back_button)
        self.compare_screen_buttons.add(self.start_compare_button)
        
        # Checkboxes for selecting heuristics to compare
        self.checkboxes = pygame.sprite.Group()
        heuristics = ["Misplaced", "Manhattan", "Pattern DB", "Edge Match"]
        for i, h in enumerate(heuristics):
            cb = Checkbox(WIDTH // 2 - 100, 150 + i * 60, 200, 40, h)
            self.checkboxes.add(cb)
        
        # Results screen buttons
        self.results_screen_buttons = pygame.sprite.Group()
        self.back_to_compare_button = Button(20, 20, 150, 40, "Back to Compare", self.back_to_compare)
        self.results_screen_buttons.add(self.back_to_compare_button)

        # Buttons for solve screen
        self.solve_screen_buttons = pygame.sprite.Group()
        self.back_to_main_button = Button(20, 20, 100, 40, "Back", self.back_to_main)
        self.solve_screen_buttons.add(self.back_to_main_button)

    def create_game(self):
        grid = [[0 for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
        return grid

    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for  column, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self,column,row,str(tile)))
                else:
                    self.tiles[row].append(Tile(self,column,row,"empty"))

    def draw_tiles_grid(self, grid_data, tile_obj_grid, offset_y=0):
        for row_idx, row in enumerate(grid_data):
            for col_idx, val in enumerate(row):
                text = str(val) if val != 0 else "empty"
                tile = Tile(self, col_idx, row_idx, text, offset_y)
                tile_obj_grid[row_idx][col_idx] = tile
                tile.offset_y = offset_y
                tile.update()

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_2 = self.create_game()
        self.tile_objs_grid1 = [[None for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
        self.tile_objs_grid2 = [[None for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
        self.parity_result_1 = ""
        self.parity_result_2 = ""
        self.solve_result = None
        self.solve_current_step = 0

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        for row in self.tile_objs_grid1 + self.tile_objs_grid2:
            for tile in row:
                if tile is not None:
                    tile.selected = (tile == self.selected_tile)
        self.all_sprites.update()
        # if self.result_data:
        #     steps,chiphi, elapsed = self.result_data
        #     if steps is None:
        #         self.show_result_window("Không tìm được lời giải.", elapsed)
        #     else:
        #         self.show_result_window(steps,chiphi, elapsed)
        #     self.result_data = None  # reset lại để không lặp

    def draw_grid_lines(self, offset_y=0):
        for i in range(GAME_SIZE + 1):
            # Đường dọc
            pygame.draw.line(
                self.screen, RED_DEFAULT,
                (i * TILESIZE, offset_y),
                (i * TILESIZE, offset_y + GAME_SIZE * TILESIZE), 2
            )
            # Đường ngang
            pygame.draw.line(
                self.screen, RED_DEFAULT,
                (0, offset_y + i * TILESIZE),
                (GAME_SIZE * TILESIZE, offset_y + i * TILESIZE), 2
            )

    def draw_label(self, text, y, x=100):
        font = pygame.font.SysFont("Consolas", 20, bold=True)
        label_surface = font.render(text, True, BLACK)
        label_rect = label_surface.get_rect(center=(x, y))
        self.screen.blit(label_surface, label_rect)

    def draw(self):
        self.screen.fill(GRAY_LIGHT)
        
        if self.current_screen == "main":
            self.all_sprites.draw(self.screen)
            
            # Lưới 1
            self.draw_label("Trạng thái bắt đầu", y=60)
            self.draw_tiles_grid(self.tiles_grid, self.tile_objs_grid1, offset_y=80)
            self.draw_grid_lines(offset_y=80)

            # Kết quả parity lưới 1
            if self.parity_result_1:
                self.draw_label(f"Parity: {self.parity_result_1}", y=80 + GAME_SIZE * TILESIZE + 20,
                                x=70)

            # Lưới 2
            offset2_y = 100 + GAME_SIZE * TILESIZE + 60
            self.draw_label("Trạng thái đích", y=offset2_y - 20)
            self.draw_tiles_grid(self.tiles_grid_2, self.tile_objs_grid2, offset_y=offset2_y)
            self.draw_grid_lines(offset_y=offset2_y)

            # Kết quả parity lưới 2
            if self.parity_result_2:
                self.draw_label(f"Parity: {self.parity_result_2}", y=offset2_y + GAME_SIZE * TILESIZE + 20,
                                x=70)

            self.buttons.draw(self.screen)
            self.heuristic_dropdown.draw(self.screen)
            
        elif self.current_screen == "compare":
            # Draw compare screen UI
            title_font = pygame.font.SysFont("Consolas", 30, bold=True)
            title = title_font.render("Select Heuristics to Compare", True, BLACK)
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
            
            # Draw checkboxes
            self.checkboxes.draw(self.screen)
            
            # Draw compare screen buttons
            self.compare_screen_buttons.draw(self.screen)
            
            # Draw current puzzle matrices
            self.draw_label("Current Starting State:", y=350)
            self.draw_small_grid(self.tiles_grid, x=WIDTH//3 - 80, y=380)
            
            self.draw_label("Current Goal State:", y=350, x=WIDTH*2//3)
            self.draw_small_grid(self.tiles_grid_2, x=WIDTH*2//3 - 80, y=380)
            
        elif self.current_screen == "results":
            # Draw results UI
            self.results_screen_buttons.draw(self.screen)
            self.draw_comparison_results()
        elif self.current_screen == "solve":
            self.solve_screen_buttons.draw(self.screen)
            self.draw_solve_results()
            
        if self.notification_text and time.time() < self.notification_timer:
            font = pygame.font.SysFont("Consolas", 24, bold=True)
            text_surface = font.render(self.notification_text, True, WHITE)
            background_rect = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)
            pygame.draw.rect(self.screen, RED_DEFAULT, background_rect)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 25))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def select_tile(self, mx, my):
        self.selected_tile = None
        for row in self.tile_objs_grid1:
            for tile in row:
                if tile and tile.click(mx, my) and tile.editable:
                    self.selected_tile = tile
                    self.selected_grid = "grid1"
                    return
        for row in self.tile_objs_grid2:
            for tile in row:
                if tile and tile.click(mx, my) and tile.editable:
                    self.selected_tile = tile
                    self.selected_grid = "grid2"
                    return

    def update_tile_value(self, value):
        tile = self.selected_tile
        if value == "":
            tile.text = ""  # Nếu value là chuỗi rỗng, xóa nội dung ô
        else:
            tile.text = str(value)  # Cập nhật ô với giá trị mới

        tile.image.fill(WHITE)

        font = pygame.font.SysFont("Consolas", 40)
        font_surface = font.render(tile.text, True, BLACK)
        draw_x = (TILESIZE / 2) - font.size(tile.text)[0] / 2
        draw_y = (TILESIZE / 2) - font.size(tile.text)[1] / 2
        tile.image.blit(font_surface, (draw_x, draw_y))

        # Cập nhật giá trị trong grid tương ứng
        if self.selected_grid == "grid1":
            self.tiles_grid[tile.y][tile.x] = value
        elif self.selected_grid == "grid2":
            self.tiles_grid_2[tile.y][tile.x] = value

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_solver_threads()  # Stop all threads before exiting
                pygame.quit()
                quit(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                if self.current_screen == "main":
                    self.select_tile(mx, my)
                    self.heuristic_dropdown.handle_event(event)
                    for button in self.buttons:
                        if button.click(mx, my) and button.action:
                            button.action()
                            
                elif self.current_screen == "compare":
                    for button in self.compare_screen_buttons:
                        if button.click(mx, my) and button.action:
                            button.action()
                    for checkbox in self.checkboxes:
                        if checkbox.click(mx, my):
                            checkbox.toggle()
                            
                elif self.current_screen == "results":
                    for button in self.results_screen_buttons:
                        if button.click(mx, my) and button.action:
                            button.action()
                    
                    # Handle next/previous buttons for each heuristic result
                    for i, result in enumerate(self.compare_results):
                        if result and 'next_button' in result and result['next_button'].click(mx, my):
                            self.next_step(result['heuristic'])
                        if result and 'prev_button' in result and result['prev_button'].click(mx, my):
                            self.prev_step(result['heuristic'])
                elif self.current_screen == "solve":
                    for button in self.solve_screen_buttons:
                        if button.click(mx, my) and button.action:
                            button.action()
                    if self.solve_result and 'next_button' in self.solve_result and self.solve_result['next_button'].click(mx, my):
                        self.next_solve_step()
                    if self.solve_result and 'prev_button' in self.solve_result and self.solve_result['prev_button'].click(mx, my):
                        self.prev_solve_step()

            elif event.type == pygame.KEYDOWN and self.selected_tile and self.current_screen == "main":
                if event.unicode.isdigit() and event.unicode != "0":
                    self.update_tile_value(int(event.unicode))
                elif event.key == pygame.K_BACKSPACE:  # Xóa nội dung khi nhấn Backspace
                    self.update_tile_value(0)  # Cập nhật nội dung ô là rỗng

    def shuffle(self):
        print("Shuffle clicked!")

        self.shuffle_grid(self.tiles_grid)
        self.shuffle_grid(self.tiles_grid_2)

        self.draw_tiles_grid(self.tiles_grid, self.tile_objs_grid1, offset_y=80)
        self.draw_tiles_grid(self.tiles_grid_2, self.tile_objs_grid2, offset_y=100 + GAME_SIZE * TILESIZE + 60)

    def solve(self):
        if not self.checked_parity:
            self.show_notification("Vui lòng kiểm tra parity trước khi giải.")
            return
        if self.parity_result_1 != self.parity_result_2:
            self.show_notification("Parity không giống nhau! Không thể giải.")
            return
        if not self.selected_heuristic:
            self.show_notification("Vui lòng chọn heuristic trước khi giải.")
            return

        self.show_notification("Đang giải...")
        self.current_screen = "solve"  # Switch to solve screen
        self.solve_result = None  # Reset solve result
        self.solve_current_step = 0
        solver_thread = threading.Thread(target=self.run_solve)
        solver_thread.daemon = True  # Make thread exit when main program exits
        self.solver_threads.append(solver_thread)
        solver_thread.start()

    def run_solve(self):
        if not self.running:
            return  # Exit if game is shutting down
            
        start_time = time.time()

        # Giả sử bạn có hàm a_star_search(start_grid, goal_grid, heuristic)
        path, chiphi = a_star_search(self.tiles_grid, self.tiles_grid_2, self.current_heuristic)
        
        if not self.running:
            return  # Check again if game is shutting down
            
        # path = path[::-1]
        elapsed_time = time.time() - start_time
        self.solve_result = {
            'heuristic': self.current_heuristic,
            'path': path[::-1] if path else None,
            'cost': chiphi,
            'time': elapsed_time,
            'nodes_visited': len(path) if path else 0
        }
        # self.result_data = (path, chiphi, elapsed_time)

    def heuristic(self):
        print("Heuristic clicked!")

    def shuffle_grid(self, grid):
        nums = list(range(GAME_SIZE * GAME_SIZE))  # Tạo list từ 0 → 8 (nếu GAME_SIZE = 3)
        random.shuffle(nums)

        for i in range(GAME_SIZE):
            for j in range(GAME_SIZE):
                grid[i][j] = nums[i * GAME_SIZE + j]

    def setup(self):
        print("Setup clicked!")

        def fill_grid(grid):
            values = list(range(1, GAME_SIZE * GAME_SIZE))
            random.shuffle(values)
            values.append(0)  # ô trống cuối cùng

            for i in range(GAME_SIZE):
                for j in range(GAME_SIZE):
                    grid[i][j] = values[i * GAME_SIZE + j]

        fill_grid(self.tiles_grid)
        fill_grid(self.tiles_grid_2)

        self.draw_tiles_grid(self.tiles_grid, self.tile_objs_grid1, offset_y=80)
        self.draw_tiles_grid(self.tiles_grid_2, self.tile_objs_grid2, offset_y=100 + GAME_SIZE * TILESIZE + 60)

    def get_parity(self, grid):
        flat = [num for row in grid for num in row if num != 0]
        inversions = 0
        for i in range(len(flat)-1):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1
        return "Chẵn" if inversions % 2 == 0 else "Lẻ"

    def is_unique_grid(self, grid):
        flat = [num for row in grid for num in row]
        if sorted(flat) != list(range(GAME_SIZE * GAME_SIZE)):
            return False
        return True

    def check_parity(self):
        print("Check Parity clicked!")
        if not self.is_valid_grid(self.tiles_grid) or not self.is_valid_grid(self.tiles_grid_2) or not self.is_unique_grid(self.tiles_grid_2) or not self.is_unique_grid(self.tiles_grid):
            self.show_notification("Mỗi lưới phải chứa đủ số từ 0 đến 8, không trùng!")
            return
        self.parity_result_1 = self.get_parity(self.tiles_grid)
        self.parity_result_2 = self.get_parity(self.tiles_grid_2)
        self.checked_parity = True

    def set_heuristic(self, heuristic_name):
        print(f"Heuristic selected: {heuristic_name}")
        self.current_heuristic = heuristic_name
        self.selected_heuristic = True

    def show_notification(self, message, duration=2):
        self.notification_text = message
        self.notification_timer = time.time() + duration  # thời gian kết thúc hiển thị

    def show_compare_screen(self):
        """Switch to the compare screen"""
        self.current_screen = "compare"
        # Reset selected heuristics
        for checkbox in self.checkboxes:
            checkbox.checked = False
            
    def back_to_main(self):
        """Return to the main screen"""
        self.current_screen = "main"
        # Stop all solver threads
        self.stop_solver_threads()
        # Reset checkboxes
        for checkbox in self.checkboxes:
            checkbox.checked = False
            checkbox.update_image()
            
    def back_to_compare(self):
        """Return to the compare screen from results"""
        self.current_screen = "compare"
        self.compare_results = []
        # Stop all solver threads
        self.stop_solver_threads()
        
    def stop_solver_threads(self):
        """Stop all running solver threads"""
        self.running = False  # Signal threads to terminate
        # Wait for all threads to finish
        for thread in self.solver_threads:
            if thread.is_alive():
                thread.join(0.1)  # Give a short timeout
        self.solver_threads = []  # Clear the list
        self.running = True  # Reset flag for future threads

    def start_compare(self):
        """Start comparison of selected heuristics"""
        selected = [cb.text for cb in self.checkboxes if cb.checked]
        if not selected:
            self.show_notification("Please select at least one heuristic")
            return
            
        if not self.is_valid_grid(self.tiles_grid) or not self.is_valid_grid(self.tiles_grid_2):
            self.show_notification("Invalid puzzle configuration")
            return
            
        self.compare_heuristics = selected
        self.current_screen = "results"
        self.compare_results = []
        self.compare_current_step = {}
        
        # Stop any existing solver threads
        self.stop_solver_threads()
        
        # Start a solver thread for each selected heuristic
        for heuristic in selected:
            solver_thread = threading.Thread(target=self.run_compare_solve, args=(heuristic,))
            solver_thread.daemon = True
            self.solver_threads.append(solver_thread)
            solver_thread.start()
            
    def run_compare_solve(self, heuristic_name):
        """Run A* algorithm with the specified heuristic"""
        if not self.running:
            return  # Exit if game is shutting down
            
        start_time = time.time()
        path, chiphi = a_star_search(self.tiles_grid, self.tiles_grid_2, heuristic_name)
        
        if not self.running:
            return  # Check again if game is shutting down
            
        elapsed_time = time.time() - start_time
        
        # Store result
        result = {
            'heuristic': heuristic_name,
            'path': path[::-1] if path else None,
            'cost': chiphi,
            'time': elapsed_time,
            'nodes_visited': len(path) if path else 0,
            'current_step': 0
        }
        
        self.compare_current_step[heuristic_name] = 0
        self.compare_results.append(result)
        
    def draw_small_grid(self, grid_data, x, y):
        """Draw a small representation of a grid"""
        cell_size = 30
        for row in range(GAME_SIZE):
            for col in range(GAME_SIZE):
                rect = pygame.Rect(x + col * cell_size, y + row * cell_size, cell_size, cell_size)
                pygame.draw.rect(self.screen, WHITE, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                
                # Draw number
                if grid_data[row][col] != 0:
                    font = pygame.font.SysFont("Consolas", 20)
                    text = font.render(str(grid_data[row][col]), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
                    
    def draw_comparison_results(self):
        """Draw the comparison results screen"""
        if not self.compare_results:
            font = pygame.font.SysFont("Consolas", 24)
            text = font.render("Running comparison...", True, BLACK)
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
            return
            
        num_heuristics = len(self.compare_heuristics)
        
        if num_heuristics == 1:
            grid_size = (1, 1)
        elif num_heuristics <= 2:
            grid_size = (1, 2)
        elif num_heuristics <= 4:
            grid_size = (2, 2)
        elif num_heuristics <= 6:
            grid_size = (2, 3)
        else:
            grid_size = (3, 3)  # Maximum 9 heuristics
            
        cell_width = (WIDTH - 40) // grid_size[1]
        cell_height = (HEIGHT - 80) // grid_size[0]
        
        for i, result in enumerate(self.compare_results):
            if not result:
                continue
                
            row = i // grid_size[1]
            col = i % grid_size[1]
            
            x = 20 + col * cell_width
            y = 80 + row * cell_height
            
            # Draw cell border
            rect = pygame.Rect(x, y, cell_width - 10, cell_height - 10)
            pygame.draw.rect(self.screen, WHITE, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
            
            # Draw heuristic name
            font = pygame.font.SysFont("Consolas", 20, bold=True)
            name_text = font.render(result['heuristic'], True, BLACK)
            self.screen.blit(name_text, (x + 10, y + 10))
            
            # Draw stats
            stats_font = pygame.font.SysFont("Consolas", 16)
            time_text = stats_font.render(f"Time: {result['time']:.4f}s", True, BLACK)
            nodes_text = stats_font.render(f"Nodes: {result['nodes_visited']}", True, BLACK)
            cost_text = stats_font.render(f"Cost: {result['cost']}", True, BLACK)
            
            self.screen.blit(time_text, (x + 10, y + 40))
            self.screen.blit(nodes_text, (x + 10, y + 60))
            self.screen.blit(cost_text, (x + 10, y + 80))
            
            # Draw current state
            if result['path']:
                current_step = self.compare_current_step[result['heuristic']]
                current_state = result['path'][current_step] if current_step < len(result['path']) else result['path'][-1]
                self.draw_small_grid(current_state, x + (cell_width - 90) // 2, y + 110)
                
                # Add navigation buttons if solution exists
                if 'next_button' not in result:
                    result['next_button'] = Button(x + cell_width - 110, y + cell_height - 50, 80, 30, "Next", None)
                    result['prev_button'] = Button(x + 20, y + cell_height - 50, 80, 30, "Prev", None)
                
                # Draw buttons
                result['next_button'].rect.topleft = (x + cell_width - 110, y + cell_height - 50)
                result['prev_button'].rect.topleft = (x + 20, y + cell_height - 50)
                
                self.screen.blit(result['next_button'].image, result['next_button'].rect)
                self.screen.blit(result['prev_button'].image, result['prev_button'].rect)
                
                # Draw step counter
                step_text = stats_font.render(f"Step {current_step + 1}/{len(result['path'])}", True, BLACK)
                step_rect = step_text.get_rect(center=(x + cell_width // 2, y + cell_height - 35))
                self.screen.blit(step_text, step_rect)
            else:
                no_solution = stats_font.render("No solution found", True, RED_DEFAULT)
                self.screen.blit(no_solution, (x + 20, y + cell_height // 2))

    def draw_solve_results(self):
        if not self.solve_result:
            font = pygame.font.SysFont("Consolas", 24)
            text = font.render("Running solver...", True, BLACK)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            return

        x = 20
        y = 80
        cell_width = WIDTH - 40
        cell_height = HEIGHT - 160

        rect = pygame.Rect(x, y, cell_width, cell_height)
        pygame.draw.rect(self.screen, WHITE, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 2)

        font = pygame.font.SysFont("Consolas", 20, bold=True)
        name_text = font.render(f"Solve with {self.solve_result['heuristic']}", True, BLACK)
        self.screen.blit(name_text, (x + 10, y + 10))

        stats_font = pygame.font.SysFont("Consolas", 16)
        time_text = stats_font.render(f"Time: {self.solve_result['time']:.4f}s", True, BLACK)
        nodes_text = stats_font.render(f"Nodes: {self.solve_result['nodes_visited']}", True, BLACK)
        cost_text = stats_font.render(f"Cost: {self.solve_result['cost']}", True, BLACK)

        self.screen.blit(time_text, (x + 10, y + 40))
        self.screen.blit(nodes_text, (x + 10, y + 60))
        self.screen.blit(cost_text, (x + 10, y + 80))

        if self.solve_result['path']:
            current_state = self.solve_result['path'][self.solve_current_step] if self.solve_current_step < len(
                self.solve_result['path']) else self.solve_result['path'][-1]
            self.draw_small_grid(current_state, x + (cell_width - 90) // 2, y + 110)

            if 'next_button' not in self.solve_result:
                self.solve_result['next_button'] = Button(x + cell_width - 110, y + cell_height - 50, 80, 30, "Next",
                                                          None)
                self.solve_result['prev_button'] = Button(x + 20, y + cell_height - 50, 80, 30, "Prev", None)

            self.solve_result['next_button'].rect.topleft = (x + cell_width - 110, y + cell_height - 50)
            self.solve_result['prev_button'].rect.topleft = (x + 20, y + cell_height - 50)

            self.screen.blit(self.solve_result['next_button'].image, self.solve_result['next_button'].rect)
            self.screen.blit(self.solve_result['prev_button'].image, self.solve_result['prev_button'].rect)

            step_text = stats_font.render(f"Step {self.solve_current_step + 1}/{len(self.solve_result['path'])}", True,
                                          BLACK)
            step_rect = step_text.get_rect(center=(x + cell_width // 2, y + cell_height - 35))
            self.screen.blit(step_text, step_rect)
        else:
            no_solution = stats_font.render("No solution found", True, RED_DEFAULT)
            self.screen.blit(no_solution, (x + 20, y + cell_height // 2))

    def next_step(self, heuristic):
        """Move to the next step in the solution path"""
        for result in self.compare_results:
            if result['heuristic'] == heuristic and result['path']:
                if self.compare_current_step[heuristic] < len(result['path']) - 1:
                    self.compare_current_step[heuristic] += 1
    
    def prev_step(self, heuristic):
        """Move to the previous step in the solution path"""
        for result in self.compare_results:
            if result['heuristic'] == heuristic and result['path']:
                if self.compare_current_step[heuristic] > 0:
                    self.compare_current_step[heuristic] -= 1

    def next_solve_step(self):
        if self.solve_result['path'] and self.solve_current_step < len(self.solve_result['path']) - 1:
            self.solve_current_step += 1

    def prev_solve_step(self):
        if self.solve_result['path'] and self.solve_current_step > 0:
            self.solve_current_step -= 1

    def is_valid_grid(self, grid):
        flat = [num for row in grid for num in row]
        non_empty = [num for num in flat if num != 0 and num != ""]
        return len(non_empty) == GAME_SIZE * GAME_SIZE - 1

game= Game()
while True:
    game.new()
    game.run()


