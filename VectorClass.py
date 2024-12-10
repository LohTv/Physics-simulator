import math

import pygame.draw


class Vector():
    def __init__(self, x=0., y=0.):
        self.x = x
        self.y = y
        self.angle = math.atan2(y, x)
        self.magnitude = math.sqrt(x**2 + y**2)
        self.val = (x, y)

    def __add__(self, other):
        return  Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def Normalise(self):
        if self.magnitude != 0:
            return Vector(self.x / self.magnitude , self.y / self.magnitude)
        else:
            return self

    def Inverse(self):
        return Vector(-self.y, self.x).Normalise()

    def Draw(self, screen, centre):
        pos = centre.val
        end_pos_vec = centre + self
        end_pos = end_pos_vec.val
        pygame.draw.line(screen, (255, 0, 0), pos, end_pos, 6)
        # left_end_vec = end_pos_vec.Inverse()
        # right_end_vec = end_pos_vec.Inverse() * (-1)
        # end_point = end_pos_vec * 1.1
        # left_end = left_end_vec.val
        # right_end = right_end_vec.val
        # end_point_point = end_point.val
        # pygame.draw.polygon(screen, (255, 0, 0),[left_end, right_end, end_point_point])

def VectorByTwoPoints(a, b):
    return Vector(b[0] - a[0], b[1] - a[1])

def DrawVect(screen, centre, vect):
    pos = centre.val
    end_pos_vec = centre + vect
    end_pos = end_pos_vec.val
    pygame.draw.line(screen, (255, 0, 0), pos, end_pos, 2)
    left_end_vec = end_pos_vec.Inverse()
    right_end_vec = end_pos_vec.Inverse() * (-1)
    end_point = end_pos_vec * 1.1
    left_end = left_end_vec.val
    right_end = right_end_vec.val
    end_point_point = end_point.val
    pygame.draw.polygon(screen, (255, 0, 0),[left_end, right_end, end_point_point])