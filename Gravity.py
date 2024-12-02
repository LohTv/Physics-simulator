import math
from VectorClass import Vector


def calculate_gravity(obj1, obj2, G):
    dx = obj2.position.x - obj1.position.x
    dy = obj2.position.y - obj1.position.y
    distance = math.sqrt(dx**2 + dy**2)

    if distance < obj1.shape.radius + obj2.shape.radius:
        distance = obj1.shape.radius + obj2.shape.radius

    force_magnitude = G * (obj1.mass * obj2.mass) / (distance**2)

    force_direction = Vector(dx, dy).Normalise()


    force = force_direction * force_magnitude
    return force

def apply_gravity_force(obj1, obj2, G):
    force = calculate_gravity(obj1, obj2, G)
    obj1.body.apply_force_at_local_point((force.x, force.y), (0, 0))
    obj2.body.apply_force_at_local_point((-force.x, -force.y), (0, 0))

