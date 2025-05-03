import sys
import math
import pygame
import pymunk
from pymunk.vec2d import Vec2d

# --- Configurable Defaults ---
WIDTH, HEIGHT = 800, 600
FPS = 60
DEFAULT_VEL_SCALE = 0.1
DEFAULT_ACC_SCALE = 0.5
SLIDER_Y = HEIGHT - 40
SLIDER_WIDTH = 200
SLIDER_HEIGHT = 10
SLIDER_MARGIN = 50

# --- Helper Classes ---
class Slider:
    """Simple horizontal slider for adjusting a float value."""
    def __init__(self, x, y, width, height, initial, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.handle = pygame.Rect(x + (initial * width) - 5, y - 5, 10, height + 10)
        self.value = initial
        self.color = color
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.handle.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            x = max(self.rect.x, min(event.pos[0], self.rect.right))
            self.handle.x = x - 5
            self.value = (self.handle.x + 5 - self.rect.x) / self.rect.width

    def draw(self, surf):
        pygame.draw.rect(surf, (200,200,200), self.rect)
        pygame.draw.rect(surf, self.color, self.handle)

class BodyVisualizer:
    """Manages drawing velocity, acceleration, angular velocity, and labels."""
    def __init__(self, body, radius, font):
        self.body = body
        self.radius = radius
        self.font = font
        # FIX: unpack the Vec2d components into a new Vec2d
        self.prev_vel = Vec2d(*body.velocity)

        self.vel_scale = DEFAULT_VEL_SCALE
        self.acc_scale = DEFAULT_ACC_SCALE
        self.show_vel = True
        self.show_acc = True
        self.show_labels = True

    def update(self, dt):
        # FIX: unpack again when reading current velocity
        self.vel = Vec2d(*self.body.velocity)
        self.acc = (self.vel - self.prev_vel) / dt if dt > 0 else Vec2d(0,0)
        self.ang_vel = self.body.angular_velocity
        self.prev_vel = Vec2d(*self.vel)

    def draw_arrow(self, surf, start, vector, color, scale, head_size=8, width=2):
        end = start + vector * scale
        pygame.draw.line(surf, color, start, end, width)
        angle = math.atan2((end - start).y, (end - start).x)
        left = end + Vec2d(-head_size, head_size/2).rotated(angle)
        right = end + Vec2d(-head_size, -head_size/2).rotated(angle)
        pygame.draw.polygon(surf, color, [end, left, right])

    def draw(self, surf):
        pos = Vec2d(*self.body.position)
        # Draw body shape
        pygame.draw.circle(surf, (180,180,180), pos, self.radius, 2)

        # Velocity arrow
        if self.show_vel:
            self.draw_arrow(surf, pos, self.vel, (0,0,255), self.vel_scale)
        # Acceleration arrow
        if self.show_acc:
            self.draw_arrow(surf, pos, self.acc, (255,0,0), self.acc_scale)
        # Angular velocity arc
        if abs(self.ang_vel) > 0.1:
            sweep = self.ang_vel * 0.2
            rect = pygame.Rect(
                pos.x - self.radius - 10,
                pos.y - self.radius - 10,
                2*(self.radius + 10),
                2*(self.radius + 10)
            )
            pygame.draw.arc(surf, (0,255,0), rect, 0, sweep, 2)
        # Numeric labels
        if self.show_labels:
            vel_label = self.font.render(f"v={self.vel.length:.1f}", True, (0,0,255))
            acc_label = self.font.render(f"a={self.acc.length:.1f}", True, (255,0,0))
            surf.blit(vel_label, pos + (self.radius + 5, -20))
            surf.blit(acc_label, pos + (self.radius + 5,   0))

# --- Main Program ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Physics setup
    space = pymunk.Space()
    space.gravity = (0, 0)

    # Create a dynamic circle
    mass, radius = 1, 30
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = WIDTH//2, HEIGHT//4
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.6
    space.add(body, shape)

    # Visualizer and UI
    viz = BodyVisualizer(body, radius, font)
    vel_slider = Slider(SLIDER_MARGIN, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT,
                        DEFAULT_VEL_SCALE, (0,0,255))
    acc_slider = Slider(WIDTH - SLIDER_MARGIN - SLIDER_WIDTH, SLIDER_Y,
                        SLIDER_WIDTH, SLIDER_HEIGHT, DEFAULT_ACC_SCALE, (255,0,0))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    viz.show_vel = not viz.show_vel
                elif event.key == pygame.K_a:
                    viz.show_acc = not viz.show_acc
                elif event.key == pygame.K_n:
                    viz.show_labels = not viz.show_labels
            vel_slider.handle_event(event)
            acc_slider.handle_event(event)

        # Step physics
        space.step(dt)
        # Update scales from sliders
        viz.vel_scale = vel_slider.value * 2
        viz.acc_scale = acc_slider.value * 2
        viz.update(dt)

        # Draw
        screen.fill((30,30,30))
        viz.draw(screen)
        vel_slider.draw(screen)
        acc_slider.draw(screen)
        hud = font.render(
            "V:toggle velocity  A:toggle acceleration  N:toggle labels  Drag sliders to adjust scales",
            True, (200,200,200)
        )
        screen.blit(hud, (20,20))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
