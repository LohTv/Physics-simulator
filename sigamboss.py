import pygame
import pymunk
import pymunk.pygame_util


def create_static_cube(space, pos, size):
    """
    Create a static body with a rectangular shape (our "cube").
    pos: Tuple (x, y) for the center of the cube.
    size: Tuple (width, height) for the rectangle.
    """
    # Instead of using the global static body, create a new static body for customization.
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Poly.create_box(body, size)
    shape.friction = 1.0
    space.add(body, shape)
    return body, shape


def create_ball(space, pos, radius=15, mass=1):
    """
    Create a dynamic circular body (ball) at position pos.
    """
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.95
    shape.friction = 0.9
    space.add(body, shape)
    return body, shape


def main():
    # Initialize pygame and create a window
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Double Pendulum with Trajectory Trace")
    clock = pygame.time.Clock()

    # Create a pymunk space with gravity pointing downwards
    space = pymunk.Space()
    space.gravity = (0, 900)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # --- Create the static anchor ("cube") ---
    # We choose a cube of size 50x50 placed at (400, 100).
    cube_body, cube_shape = create_static_cube(space, (400, 100), (50, 50))

    # --- Create the dynamic balls ---
    # First ball (upper pendulum mass)
    ball1_body, ball1_shape = create_ball(space, (400, 250))

    # Second ball (lower pendulum mass)
    ball2_body, ball2_shape = create_ball(space, (400, 350))

    # --- Create joints to connect the bodies ---
    # Joint between static cube and ball1.
    # Since the cube's shape is centered on cube_body, we pick the bottom of the cube.
    # For a 50x50 box, half its height is 25 so bottom is (0, -25) in local coordinates.
    # For ball1, we pick a connection point near the top of the ball, e.g., (0, -15).
    joint1 = pymunk.PinJoint(cube_body, ball1_body, (0, -25), (0, -15))
    space.add(joint1)

    # Joint between ball1 and ball2.
    # We connect ball1’s lower point (0, 15) to ball2’s upper point (0, -15)
    joint2 = pymunk.PinJoint(ball1_body, ball2_body, (0, 15), (0, -15))
    space.add(joint2)

    # --- For trajectory trace ---
    # We will store the positions of ball2 to draw its past path.
    trace_points = []
    ball1_body.apply_impulse_at_local_point((500, 0))
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Save the current position of ball2 for the trace.
        # We convert the pymunk Vec2d position to a tuple for drawing.
        trace_points.append((int(ball2_body.position.x), int(ball2_body.position.y)))

        # Clear the screen with a light gray background.
        screen.fill((220, 220, 220))

        # Draw the trace as a red line connecting all previous positions.
        if len(trace_points) > 1:
            pygame.draw.lines(screen, (255, 0, 0), False, trace_points, 2)

        # Optionally, draw all pymunk objects (bodies, shapes, joints, etc.).
        space.debug_draw(draw_options)

        # Update the display
        pygame.display.flip()

        # Step the simulation (using a fixed time step for stability)
        dt = 1.0 / 50.0
        space.step(dt)
        clock.tick(50)

    pygame.quit()


if __name__ == '__main__':
    main()
