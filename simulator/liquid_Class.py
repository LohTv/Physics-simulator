import pygame
import pymunk
import pymunk.pygame_util
from pygame import Surface
from simulator.VectorClass import *
import random
import math
from simulator.Button_Add_Ball import Add_Ball


class Water_Particle:
    def __init__(self, mass, surface_tension, color, radius=5):
        self.mass = mass
        self.radius = radius
        self.surf_tens = surface_tension
        self.color = color
        self.body = None

    def Create_Water_Particle(self, pos, space):
        self.particle = Add_Ball(space, radius=self.radius, mass=self.mass,  elasticity=0.5, friction = 0.5, color=self.color, pos=pos)
        self.shape = self.particle
        self.body = self.particle.body
        return self.particle


class Liquid:
    def __init__(self, mass, radius, surface_tension, color):
        self.mass = mass
        self.surf_tens = surface_tension
        self.color = color
        self.radius = radius
        self.radiuspart = 10
        self.particles = []

    def Create_Liquid(self, space, pos):
        """
        Spawns water particles uniformly inside a ball of given radius and position.

        :param space: The pymunk space where particles will be added.
        :param num_particles: The number of particles to spawn inside the liquid.
        """
        num_particles = int(round((self.radius**2))/50)
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
            self.particles.append(particle)
        return self.particles

def apply_surface_tension_acceleration(self, other, rest_distance):

    direction = other.body.position - self.body.position
    direction_vect = Vector(direction[0], direction[1])
    current_distance = direction.length
    if current_distance == 0:
        return (0, 0)

    elif current_distance >= 100:
        return (0, 0)

    displacement = current_distance - rest_distance

    k = self.surf_tens

    force_magnitude = k * displacement

    force = direction_vect.Normalise()*force_magnitude

    acceleration = force*(1/self.body.mass)

    accel = acceleration.val

    return accel



