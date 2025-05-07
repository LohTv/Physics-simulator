import pygame
import pymunk
import pymunk.pygame_util


def Add_Ball(space, pos, radius=0.5, mass=1, elasticity=0.5, friction = 0.5, color=(255, 255, 255, 100)):
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.color = color
    space.add(body, shape)
    return shape
