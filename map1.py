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


def Add_Ball_Dynamic(space, pos, radius=5,  elasticity=0.4, friction=0.5, color=(255, 255, 255, 100), mass=1):
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.color = color
    space.add(body, shape)
    return shape

# def open_new_window_with_text():
#     # Initialize pygame
#     pg.init()
#
#     # Set up the display
#     width, height = 800, 600
#     window = pg.display.set_mode((width, height))
#     pg.display.set_caption("Random Walk and Path Distribution")
#
#     # Define colors
#     white = (255, 255, 255)
#     black = (0, 0, 0)
#
#     # Define the text to display
#     text = (
#         "Random Walk and Path Distribution in the Galton Board:\n"
#         "As a ball descends through the Galton board, its motion is governed by a random walk. "
#         "Each peg the ball encounters introduces a binary choice: it will be deflected either to the left or to the right. "
#         "Ideally, these deflections occur with equal probability, assuming no bias in the placement or shape of the pegs.\n\n"
#         "This sequence of random left and right movements mirrors a probabilistic process. Over multiple rows of pegs, "
#         "the number of left and right deflections accumulates, determining the ball's final position. Balls that experience roughly "
#         "equal left and right deflections tend to land in the central bins, while those that are consistently deflected in one direction "
#         "(though less likely) end up in the outer bins.\n\n"
#         "The overall distribution of balls at the bottom aligns with the binomial distribution, which approximates a normal distribution "
#         "as the number of rows increases. This demonstrates the central limit theorem, where random processes converge to form predictable "
#         "patterns despite individual uncertainty."
#     )
#
#
#     font = pg.font.SysFont("Arial", 20)
#
#     # Break the text into lines to fit the screen
#     lines = []
#     words = text.split(" ")
#     line = ""
#     for word in words:
#         test_line = line + word + " "
#         if font.size(test_line)[0] > width - 40:  # Check if the line width exceeds the window width
#             lines.append(line)
#             line = word + " "
#         else:
#             line = test_line
#     lines.append(line)
#
#     running = True
#     while running:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 running = False
#
#         window.fill(white)
#
#
#         y = 20
#         for line in lines:
#             text_surface = font.render(line, True, black)
#             window.blit(text_surface, (20, y))
#             y += 30
#
#
#         pg.display.flip()
#
#     pg.quit()

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
                segment = pymunk.Segment(space.static_body, (i, 70 + HEIGHT / 6 + 110 + r*40),(i, HEIGHT), 5)
                space.add(segment)
                objectstoadd.append(segment)
        else:
            for i in range(415, int(WIDTH), 110):
                if r % 2 == 0:
                    ball = Add_Ball(space, (i, 70 + HEIGHT / 6 + 110 + r*40))
                    objectstoadd.append(ball)
                else:
                    ball = Add_Ball(space, (i + 55, 70 + HEIGHT / 6 + 110 + r * 40))
                    objectstoadd.append(ball)
    for i in range(500):
        ball = Add_Ball_Dynamic(space, (random.uniform(350, WIDTH), 0), radius=7,  elasticity=0.2, friction=0.5, color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 100), mass=10)
        objectstoadd.append(ball)
    return objectstoadd