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
    obj1.body.apply_force_at_local_point((force.x, force.y))
    # obj2.body.apply_force_at_local_point((-force.x, -force.y), (0, 0))

def apply_gravity_acceleration(obj1, obj2, G):
    force = calculate_gravity(obj1, obj2, G)
    acceleration = force*(1/obj1.body.mass)
    accel = acceleration.val
    return accel

def planet_gravity(obj1, obj2, G, damping, dt):
    # Gravitational acceleration is proportional to the inverse square of
    # distance, and directed toward the origin. The central planet is assumed
    # to be massive enough that it affects the satellites but not vice versa.
    p1 = obj1.body.position
    p2 = obj2.body.position
    sq_dist = p1.get_dist_sqrd(p2)
    g = (p1 - p2) * -G / (sq_dist * math.sqrt(sq_dist))
    # body.velocity += g * dt # setting velocity directly like would be slower
    pymunk.Body.update_velocity(obj1.body, g, damping, dt)

