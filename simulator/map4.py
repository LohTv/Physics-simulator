import random
import pygame as pg
import pymunk
import pymunk.pygame_util
import pyautogui
import math

WIDTH = pyautogui.size()[0] * 0.90
HEIGHT = pyautogui.size()[1] * 0.90

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

def CreateMap4(space, G):
    pos1 = ((300+WIDTH)/2, HEIGHT/2)
    pos2 = ((300+WIDTH)/2 + (300+WIDTH)/4, HEIGHT/2)
    pos3 = ((300+WIDTH)/2 + (300+WIDTH)/4 + (300+WIDTH)/32, HEIGHT/2)
    ball1 = Add_Ball_Dynamic(space, pos1, 40, mass=1000)
    ball2 = Add_Ball_Dynamic(space, pos2, 8, mass=10)
    R1 = (300+WIDTH)/4
    R2 = (300+WIDTH)/32
    ball2.body.velocity = (0, math.sqrt(G*1000/R1))
    ball3 = Add_Ball_Dynamic(space, pos3, 2, mass=10/32)
    ball3.body.velocity = (0, math.sqrt(G * 1000 / (R1 + R2)) + math.sqrt(G * 10/ (R2)))
    objectstoadd = [ball1, ball2, ball3]
    return objectstoadd
