import pygame
import sys


def draw_settings_components(surface, x, y, width, value, min_value, max_value):
    # Draw the slider track
    pygame.draw.rect(surface, (200, 200, 200), (x, y, width, 10))

    # Calculate slider thumb position
    thumb_pos = x + ((value - min_value) / (max_value - min_value)) * width
    pygame.draw.circle(surface, (0, 0, 0), (int(thumb_pos), y + 5), 8)


def open_settings_window(screen, current_settings, save_callback, languages=None, volume_range=(0, 100)):
    if languages is None:
        languages = ["English", "Spanish", "French", "German", "Chinese"]

    font = pygame.font.Font(None, 36)
    button_font = pygame.font.Font(None, 28)
    clock = pygame.time.Clock()

    # UI Colors
    bg_color = (220, 220, 220)  # Light gray
    panel_color = (255, 255, 255)  # White settings panel
    text_color = (0, 0, 0)
    button_color = (100, 100, 255)
    hover_color = (150, 150, 255)

    language_index = languages.index(current_settings.get("language", languages[0]))
    volume_value = current_settings.get("volume", 50)

    # Panel properties (Centered at 650, 300)
    panel_x, panel_y, panel_width, panel_height = 650, 300, 500, 300

    # Slider properties (Inside panel)
    slider_x, slider_y = panel_x + 100, panel_y + 250
    slider_width = 300
    slider_active = False

    settings_running = True
    while settings_running:

        # Draw settings panel
        pygame.draw.rect(screen, panel_color, (panel_x, panel_y, panel_width, panel_height), border_radius=10)

        # Draw volume slider
        draw_settings_components(screen, slider_x, slider_y, slider_width, volume_value, volume_range[0],
                                 volume_range[1])
        volume_text = font.render(f"Volume: {volume_value}", True, text_color)
        screen.blit(volume_text, (panel_x + 200, panel_y + 200))

        # Draw language selection inside panel
        language_text = font.render(f"Language: {languages[language_index]}", True, text_color)
        screen.blit(language_text, (panel_x + 140, panel_y + 100))

        left_arrow = pygame.Rect(panel_x + 80, panel_y + 100, 30, 30)
        right_arrow = pygame.Rect(panel_x + 400, panel_y + 100, 30, 30)
        pygame.draw.rect(screen, button_color, left_arrow)
        pygame.draw.rect(screen, button_color, right_arrow)

        left_arrow_text = button_font.render("<", True, text_color)
        right_arrow_text = button_font.render(">", True, text_color)
        screen.blit(left_arrow_text, (panel_x + 90, panel_y + 105))
        screen.blit(right_arrow_text, (panel_x + 410, panel_y + 105))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if slider_x <= mouse_x <= slider_x + slider_width and slider_y - 10 <= mouse_y <= slider_y + 10:
                    slider_active = True
                elif left_arrow.collidepoint(mouse_x, mouse_y):
                    language_index = (language_index - 1) % len(languages)
                    current_settings["language"] = languages[language_index]
                    save_callback(current_settings)
                elif right_arrow.collidepoint(mouse_x, mouse_y):
                    language_index = (language_index + 1) % len(languages)
                    current_settings["language"] = languages[language_index]
                    save_callback(current_settings)
            elif event.type == pygame.MOUSEBUTTONUP:
                slider_active = False
            elif event.type == pygame.MOUSEMOTION and slider_active:
                mouse_x, _ = pygame.mouse.get_pos()
                new_value = int(
                    ((mouse_x - slider_x) / slider_width) * (volume_range[1] - volume_range[0]) + volume_range[0])
                volume_value = max(volume_range[0], min(volume_range[1], new_value))

                # Apply volume setting
                pygame.mixer.music.set_volume(volume_value / 100)
                current_settings["volume"] = volume_value
                save_callback(current_settings)

        pygame.display.flip()
        clock.tick(60)


