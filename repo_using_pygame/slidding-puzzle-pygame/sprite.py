import pygame
from settings import *

pygame.font.init()


class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        if self.text != "empty":
            self.font = pygame.font.SysFont("Consolas", 50)
            font_surface = self.font.render(self.text, True, BLACK)
            self.image.fill(WHITE)
            self.font_size = self.font.size(self.text)
            draw_x = (TILESIZE / 2) - self.font_size[0] / 2
            draw_y = (TILESIZE / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y))
        else:
            self.image.fill(BGCOLOUR)

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

    def right(self):
        return self.rect.x + TILESIZE < GAME_SIZE * TILESIZE

    def left(self):
        return self.rect.x - TILESIZE >= 0

    def up(self):
        return self.rect.y - TILESIZE >= 0

    def down(self):
        return self.rect.y + TILESIZE < GAME_SIZE * TILESIZE


class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))


class Button:
    def __init__(self, x, y, width, height, text, colour, text_colour):
        self.colour, self.text_colour = colour, text_colour
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, self.text_colour)
        self.font_size = font.size(self.text)
        draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
        draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))

    def click(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height


class Dropdown:
    def __init__(self, x, y, width, height, options, label="Select Option"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.label = label
        self.expanded = False
        self.selected_option = options[0]
        self.font = pygame.font.SysFont("Consolas", 20)
        
    def draw(self, screen):
        # Draw the main button
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
        
        # Draw selected option text
        text = self.font.render(f"{self.label}: {self.selected_option}", True, BLACK)
        self.font_size = self.font.size(f"{self.label}: {self.selected_option}")
        draw_x = self.x + 10
        draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))
        
        # Draw dropdown arrow
        pygame.draw.polygon(screen, BLACK, [
            (self.x + self.width - 15, self.y + self.height / 2 - 3),
            (self.x + self.width - 5, self.y + self.height / 2 - 3),
            (self.x + self.width - 10, self.y + self.height / 2 + 5)
        ])
        
        # Draw dropdown options if expanded
        if self.expanded:
            for i, option in enumerate(self.options):
                option_y = self.y + self.height + i * 30
                # Draw option background
                pygame.draw.rect(screen, WHITE, (self.x, option_y, self.width, 30))
                pygame.draw.rect(screen, BLACK, (self.x, option_y, self.width, 30), 1)
                
                # Draw option text
                option_text = self.font.render(option, True, BLACK)
                screen.blit(option_text, (self.x + 10, option_y + 5))
    
    def click(self, mouse_x, mouse_y):
        # Check if main dropdown button was clicked
        if (self.x <= mouse_x <= self.x + self.width and
            self.y <= mouse_y <= self.y + self.height):
            self.expanded = not self.expanded
            return True
        
        # Check if an option was clicked
        if self.expanded:
            for i, option in enumerate(self.options):
                option_y = self.y + self.height + i * 30
                if (self.x <= mouse_x <= self.x + self.width and
                    option_y <= mouse_y <= option_y + 30):
                    self.selected_option = option
                    self.expanded = False
                    return True
        
        return False
