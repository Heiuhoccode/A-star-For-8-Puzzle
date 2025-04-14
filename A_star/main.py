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
        # Thêm các nút vào group
        self.buttons.add(self.shuffle_button)
        self.buttons.add(self.check_parity_button)
        self.buttons.add(self.solve_button)
        self.buttons.add(self.setup_button)

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

        # 2D lists để chứa Tile object (khác với grid số)
        self.tile_objs_grid1 = [[None for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
        self.tile_objs_grid2 = [[None for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
        self.parity_result_1 = ""
        self.parity_result_2 = ""

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
        if self.result_data:
            steps,chiphi, elapsed = self.result_data
            if steps is None:
                self.show_result_window("Không tìm được lời giải.", elapsed)
            else:
                self.show_result_window(steps,chiphi, elapsed)
            self.result_data = None  # reset lại để không lặp

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
                pygame.quit()
                quit(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                self.select_tile(mx, my)
                self.heuristic_dropdown.handle_event(event)

                for button in self.buttons:
                    if button.click(mx, my) and button.action:
                        button.action()
            elif event.type == pygame.KEYDOWN and self.selected_tile:
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
        threading.Thread(target=self.run_solve).start()

    def run_solve(self):
        start_time = time.time()

        # Giả sử bạn có hàm a_star_search(start_grid, goal_grid, heuristic)
        path, chiphi = a_star_search(self.tiles_grid, self.tiles_grid_2, self.current_heuristic)
        path = path[::-1]
        elapsed_time = time.time() - start_time

        self.result_data = (path,chiphi, elapsed_time)

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

    def is_valid_grid(self, grid):
        flat = [num for row in grid for num in row]
        non_empty = [num for num in flat if num != 0 and num != ""]
        return len(non_empty) == GAME_SIZE * GAME_SIZE - 1

    def show_result_window(self, steps,fee, elapsed_time):
        root = tk.Tk()
        root.title("Kết quả giải")

        text = tk.Text(root, wrap=tk.WORD, width=50, height=20)
        text.pack(padx=10, pady=10)

        if isinstance(steps, str):  # Nếu là lỗi
            text.insert(tk.END, steps)
        else:
            for i, step in enumerate(steps):
                text.insert(tk.END, f"Bước {i + 1}: {step}\n")

        text.insert(tk.END, f"\nThời gian chạy: {elapsed_time:.4f} giây")
        text.insert(tk.END, f"\nChi phí: {fee}")
        text.config(state=tk.DISABLED)

        root.mainloop()

game= Game()
while True:
    game.new()
    game.run()


