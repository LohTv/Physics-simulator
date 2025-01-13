import pygame
import pymunk
import pymunk.pygame_util
from pygame import Surface

from VectorClass import Vector, VectorByTwoPoints
import random
import math
from Button_Add_Ball import Add_Ball

class Water_Particle:
    def __init__(self, mass, surface_tension, color, radius=5):
        self.mass = mass
        self.radius = radius
        self.surf_tens = surface_tension
        self.color = color
        self.body = None
    def Create_Water_Particle(self, pos, space):
        self.particle = Add_Ball(space, radius=self.radius, mass=self.mass,  elasticity=0.5, friction = 0.5, color=self.color, pos=pos)
        self.body = self.particle.body
        return self.particle
    def Apply_Tension(self, other):
        force = VectorByTwoPoints(self.body[0], other.body[0])
        dist = force.magnitude
        if dist < self.surf_tens:
            force = 10*force/(dist**2)
            self.body.apply_force_at_local_point((force.x, force.y))


class Liquid:
    def __init__(self, mass, radius, surface_tension, color):
        self.mass = mass
        self.surf_tens = surface_tension
        self.color = color
        self.radius = radius
        self.radiuspart = 7
        self.particles = set()

    def Create_Liquid(self, space, pos):
        """
        Spawns water particles uniformly inside a ball of given radius and position.

        :param space: The pymunk space where particles will be added.
        :param num_particles: The number of particles to spawn inside the liquid.
        """
        num_particles = int(round((self.radius**2))/100)
        for _ in range(num_particles):
            # Generate random angle and distance in polar coordinates
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, self.radius)

            # Convert polar coordinates to Cartesian coordinates
            x = pos[0] + distance * math.cos(angle)
            y = pos[1] + distance * math.sin(angle)

            # Create a water particle at the calculated position
            particle = Water_Particle(self.mass, self.surf_tens, self.color, self.radiuspart)
            particle.Create_Water_Particle((x, y), space)
            self.particles.add(particle)
        return self.particles



