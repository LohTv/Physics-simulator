import pygame as pg
import pymunk
import pymunk.pygame_util
import pyautogui

WIDTH = int(pyautogui.size()[0] * 0.9)
HEIGHT = int(pyautogui.size()[1] * 0.90)


def create_segment(from_, to_, thickness, space, color):
    segment_shape = pymunk.Segment(space.static_body, from_, to_, thickness)
    segment_shape.color = pg.color.THECOLORS[color]
    # space.add(segment_shape)
    return segment_shape


def Add_Ball_Dynamic(space, pos, radius=5, elasticity=0.99, friction=0, color=(255, 255, 255, 100), mass=1):
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.color = color
    space.add(body, shape)
    shape.elasticity = elasticity
    shape.friction = friction
    return shape

def CreateMap2(space):
    segment_shape1 = pymunk.Segment(space.static_body, (380, HEIGHT / 6), ((330 + WIDTH) / 3, HEIGHT / 6), 10)
    segment_shape1.color = pg.color.THECOLORS['grey']
    space.add(segment_shape1)
    segment_shape2 = pymunk.Segment(space.static_body, (WIDTH - 50, HEIGHT / 6), (2*(330 + WIDTH) / 3, HEIGHT / 6), 10)
    segment_shape2.color = pg.color.THECOLORS['grey']
    space.add(segment_shape2)
    segment_shape3 = pymunk.Segment(space.static_body, ((330 + WIDTH) / 3, HEIGHT / 2),(2*(330 + WIDTH) / 3, HEIGHT / 2), 10)
    segment_shape3.color = pg.color.THECOLORS['grey']
    space.add(segment_shape3)
    objectstoadd = [segment_shape1, segment_shape2, segment_shape3]
    joints = []
    d = ((330 + WIDTH) / 3 - 380)/5
    for i in range(5):
        ball = Add_Ball_Dynamic(space, (((330 + WIDTH) / 3 + 380)/2 + (i - 2)*d, HEIGHT/3), radius=30)
        joint = pymunk.PinJoint(ball.body, segment_shape1.body, (0, 0), (ball.body.position.x, HEIGHT/6))
        space.add(joint)
        joints.append(joint)
        objectstoadd.append(ball)
    objectstoadd[-1].body.apply_impulse_at_local_point((400, 0), (0, 0))
    for i in range(5):
        ball = Add_Ball_Dynamic(space, ((WIDTH - 50 + 2*(330 + WIDTH) / 3)/2 + (i - 2)*d, HEIGHT/3), radius=30)
        joint = pymunk.PinJoint(ball.body, segment_shape1.body, (0, 0), (ball.body.position.x, HEIGHT/6))
        space.add(joint)
        joints.append(joint)
        objectstoadd.append(ball)
    objectstoadd[-2].body.apply_impulse_at_local_point((400, 0), (0, 0))
    objectstoadd[-1].body.apply_impulse_at_local_point((400, 0), (0, 0))
    for i in range(5):
        ball = Add_Ball_Dynamic(space, (((WIDTH + 330)/2 + (i - 2)*d, 2*HEIGHT/3 + 100)), radius=30)
        joint = pymunk.PinJoint(ball.body, segment_shape1.body, (0, 0), (ball.body.position.x, HEIGHT / 2))
        space.add(joint)
        joints.append(joint)
        objectstoadd.append(ball)
    return (objectstoadd, joints)