import pygame as pg
import pymunk
import pymunk.pygame_util
import pyautogui

WIDTH = int(pyautogui.size()[0] * 0.95)
HEIGHT = int(pyautogui.size()[1] * 0.95)


def Add_Cube(space, pos, size, color, elasticity, friction):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = elasticity
    shape.friction = friction
    shape.color = color
    space.add(body, shape)
    return shape

def Add_Ball_Dynamic(space, pos, radius=5, elasticity=0.99, friction=0.0, color=(255, 255, 255, 100), mass=1):
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.color = color
    space.add(body, shape)
    shape.elasticity = elasticity
    shape.friction = friction
    return shape

def CreateMap3(space):
    cube1 = Add_Cube(space, ((WIDTH + 330)/2, 30), (30, 30), (255, 255, 255, 100), 0.99, 0.1)
    ball1 = Add_Ball_Dynamic(space, ((WIDTH + 330)/2, HEIGHT/3), 20, 0.99, 0.1, (255, 255, 255, 100) )
    ball2 = Add_Ball_Dynamic(space, ((WIDTH + 330)/2, 2*HEIGHT/3), 20, 0.99, 0.1, (255, 255, 255, 100))
    objectstoadd = [cube1, ball1, ball2]
    joint1 =  pymunk.PinJoint(ball1.body, cube1.body, (0, 0), (0, 0))
    joint2 = pymunk.PinJoint(ball2.body, ball1.body, (0, 0), (0, 0))
    space.add(joint1)
    space.add(joint2)
    joints = [joint1, joint2]
    return (objectstoadd, joints)
