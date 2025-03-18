import pygame as pg
import pymunk
import pymunk.pygame_util
import pyautogui

WIDTH = int(pyautogui.size()[0] * 0.95)
HEIGHT = int(pyautogui.size()[1] * 0.95)


def create_segment(from_, to_, thickness, space, color):
    segment_shape = pymunk.Segment(space.static_body, from_, to_, thickness)
    segment_shape.color = pg.color.THECOLORS[color]
    # space.add(segment_shape)
    return segment_shape


def Add_Ball_Dynamic(space, pos, radius=5, elasticity=0.4, friction=0.5, color=(255, 255, 255, 100), mass=1):
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.color = color
    space.add(body, shape)
    return shape


