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

def Add_Ball(space, pos, radius=10,  elasticity=0.1, friction=0.5, color=(255, 255, 255, 100)):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.elasticity = elasticity
    shape.friction = friction
    shape.color = color
    space.add(body, shape)
    return shape



def CreateMap1(space):
    segment_shape1 = pymunk.Segment(space.static_body, (330, 0), ((330 + WIDTH) / 2 - 25, HEIGHT / 6), 10)
    segment_shape1.color = pg.color.THECOLORS['grey']
    space.add(segment_shape1)
    segment_shape2 = pymunk.Segment(space.static_body, (WIDTH, 0), ((330 + WIDTH) / 2 + 25, HEIGHT / 6), 10)
    segment_shape2.color = pg.color.THECOLORS['grey']
    space.add(segment_shape2)
    segment_shape3 = pymunk.Segment(space.static_body, ((330 + WIDTH) / 2 - 25, HEIGHT / 6), ((330 + WIDTH) / 2 - 25, HEIGHT / 6 + 110), 10)
    segment_shape3.color = pg.color.THECOLORS['grey']
    space.add(segment_shape3)
    segment_shape4 = pymunk.Segment(space.static_body, ((330 + WIDTH) / 2 + 25, HEIGHT / 6),((330 + WIDTH) / 2 + 25, HEIGHT / 6 + 110), 10)
    segment_shape4.color = pg.color.THECOLORS['grey']
    space.add(segment_shape4)
    segment_shape5 = pymunk.Segment(space.static_body, (330, HEIGHT),(WIDTH, HEIGHT), 20)
    segment_shape5.color = pg.color.THECOLORS['grey']
    space.add(segment_shape5)
    objectstoadd = [segment_shape1, segment_shape2, segment_shape3, segment_shape4, segment_shape5]
    for r in range(13):
        if r == 12:
            for i in range(375, int(WIDTH), 100):
                segment = pymunk.Segment(space.static_body, (i, 100 + HEIGHT / 6 + 110 + r*40),(i, HEIGHT), 5)
                space.add(segment)
                objectstoadd.append(segment)
        else:
            for i in range(375, int(WIDTH), 100):
                if r % 2 == 0:
                    ball = Add_Ball(space, (i, 100 + HEIGHT / 6 + 110 + r*40))
                    objectstoadd.append(ball)
                else:
                    ball = Add_Ball(space, (i + 50, 100 + HEIGHT / 6 + 110 + r * 40))
                    objectstoadd.append(ball)


    return objectstoadd