import math
import pygame
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

def draw_arrow_angle(screen, start, length, angle, color = (255, 0, 0), thickness = 3, head_angle = math.radians(30), font_type = 'Arial'):
    x0, y0 = start
    # Compute end point of the shaft
    x1 = x0 + length * math.cos(angle)
    y1 = y0 + length * math.sin(angle)  # Pygame y-axis goes down

    # Draw shaft
    pygame.draw.line(screen, color, (x0, y0), (x1, y1), thickness)
    head_length = 0.2 * length


    angle1 = angle + math.pi - head_angle
    angle2 = angle + math.pi + head_angle

    x2 = x1 + head_length * math.cos(angle1)
    y2 = y1 + head_length * math.sin(angle1)
    x3 = x1 + head_length * math.cos(angle2)
    y3 = y1 + head_length * math.sin(angle2)

    font = pygame.font.SysFont(font_type, 30)
    length_text = f"{5*length:.1f}"  # format to 1 decimal place
    text_surf = font.render(length_text, True, color)
    text_rect = text_surf.get_rect()

    # Position text a bit beyond the arrow tip
    # Offset along the same angle direction by 'padding' pixels
    tx = x1 + math.cos(angle)*40
    ty = y1 - math.sin(angle)*40
    # Center the text on that point
    text_rect.center = (tx, ty)
    screen.blit(text_surf, text_rect)
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), thickness)
    pygame.draw.line(screen, color, (x1, y1), (x3, y3), thickness)

def draw_text(screen, start, length, angle=math.radians(30), shift = 0,color = (255, 0, 0), thickness = 3, head_angle = math.radians(30), font_type = 'Arial'):
    x0, y0 = start
    # Compute end point of the shaft
    x1 = x0
    y1 = y0  # Pygame y-axis goes down

    # Draw shaft
    pygame.draw.line(screen, color, (x0, y0), (x1, y1), thickness)
    head_length = 0
    angle1 = angle + math.pi - head_angle
    angle2 = angle + math.pi + head_angle

    x2 = x1 + head_length * math.cos(angle1)
    y2 = y1 + head_length * math.sin(angle1)
    x3 = x1 + head_length * math.cos(angle2)
    y3 = y1 + head_length * math.sin(angle2)

    font = pygame.font.SysFont(font_type, 30)
    length_text = f"{5*length:.1f}"  # format to 1 decimal place
    text_surf = font.render(length_text, True, color)
    text_rect = text_surf.get_rect()

    # Position text a bit beyond the arrow tip
    # Offset along the same angle direction by 'padding' pixels
    tx = x1 + math.cos(angle)*40
    ty = y1 - math.sin(angle)*40 + shift
    # Center the text on that point
    text_rect.center = (tx, ty)
    screen.blit(text_surf, text_rect)
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), thickness)
    pygame.draw.line(screen, color, (x1, y1), (x3, y3), thickness)