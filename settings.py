import pygame
import sys

# Initialize Pygame
pygame.init()

def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def draw_slider(surface, x, y, width, value, min_value, max_value):
    # Draw the slider track
    pygame.draw.rect(surface, (200, 200, 200), (x, y, width, 10))
    # Draw the slider thumb
    thumb_pos = x + ((value - min_value) / (max_value - min_value)) * width
    pygame.draw.circle(surface, (0, 0, 0), (int(thumb_pos), y + 5), 8)

def open_settings_window(screen, current_settings, save_callback, languages=None, volume_range=(0, 100)):
    # Default values
    if languages is None:
        languages = ["English", "Spanish", "French", "German", "Chinese"]

    # Pygame setup
    font = pygame.font.Font(None, 36)
    button_font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()

    # Set up colors
    bg_color = (255, 255, 255)
    text_color = (0, 0, 0)
    button_color = (100, 100, 255)
    hover_color = (150, 150, 255)

    # Current state for the settings
    language_index = languages.index(current_settings.get("language", languages[0]))
    volume_value = current_settings.get("volume", 50)