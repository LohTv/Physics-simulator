import pygame
import pymunk

class Mouse():
    def __init__(self, state):
        self.state = state

    def Add_Ball(self, space, pos, radius=0.5, mass=1, elasticity=0.5, friction=0.5, color=(255, 255, 255, 100)):
        moment = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
        body.position = pos
        shape = pymunk.Circle(body, radius)
        shape.color = color
        space.add(body, shape)
        return shape

    def getstate(self, event, screen):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        if self.state == 'ReadyToAddBall' :
            circle_radius = 30
            circle_color = (255, 255, 0)
            outline_thickness = 3
            pygame.draw.circle(screen, circle_color, (self.mouse_x, self.mouse_y), circle_radius, outline_thickness)
            if self.mouse_x > 300 and event.type == pygame.MOUSEBUTTONDOWN:
                return 'DrawBall'
        return None