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

class Terminal:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.lines = []
        self.font = pygame.font.SysFont("Consolas", 16)
        self.line_height = 20
        self.max_visible_lines = self.height // self.line_height
        self.scroll_offset = 0
        self.bg_color = (30, 30, 30)
        self.text_color = (0, 255, 0)  # Terminal green
        self.scrollbar_color = (80, 80, 80)
        self.scrollbar_width = 15
        self.scrollbar_dragging = False
        
    def add_line(self, text):
        self.lines.append(text)
        # Auto-scroll to bottom when new line is added
        if len(self.lines) > self.max_visible_lines:
            self.scroll_offset = len(self.lines) - self.max_visible_lines
    
    def clear(self):
        self.lines = []
        self.scroll_offset = 0
        
    def draw(self, screen):
        # Draw terminal background
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height), 2)
        
        # Draw visible lines
        visible_lines = self.lines[self.scroll_offset:self.scroll_offset + self.max_visible_lines]
        for i, line in enumerate(visible_lines):
            text_surf = self.font.render(line, True, self.text_color)
            screen.blit(text_surf, (self.x + 10, self.y + i * self.line_height + 5))
        
        # Draw scrollbar if needed
        if len(self.lines) > self.max_visible_lines:
            # Draw scrollbar background
            pygame.draw.rect(screen, (50, 50, 50), 
                            (self.x + self.width - self.scrollbar_width, self.y, 
                             self.scrollbar_width, self.height))
            
            # Calculate scrollbar position and size
            total_content_height = len(self.lines) * self.line_height
            visible_ratio = min(1.0, self.height / total_content_height)
            scrollbar_height = max(20, int(self.height * visible_ratio))
            
            scroll_position_ratio = self.scroll_offset / max(1, len(self.lines) - self.max_visible_lines)
            scrollbar_position = int(self.y + scroll_position_ratio * (self.height - scrollbar_height))
            
            # Draw scrollbar handle
            pygame.draw.rect(screen, self.scrollbar_color, 
                            (self.x + self.width - self.scrollbar_width, scrollbar_position, 
                             self.scrollbar_width, scrollbar_height))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll_up()
            elif event.button == 5:  # Scroll down
                self.scroll_down()
            elif event.button == 1:  # Left click - check for scrollbar drag
                mouse_x, mouse_y = event.pos
                if (self.x + self.width - self.scrollbar_width <= mouse_x <= self.x + self.width and
                    self.y <= mouse_y <= self.y + self.height):
                    self.scrollbar_dragging = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button released
                self.scrollbar_dragging = False
                
        elif event.type == pygame.MOUSEMOTION and self.scrollbar_dragging:
            _, mouse_y = event.pos
            # Calculate new scroll position
            total_lines = max(1, len(self.lines))
            scrollable_lines = max(0, total_lines - self.max_visible_lines)
            
            # Map mouse position to scroll position
            relative_y = mouse_y - self.y
            scroll_ratio = max(0, min(1, relative_y / self.height))
            self.scroll_offset = int(scroll_ratio * scrollable_lines)
    
    def scroll_up(self):
        self.scroll_offset = max(0, self.scroll_offset - 1)
    
    def scroll_down(self):
        max_offset = max(0, len(self.lines) - self.max_visible_lines)
        self.scroll_offset = min(max_offset, self.scroll_offset + 1)
