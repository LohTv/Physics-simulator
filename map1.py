import random
import pygame as pg
import pymunk
import pymunk.pygame_util
import pyautogui
WIDTH = pyautogui.size()[0] * 0.95
HEIGHT = pyautogui.size()[1] * 0.95

def create_segment(from_, to_, thickness, space, color):
    segment_shape = pymunk.Segment(space.static_body, from_, to_, thickness)
    segment_shape.color = pg.color.THECOLORS[color]
    # space.add(segment_shape)
    return segment_shape

def Add_Ball(space, pos, radius=0.5, mass=1, elasticity=0.5, friction = 0.5, color=(255, 255, 255, 100)):
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment, body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.color = color
    space.add(body, shape)
    return shape

def CreateMap1(space):
    segment_shape1 = pymunk.Segment(space.static_body, (330, 0), ((330 + WIDTH) / 2 - 25, HEIGHT / 5), 10)
    segment_shape1.color = pg.color.THECOLORS['grey']
    space.add(segment_shape1)
    segment_shape2 = pymunk.Segment(space.static_body, (WIDTH, 0), ((330 + WIDTH) / 2 + 25, HEIGHT / 5), 10)
    segment_shape2.color = pg.color.THECOLORS['grey']
    space.add(segment_shape2)
    segment_shape3 = pymunk.Segment(space.static_body, ((330 + WIDTH) / 2 - 25, HEIGHT / 5), ((330 + WIDTH) / 2 - 25, HEIGHT / 5 + 110), 10)
    segment_shape3.color = pg.color.THECOLORS['grey']
    space.add(segment_shape3)
    segment_shape4 = pymunk.Segment(space.static_body, ((330 + WIDTH) / 2 + 25, HEIGHT / 5),((330 + WIDTH) / 2 + 25, HEIGHT / 5 + 110), 10)
    segment_shape4.color = pg.color.THECOLORS['grey']
    space.add(segment_shape4)
    return [segment_shape1, segment_shape2, segment_shape3, segment_shape4]