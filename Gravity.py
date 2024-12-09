import math
import pymunk
from VectorClass import Vector


def calculate_gravity(obj1, obj2, G):
    dx = obj2.body.position.x - obj1.body.position.x
    dy = obj2.body.position.y - obj1.body.position.y
    distance = math.sqrt(dx**2 + dy**2)

    if distance < obj1.radius + obj2.radius:
        distance = obj1.radius + obj2.radius

    force_magnitude = G * (obj1.body.mass * obj2.body.mass) / (distance**2)

    force_direction = Vector(dx, dy).Normalise()

    force = force_direction * force_magnitude
    return force

def apply_gravity_force(obj1, obj2, G):
    force = calculate_gravity(obj1, obj2, G)
    obj1.body.apply_force_at_local_point((force.x, force.y), (0, 0))

def apply_gravity_acceleration(obj1, obj2, G):
    force = calculate_gravity(obj1, obj2, G)
    acceleration = force*(1/obj1.body.mass)
    accel = acceleration.val
    return accel

