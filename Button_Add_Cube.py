import pymunk
import pymunk.pygame_util


def Add_Cube(space, pos, size=(50, 50), color=(255, 0, 0), elasticity=0.5, friction=0.5):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = elasticity
    shape.friction = friction
    shape.color = color
    space.add(body, shape)
    return shape

