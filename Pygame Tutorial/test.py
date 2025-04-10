import pygame
from pygame.examples.scrap_clipboard import screen

pygame.init()

win = pygame.display.set_mode((400,500))
pygame.display.set_caption("Demo")
run = True
while run:
    win.fill((30, 144, 255))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
