from ssl import TLSVersion

import pygame
from setting import *

pygame.font.init()
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, action=None):
        super().__init__()  # Kế thừa đúng cách từ Sprite
        self.image = pygame.Surface((width, height))
        self.image.fill(RED_DEFAULT)  # Màu của nút
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.text = text
        self.font = pygame.font.SysFont("Consolas", 20)
        self.font_surface = self.font.render(text, True, BLACK)
        self.font_size = self.font.size(text)
        self.draw_text()

        # Tạo hành động khi nút được click (sẽ gán sau)
        self.action = action

    def draw_text(self):
        """Vẽ văn bản vào nút"""
        draw_x = (self.rect.width / 2) - self.font_size[0] / 2
        draw_y = (self.rect.height / 2) - self.font_size[1] / 2
        self.image.blit(self.font_surface, (draw_x, draw_y))

    def click(self, mouse_x, mouse_y):
        """Kiểm tra xem nút có bị click không"""
        return self.rect.collidepoint(mouse_x, mouse_y)

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text, offset_y=0):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.x, self.y = x, y
        self.offset_y = offset_y  # 👈 lưu lại giá trị offset
        self.text = text
        self.rect = self.image.get_rect()
        self.editable = True
        self.selected = False
        self.highlighted = False

        if self.text != "empty":
            self.font = pygame.font.SysFont("Consolas", 40)
            font_surface = self.font.render(self.text, True, BLACK)
            self.image.fill(WHITE)
            self.font_size = self.font.size(self.text)
            draw_x = (TILESIZE / 2) - self.font_size[0] / 2
            draw_y = (TILESIZE / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y))
        else:
            self.image.fill(WHITE)

        # Cập nhật vị trí ngay từ đầu
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE + self.offset_y

    def update_image(self):
        """Cập nhật hình ảnh của ô"""
        if self.highlighted:
            self.image.fill(RED_DEFAULT)  # Màu đỏ khi ô được chọn
        else:
            self.image.fill(WHITE)  # Màu trắng khi không được chọn
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE + self.offset_y  # 👈 cộng offset_y vào đây

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

class Dropdown(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, options, callback):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(RED_DEFAULT)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = text
        self.options = options
        self.callback = callback  # Hàm gọi khi chọn item
        self.font = pygame.font.SysFont("Consolas", 20)
        self.is_open = False
        self.selected = text

    def draw(self, screen):
        # Vẽ nút chính
        self.image.fill(RED_DEFAULT)
        label = self.font.render(self.selected, True, BLACK)
        self.image.blit(label, ((self.rect.width - label.get_width()) // 2, (self.rect.height - label.get_height()) // 2))
        screen.blit(self.image, self.rect)

        # Vẽ các tùy chọn nếu đang mở
        if self.is_open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                pygame.draw.rect(screen, WHITE, option_rect)
                pygame.draw.rect(screen, RED_DEFAULT, option_rect, 2)
                label = self.font.render(option, True, BLACK)
                screen.blit(label, (option_rect.x + 5, option_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if self.rect.collidepoint(mx, my):
                self.is_open = not self.is_open
            elif self.is_open:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                    if option_rect.collidepoint(mx, my):
                        self.selected = option
                        self.is_open = False
                        self.callback(option)
                        break
                else:
                    self.is_open = False
