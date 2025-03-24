import pygame
import pyautogui
import pymunk.pygame_util
from map2 import CreateMap2

# --- Set up the physics space ---
space = pymunk.Space()
space.gravity = (0, 900)
WIDTH = pyautogui.size()[0] * 0.95
HEIGHT = pyautogui.size()[1] * 0.95
objects = CreateMap2(space)

# --- Set up Pygame ---
pygame.init()
width, height = WIDTH, HEIGHT
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pymunk Joint Example")
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# --- Simulation loop ---
dt = 1.0 / 60.0  # time step for 60 FPS
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen to white
    screen.fill((255, 255, 255))

    # Step the physics simulation
    space.step(dt)

    # Draw all objects (bodies, shapes, and joints)
    space.debug_draw(draw_options)

    # Update the display and tick the clock
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
