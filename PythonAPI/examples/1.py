import sys
import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_mode((400, 600))

print("Press any key to see if it's detected")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            print(f"Key pressed: {event.key}")  # 打印按键的键码

            if event.key == K_LEFT:
                print("Left arrow key pressed")
            elif event.key == K_w:
                print("W key pressed")
            elif event.key == K_a:
                print("A key pressed")
            elif event.key == K_s:
                print("S key pressed")
