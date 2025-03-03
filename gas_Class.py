import pygame
import pymunk
import pymunk.pygame_util
from pygame import Surface
import random
import math
# from Button_Add_Ball import Add_Ball


def Add_Ball(space, pos, radius, mass, elasticity, friction, color):
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.color = color
    space.add(body, shape)
    shape.elasticity = elasticity
    shape.friction = friction
    return shape

class Gas_Particle:
    def __init__(self, mass,  color, radius=30):
        self.mass = mass
        self.radius = radius
        self.color = color
        self.body = None


    def Create_Gas_Particle(self, pos, space):
        self.particle = Add_Ball(space, radius=self.radius, mass=self.mass,  elasticity=1, friction = 0, color=self.color, pos=pos)
        self.body = self.particle.body
        return self.particle


class Gas:
    def __init__(self, mass, radius, color, temperature):
        self.mass = mass
        self.color = color
        self.radius = radius
        self.temp = temperature
        self.radiuspart = 5
        self.particles = []

    def Create_Gas(self, space, pos):
        """
        Spawns water particles uniformly inside a ball of given radius and position.

        :param space: The pymunk space where particles will be added.
        :param num_particles: The number of particles to spawn inside the liquid.
        """
        num_particles = int(round((self.radius**2))/20)

        for _ in range(num_particles):
            # Generate random angle and distance in polar coordinates
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, self.radius)

            # Convert polar coordinates to Cartesian coordinates
            x = pos[0] + distance * math.cos(angle)
            y = pos[1] + distance * math.sin(angle)


            # Create a water particle at the calculated position
            particle = Gas_Particle(self.mass, self.color, self.radiuspart)
            particle.Create_Gas_Particle((x, y), space=space)
            velocity_angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(self.temp - 10, self.temp)
            particle.body.velocity = (
                speed * math.cos(velocity_angle),
                speed * math.sin(velocity_angle)
            )
            self.particles.append(particle)
        return self.particles
