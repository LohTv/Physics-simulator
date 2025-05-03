import pygame
import pymunk
from pymunk import Vec2d
from liquid_Class import Liquid
from gas_Class import Gas

class Mouse():
    def __init__(self, state, ball_radius, cube_size, draw_size, liquid_radius, gas_radius, cube_mass):
        self.state = state
        self.ball_radius = ball_radius
        self.cube_size = cube_size
        self.draw_size = draw_size
        self.liquid_radius = liquid_radius
        self.gas_radius = gas_radius
        self.cube_mass = cube_mass
        self.joint_pos_start = (0, 0)
        self.space = None

    def Add_Ball(self, space, pos, radius, mass, elasticity, friction, color):
        moment = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
        body.position = pos
        shape = pymunk.Circle(body, radius)
        shape.color = color
        space.add(body, shape)
        shape.elasticity = elasticity
        shape.friction = friction
        return shape

    def Add_Cube(self, space, pos, size, color, elasticity, friction):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.color = color
        space.add(body, shape)
        return shape

    def Add_Cube_Dynamic(self, space, pos, size, color, elasticity, friction, mass):
        moment = pymunk.moment_for_box(mass, size)
        body = pymunk.Body(mass, moment)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.color = color
        space.add(body, shape)
        return shape

    def Add_Liquid(self, space: object, pos: object, mass: object, radius: object, surface_tension: object, color: object):
        liquid = Liquid(mass, radius,  surface_tension, (0, 0, 100, 70))
        liquidpart = liquid.Create_Liquid(space, pos)
        return liquidpart

    def Add_Gas(self, space: object, pos: object, mass: object, radius: object, temperature: object, color: object):
        gas = Gas(mass, radius, color, temperature)
        gaspart = gas.Create_Gas(space, pos)
        return gaspart

    def getstate(self, event, screen):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        if self.state == 'ReadyToAddBall':
            circle_radius = self.ball_radius
            circle_color = (255, 255, 255)
            outline_thickness = 3
            pygame.draw.circle(screen, circle_color, (self.mouse_x, self.mouse_y), circle_radius, outline_thickness)
            if self.mouse_x > 300 and event.type == pygame.MOUSEBUTTONDOWN:
                return 'DrawBall'

        if self.state == 'ReadyToAddCube':
            square_size = self.cube_size
            square_color = (255, 255, 255)
            outline_thickness = 3
            pygame.draw.rect(screen, square_color, (
            self.mouse_x - square_size // 2, self.mouse_y - square_size // 2, square_size, square_size),outline_thickness)
            if self.mouse_x > 300 and event.type == pygame.MOUSEBUTTONDOWN:
                 return 'DrawCube'

        if self.state == 'ReadyToAddDraw':
            square_size = self.draw_size
            square_color = (255, 255, 255)
            outline_thickness = 3
            pygame.draw.rect(screen, square_color, (
                self.mouse_x - square_size // 2, self.mouse_y - square_size // 2, square_size, square_size),
                             outline_thickness)
            if self.mouse_x > 300 and event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'DrawModeCube'
                return 'DrawModeCube'

        if self.state == 'DrawModeCube':
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] and self.mouse_x > 300:
                return 'DrawModeCube'
            if event.type == pygame.MOUSEBUTTONUP:
                self.state = 'ReadyToAddDraw'
                return None

        if self.state == 'ReadyToAddLiquid':
            circle_radius = self.ball_radius
            circle_color = (255, 255, 255)
            outline_thickness = 3
            pygame.draw.circle(screen, circle_color, (self.mouse_x, self.mouse_y), circle_radius, outline_thickness)
            if self.mouse_x > 300 and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.circle(screen, circle_color, (self.mouse_x, self.mouse_y), circle_radius, outline_thickness)
                return 'DrawLiquid'

        if self.state == 'ReadyToAddGas':
            circle_radius = self.gas_radius
            circle_color = (255, 255, 255)
            outline_thickness = 3
            pygame.draw.circle(screen, circle_color, (self.mouse_x, self.mouse_y), circle_radius, outline_thickness)
            if self.mouse_x > 300 and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.circle(screen, circle_color, (self.mouse_x, self.mouse_y), circle_radius, outline_thickness)
                return 'DrawGas'

        if self.state == 'ReadyToAddRope':
            if self.mouse_x > 300 and event.type == pygame.MOUSEBUTTONDOWN:
                self.joint_pos_start = (self.mouse_x, self.mouse_y)
                p = Vec2d(*(self.mouse_x, self.mouse_y))
                self.body1 = self.space.point_query_nearest(p, 5, pymunk.ShapeFilter())
                if self.body1 != None:
                    self.body1 =self.body1.shape.body
                    self.state = 'DrawingRope'
                    return  'DrawRopeStart'
                else:
                    pass

        if self.state == 'DrawingRope':
            pygame.draw.line(screen, (255, 0 , 0), self.joint_pos_start, (self.mouse_x, self.mouse_y), 10)
            if self.mouse_x > 300 and event.type == pygame.MOUSEBUTTONDOWN:
                self.state = None
                return 'DrawRope'

        if self.state == 'Deleting':
            if self.mouse_x > 300 and event.type == pygame.MOUSEBUTTONDOWN:
                return 'Delete'

        if self.state == 'Showing Velocity':
            if self.mouse_x > 300 and event.type == pygame.MOUSEBUTTONDOWN:
                return 'Show Velocity'

        if self.state == 'Showing Acceleration':
            if self.mouse_x > 300 and event.type == pygame.MOUSEBUTTONDOWN:
                return 'Show Acceleration'

        if self.state == 'Showing Kinetic Energy':
            if self.mouse_x > 300 and event.type == pygame.MOUSEBUTTONDOWN:
                return 'Show Kinetic Energy'

        if self.state == 'Showing Potential Energy':
            if self.mouse_x > 300 and event.type == pygame.MOUSEBUTTONDOWN:
                return 'Show Potential Energy'

        if self.state == 'Showing Full Energy':
            if self.mouse_x > 300 and event.type == pygame.MOUSEBUTTONDOWN:
                return 'Show Full Energy'

        return None