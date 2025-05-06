import random

import pygame
import pymunk
import pymunk.pygame_util
import pyautogui
from liquid_Class import *
import gas_Class
from Mouse import Mouse
from VectorClass import draw_arrow_angle
from VectorClass import draw_text
from Gravity import *
from map1 import CreateMap1
from map2 import CreateMap2
from pymunk.vec2d import Vec2d
import math
from settings import *
from map3 import  CreateMap3

WIDTH = pyautogui.size()[0] * 0.9
HEIGHT = pyautogui.size()[1] * 0.9
pygame.init()
FPS = 60
# WIDTH, HEIGHT = 1600, 1000
# GRAVITY = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics-simulator")
pygame.mixer.init()
pygame.mixer.music.load(r'Music/Saoundtrack1.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 1000)
running = True
draw_options = pymunk.pygame_util.DrawOptions(screen)
MouseState = None
FontSize = 1/(2600) * (HEIGHT + WIDTH)
print(FontSize)
# root = tk.Tk()
# root.withdraw()

class Button:
    def __init__(self, is_seen, x, y, width, height, text='', font_size=30,
                 text_color=(255, 255, 255), button_color=(169,169,169),
                 hover_color=(119,136,153)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont('Arial', font_size)
        self.rect = pygame.Rect(x, y, width, height)
        self.is_seen = is_seen
        self.childrens = []
        self.layer = []
        self.parent = None
        self.clicked = False
        self.activated = False
        self.user_text = ''

    def draw(self, screen, text):
        if self.is_seen:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, self.hover_color, self.rect)
            elif self.activated:
                pygame.draw.rect(screen, self.hover_color, self.rect)
            else:
                pygame.draw.rect(screen, self.button_color, self.rect)

            text_surf = self.font.render(text, True, self.text_color)
            text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if self.is_seen and event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                return True
        return False


class Button_with_Image:
    def __init__(self, is_seen, x, y, width, height, image_path1='', image_path2='', text='', font='', text_color=(255, 255, 255), hover_image_path = '', font_size=30, special_need=False, special_need2=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image_path2 = image_path2
        self.image_path1 = image_path1
        self.image_path = image_path1
        self.hover_image_path = hover_image_path
        self.rect = pygame.Rect(x, y, width, height)
        self.is_seen = is_seen
        self.childrens = []
        self.layer = []
        self.parent = None
        self.clicked = False
        self.activated = False
        self.text = text
        self.font = font
        self.text_color = text_color
        self.user_text = ''
        self.hover_image = ''
        self.image2 = None
        self.font = pygame.font.SysFont('Arial', font_size)
        self.special_need = special_need
        self.special_need2 = special_need2

        if self.image_path1:
            self.image1 = pygame.image.load(image_path1)
            self.image1 = pygame.transform.scale(self.image1, (width, height))  # Scale image to button size
            self.image = self.image1  # Set the initial image

        if self.image_path2:
            self.image2 = pygame.image.load(image_path2)
            self.image2 = pygame.transform.scale(self.image2, (width, height))

        if self.hover_image_path:
            self.hover_image= pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        # Scale image to button size

    def draw(self, screen, text=''):
            if self.is_seen:
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos) and self.hover_image and not self.activated:
                    screen.blit(self.hover_image, (self.x, self.y))
                elif self.activated:
                    screen.blit(self.image2, (self.x, self.y))
                else:
                    screen.blit(self.image, (self.x, self.y))
            if text:  # If text is provided, render it
                text_surf = self.font.render(text, True, self.text_color)
                text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
                screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if self.is_seen and event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                if self.image_path2 and self.special_need:
                        if self.image == self.image1:
                            self.image = self.image2
                        elif self.image == self.image2:
                            self.image = self.image1
                return True
        return False


def create_wall(space, width, height, pos, color, elasticity, friction):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    size = (width, height)
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = elasticity
    shape.friction = friction
    space.add(body, shape)
    return shape


if not 'Sprites/LeBron(Thegoat).png':
    print(1/0)

button_width = 200 * FontSize
button_height = HEIGHT/13
dy = HEIGHT/10

# print(button_width)
# print(button_height)

Button_Tracing = Button(False, 40, 30 + 5*dy, button_width, button_height, 'Trace', int(40*FontSize))
Button_Show_Velocity = Button(False, 40, 30, button_width, button_height, 'Show velocity', int(25*FontSize))
Button_Show_Acceleration = Button(False, 40, 30 + dy, button_width, button_height, 'Show acceleration', int(25*FontSize))
Button_Show_Kinetic_Energy = Button(False, 40, 30 + 2*dy, button_width, button_height, 'Show kinetic energy', int(20*FontSize))
Button_Show_Potential_Energy = Button(False, 40, 30 + 3*dy, button_width, button_height, 'Show potential energy', int(20*FontSize))
Button_Show_Full_Energy = Button(False, 40, 30 + 4*dy, button_width, button_height, 'Show full energy', int(25*FontSize))
Button_Data = Button(False, 40, 30 + 3*dy, button_width, button_height, 'Data', int(40*FontSize))
Button_Pendulum = Button(False, 40, 30 + 2*dy, button_width, button_height, 'Pendulum', int(40*FontSize))
Button_Delete = Button(False, 40, HEIGHT*0.88 - 2*dy, button_width, button_height, 'Delete', int(40*FontSize))
Button_Add_Rope = Button(False, 40, 30 + 5*dy, button_width, button_height, 'Add Joint', int(40*FontSize))
Button_Cube_Mass = Button(False, 40, 30 + 2*dy, button_width, button_height, 'Mass', int(40*FontSize))
Button_Cube_Dynamic = Button(False, 40, 30 + 3*dy, button_width, button_height, 'Dynamic', int(40*FontSize))
Button_Gas_Size = Button_with_Image(False, 40, 30 + 2*dy, button_width, button_height, 'Sprites/size.png', hover_image_path='Sprites/hovers/size2.png', image_path2='Sprites/hovers/da.png')
Button_Temperature = Button(False, 40, 30 + dy, button_width, button_height, 'Temperature', int(40*FontSize))
Button_Gas_Mass = Button(False, 40, 30, button_width, button_height, 'Mass', int(40*FontSize))
Button_Add_Gas = Button(False, 40, 30 + 4*dy, button_width, button_height, 'Add Gas', int(40*FontSize))
Button_Add_Liquid = Button(False, 40, 30 + 3*dy, button_width, button_height, 'Add Liquid', int(40*FontSize))
Button_Settings = Button_with_Image(True, WIDTH - 90, 15, button_height, button_height,  'Sprites/settings.png')
Button_Pause = Button_with_Image(True, 340, 15, 80, button_height,  'Sprites/pause1.png', 'Sprites/pause2.png', special_need=True)
Button_Draw_Size = Button_with_Image(False, 40, 30, button_width, button_height, 'Sprites/size.png', hover_image_path='Sprites/hovers/size2.png', image_path2='Sprites/hovers/da.png')
Button_Forces = Button(False, 40, 30 + 2*dy, button_width, button_height, 'Forces', int(40*FontSize))
Button_Gravity_Between_Objects = Button_with_Image(False, 40, 30, button_width, button_height, 'Sprites/allow_gravity.png', hover_image_path='Sprites/hovers/allow_gravity2.png', image_path2='Sprites/hovers/allow_gravity2.png', special_need=True)
Button_Cube_Elasticity = Button_with_Image(False, 40, 30 + dy, button_width, button_height, 'Sprites/elasticity.png', hover_image_path='Sprites/hovers/elasticity2.png', image_path2='Sprites/hovers/da.png')
Button_Ball_Elasticity = Button_with_Image(False, 40, 30 + 2*dy, button_width, button_height, 'Sprites/elasticity.png', hover_image_path='Sprites/hovers/elasticity2.png', image_path2='Sprites/hovers/da.png')
Button_Cube_Size = Button_with_Image(False, 40, 30, button_width, button_height, 'Sprites/size.png', hover_image_path='Sprites/hovers/size2.png', image_path2='Sprites/hovers/da.png')
Button_Ball_Mass = Button(False, 40, 30 + dy, button_width, button_height, 'Mass', int(40*FontSize))
Button_Ball_Radius = Button_with_Image(False, 40, 30, button_width, button_height, 'Sprites/radius.png', hover_image_path='Sprites/hovers/radius2.png', text_color='white', image_path2='Sprites/hovers/da.png')
Button_Draw = Button(False, 40, 30 + 2*dy, button_width, button_height, 'Draw', int(40*FontSize))
Button_CleanAll = Button_with_Image(False, 40, HEIGHT*0.88 - dy, button_width, button_height, 'Sprites/clean_all.png', hover_image_path='Sprites/hovers/clean_all2.png', image_path2='Sprites/hovers/da.png')
Button_Const1 = Button_with_Image(False, 40, 30, button_width, button_height, 'Sprites/gravity_y.png', hover_image_path='Sprites/hovers/gravity_y2.png', image_path2='Sprites/hovers/da.png')
Button_Const3 = Button_with_Image(False, 40, 30 + dy, button_width, button_height, 'Sprites/gravity_x.png', hover_image_path='Sprites/hovers/gravity_x2.png', image_path2='Sprites/hovers/da.png')
Button_Const2 = Button_with_Image(False, 40, 30 + 2*dy, button_width, button_height, 'Sprites/add_walls.png', hover_image_path='Sprites/hovers/add_walls2.png', image_path2='Sprites/hovers/da.png')
Button_Object1 = Button(False, 40, 30, button_width, button_height, 'Add Ball', int(40*FontSize))
Button_Object2 = Button(False, 40, 30 + dy, button_width, button_height, 'Add Cube', int(40*FontSize))
Button_Map1 = Button(False, 40, 30, button_width, button_height, 'Galton board', int(30*FontSize))
Button_Map2 = Button(False, 40, 30 + dy, button_width, button_height, "Newton's cradle", int(25*FontSize))
Button_Maps = Button_with_Image(True, 40, 30 + dy, button_width, button_height, 'Sprites/maps.png', hover_image_path='Sprites/hovers/maps2.png', image_path2='Sprites/hovers/da.png')
Button_Tools = Button_with_Image(True, 40, 30, button_width, button_height, 'Sprites/tools.png', hover_image_path='Sprites/hovers/tools2.png', image_path2='Sprites/hovers/da.png')
Button_WorldSettings = Button(False, 40, 30, button_width, button_height, 'World Settings', int(30*FontSize))
Button_AddObject = Button(False, 40, 30 + dy, button_width, button_height, 'Add Object', int(30*FontSize))
Button_GoBack = Button_with_Image(False, 40, HEIGHT*0.88, button_width, button_height, 'Sprites/go_back.png', hover_image_path='Sprites/hovers/go_back2.png', image_path2='Sprites/hovers/da.png')
Button_Show_Tempreature = Button(False, 40, 30 + 3*dy, button_width, button_height, 'Show Temperature', int(25*FontSize))


Button_Show_Tempreature.layer = [Button_CleanAll, Button_Const1, Button_Const2, Button_Const3, Button_GoBack, Button_Show_Tempreature, Button_Delete]
Button_Show_Tempreature.childrens = []

Button_Gas_Size.layer = [Button_CleanAll, Button_GoBack, Button_Gas_Mass, Button_Temperature, Button_Gas_Size, Button_Delete]
Button_Gas_Size.childrens = []

Button_Temperature.layer = [Button_CleanAll, Button_GoBack, Button_Gas_Mass, Button_Temperature, Button_Gas_Size, Button_Delete]
Button_Temperature.childrens = []

Button_Gas_Mass.layer = [Button_CleanAll, Button_GoBack, Button_Gas_Mass, Button_Temperature, Button_Gas_Size, Button_Delete]
Button_Gas_Mass.childrens = []

Button_Tools.childrens = [Button_Data, Button_WorldSettings, Button_Forces, Button_AddObject, Button_GoBack, Button_CleanAll, Button_Delete]
Button_Tools.layer = [Button_Tools, Button_Maps]

Button_Maps.layer = [Button_Tools, Button_Maps]
Button_Maps.childrens = [Button_Map1, Button_Map2, Button_GoBack, Button_CleanAll, Button_Delete, Button_Pendulum]

Button_AddObject.layer = [Button_Data, Button_Forces, Button_CleanAll, Button_AddObject, Button_WorldSettings, Button_GoBack, Button_Delete]
Button_AddObject.childrens = [Button_Add_Rope, Button_Add_Gas, Button_Add_Liquid, Button_Draw, Button_CleanAll, Button_Object1, Button_Object2, Button_GoBack, Button_Delete]

Button_Data.layer = [Button_Data, Button_Forces, Button_CleanAll, Button_AddObject, Button_WorldSettings, Button_GoBack, Button_Delete]
Button_Data.childrens = [Button_Tracing, Button_Show_Full_Energy, Button_Show_Potential_Energy, Button_Show_Kinetic_Energy, Button_Show_Acceleration, Button_Show_Velocity, Button_GoBack, Button_Delete, Button_CleanAll]

Button_Show_Velocity.layer = [Button_Tracing, Button_Show_Full_Energy, Button_Show_Potential_Energy, Button_Show_Kinetic_Energy, Button_Show_Acceleration, Button_Show_Velocity, Button_GoBack, Button_Delete, Button_CleanAll]
Button_Show_Acceleration.layer = [Button_Tracing, Button_Show_Full_Energy, Button_Show_Potential_Energy, Button_Show_Kinetic_Energy, Button_Show_Acceleration, Button_Show_Velocity, Button_GoBack, Button_Delete, Button_CleanAll]
Button_Show_Kinetic_Energy.layer = [Button_Tracing, Button_Show_Full_Energy, Button_Show_Potential_Energy, Button_Show_Kinetic_Energy, Button_Show_Acceleration, Button_Show_Velocity, Button_GoBack, Button_Delete, Button_CleanAll]
Button_Show_Potential_Energy.layer = [Button_Tracing, Button_Show_Full_Energy, Button_Show_Potential_Energy, Button_Show_Kinetic_Energy, Button_Show_Acceleration, Button_Show_Velocity, Button_GoBack, Button_Delete, Button_CleanAll]
Button_Show_Full_Energy.layer =  [Button_Tracing, Button_Show_Full_Energy, Button_Show_Potential_Energy, Button_Show_Kinetic_Energy, Button_Show_Acceleration, Button_Show_Velocity, Button_GoBack, Button_Delete, Button_CleanAll]
Button_Tracing.layer = [Button_Tracing, Button_Show_Full_Energy, Button_Show_Potential_Energy, Button_Show_Kinetic_Energy, Button_Show_Acceleration, Button_Show_Velocity, Button_GoBack, Button_Delete, Button_CleanAll]

Button_WorldSettings.layer = [Button_Data, Button_Forces, Button_CleanAll, Button_WorldSettings, Button_AddObject, Button_GoBack, Button_Delete]
Button_WorldSettings.childrens = [Button_CleanAll, Button_Const1, Button_Const2, Button_Const3, Button_GoBack, Button_Show_Tempreature, Button_Delete]

Button_Object1.layer = [Button_Add_Rope, Button_Add_Gas, Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll, Button_Delete]
Button_Object1.childrens = [Button_Ball_Elasticity, Button_Ball_Radius, Button_Ball_Mass, Button_GoBack, Button_CleanAll, Button_Delete]

Button_Object2.layer = [Button_Add_Rope, Button_Add_Gas, Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll, Button_Delete]
Button_Object2.childrens = [Button_Cube_Mass, Button_Cube_Dynamic, Button_Cube_Elasticity, Button_Cube_Size, Button_GoBack, Button_CleanAll, Button_Delete]

Button_Add_Liquid.layer = [Button_Add_Rope, Button_Add_Gas, Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll]
Button_Add_Liquid.childrens = []

Button_Add_Gas.layer = [Button_Add_Rope, Button_Add_Gas, Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll, Button_Delete]
Button_Add_Gas.childrens = [Button_Gas_Size, Button_Temperature, Button_Gas_Mass, Button_GoBack, Button_CleanAll, Button_Delete]

Button_Draw.layer = [Button_Add_Rope, Button_Add_Gas, Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll, Button_Delete]
Button_Draw.childrens = [Button_Draw_Size, Button_GoBack, Button_CleanAll, Button_Delete]

Button_Add_Rope.layer = [Button_Add_Rope, Button_Add_Gas, Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll, Button_Delete]

Button_Forces.childrens = [Button_GoBack, Button_CleanAll, Button_Gravity_Between_Objects, Button_Delete]
Button_Forces.layer = [Button_Data, Button_Forces, Button_CleanAll, Button_AddObject, Button_WorldSettings, Button_GoBack, Button_Delete]

Button_Const1.layer = [Button_CleanAll, Button_Const1, Button_Const2, Button_Const3, Button_GoBack, Button_Show_Tempreature, Button_Delete]
Button_Const3.layer = [Button_CleanAll, Button_Const1, Button_Const2, Button_Const3, Button_GoBack, Button_Show_Tempreature, Button_Delete]
Button_Gravity_Between_Objects.layer = [Button_CleanAll, Button_Const1, Button_Const2, Button_Const3, Button_GoBack, Button_Show_Tempreature, Button_Delete]

Button_Ball_Radius.layer = [Button_CleanAll, Button_GoBack, Button_Ball_Mass, Button_Ball_Radius, Button_Ball_Elasticity, Button_Delete]
Button_Ball_Mass.layer = [Button_CleanAll, Button_GoBack, Button_Ball_Mass, Button_Ball_Radius, Button_Ball_Elasticity, Button_Delete]
Button_Cube_Size.layer = [Button_Cube_Mass, Button_Cube_Dynamic, Button_Cube_Elasticity, Button_Cube_Size, Button_GoBack, Button_CleanAll, Button_Delete]
Button_Cube_Elasticity.layer = [Button_Cube_Mass, Button_Cube_Dynamic, Button_Cube_Elasticity, Button_Cube_Size, Button_GoBack, Button_CleanAll, Button_Delete]
Button_Cube_Dynamic.layer = [Button_Cube_Mass, Button_Cube_Dynamic, Button_Cube_Elasticity, Button_Cube_Size, Button_GoBack, Button_CleanAll, Button_Delete]
Button_Ball_Elasticity.layer = [Button_CleanAll, Button_GoBack, Button_Ball_Mass, Button_Ball_Radius, Button_Ball_Elasticity, Button_Delete]
Button_Cube_Mass.layer = [Button_Cube_Mass, Button_Cube_Dynamic, Button_Cube_Elasticity, Button_Cube_Size, Button_GoBack, Button_CleanAll, Button_Delete]

Button_Show_Acceleration.parent = Button_Data
Button_Show_Potential_Energy.parent = Button_Data
Button_Show_Kinetic_Energy.parent = Button_Data
Button_Show_Velocity.parent = Button_Data
Button_Show_Full_Energy.parent = Button_Data
Button_Tracing.parent = Button_Data
Button_Data.parent = Button_Tools
Button_Pendulum.parent = Button_Maps
Button_Delete.parent = Button_Tools
Button_Add_Rope.parent = Button_AddObject
Button_Cube_Mass.parent = Button_Object2
Button_Cube_Dynamic.parent = Button_Object2
Button_Gas_Size.parent = Button_Add_Gas
Button_Temperature.parent = Button_Add_Gas
Button_Gas_Mass.parent = Button_Add_Gas
Button_Add_Gas.parent = Button_AddObject
Button_Add_Liquid.parent = Button_AddObject
Button_Gravity_Between_Objects.parent = Button_Forces
Button_Cube_Elasticity.parent = Button_Object2
Button_Ball_Elasticity.parent = Button_Object1
Button_Cube_Size.parent = Button_Object2
Button_Ball_Mass.parent = Button_Object1
Button_Ball_Radius.parent = Button_Object1
Button_Const3.parent = Button_WorldSettings
Button_Const1.parent = Button_WorldSettings
Button_Const2.parent = Button_WorldSettings
Button_Object2.parent = Button_AddObject
Button_Object1.parent = Button_AddObject
Button_Draw.parent = Button_AddObject
Button_WorldSettings.parent = Button_Tools
Button_AddObject.parent = Button_Tools
Button_Forces.parent = Button_Tools
Button_Map2.parent = Button_Maps
Button_Show_Tempreature.parent = Button_WorldSettings

settings = {
    "language": "English",
    "volume": 25
}


def save_callback(new_settings):
    global settings
    settings.update(new_settings)
    print("Updated settings:", new_settings)


create_wall(space, 40, 2000, (300, 500), (255, 255, 255), 1, 0)
Objects = []
Joints = []
Velocity_Tracing_Objects = []
Acceleration_Tracing_Objects = []
Kinetic_Tracing_Objects = []
Potential_Tracing_Objects = []
Full_Tracing_Objects = []
Position_Tracing_Objects = []
Buttons = [Button_Tracing, Button_Show_Potential_Energy, Button_Show_Kinetic_Energy, Button_Show_Velocity, Button_Show_Acceleration, Button_Show_Full_Energy, Button_Data, Button_Pendulum, Button_Delete, Button_Add_Rope, Button_Cube_Mass, Button_Cube_Dynamic, Button_Show_Tempreature, Button_Gas_Size, Button_Temperature, Button_Gas_Mass, Button_Add_Gas, Button_Add_Liquid, Button_Pause, Button_Settings, Button_Draw_Size, Button_Forces, Button_Gravity_Between_Objects, Button_Cube_Elasticity, Button_Ball_Elasticity, Button_Cube_Size, Button_Ball_Radius, Button_Ball_Mass ,Button_Const3, Button_Draw, Button_Tools, Button_GoBack, Button_AddObject, Button_WorldSettings, Button_Maps, Button_Map1, Button_Map2, Button_Object1, Button_Object2, Button_Const2, Button_Const1, Button_CleanAll,]
Top_Layer = Button_Tools.layer
ActivatedButton = None
Gravity_Y = 1000
Gravity_X = 0
Ball_Radius = 30
Liquid_Radiuss = 30
Liquid_Mass = 1
Gas_Temp = 1000
Gas_Mass = 0.1
Gas_Radiuss = 30
Cube_Size = 50
Draw_Size = 20
Ball_Mass = 1
Cube_Mass = 1
Ball_Elasticity = 0.8
Cube_Elasticity = 0.8
Allow_Gravity = False
Show_Temperature = False
G = 10000
mouse = Mouse(None, Ball_Radius, Cube_Size, Draw_Size, Liquid_Radiuss, Gas_Radiuss, Cube_Mass)
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
mouse_joint = None
paused = False
Cube_Dynamic = False
Deleting = False
Showing_Velocity = False
Showing_Acceleration = False
Showing_Kinetic_Energy = False
Showing_Potential_Energy = False
Showing_Full_Energy = False
trace_points_list = []
trace_point_colors = []
Tracing = False
prev_vx = []
prev_vy = []

while running:
    # print(f'Bodies: {space.bodies}')
    # print(f'Shapes: {space.shapes}')
    # print(Objects)
    mouse_body.position = pygame.mouse.get_pos()
    screen.fill((0, 0, 0))
    space.debug_draw(draw_options)
    mouse.space = space
    # prev_vx = [obj.body.velocity[0] for obj in Acceleration_Tracing_Objects]
    # prev_vy = [obj.body.velocity[1] for obj in Acceleration_Tracing_Objects]

    if paused == False:
        prev_vx = [obj.body.velocity[0] for obj in Acceleration_Tracing_Objects]
        prev_vy = [obj.body.velocity[1] for obj in Acceleration_Tracing_Objects]
        space.step(1 / FPS)
        water_particles = [obj for obj in Objects if isinstance(obj, Water_Particle)]
        water_particles_shapes = [obj.shape for obj in Objects if isinstance(obj, Water_Particle)]
        gas_particles = [obj for obj in Objects if isinstance(obj, gas_Class.Gas_Particle)]
        gas_particles_shapes = [obj.shape for obj in Objects if isinstance(obj, gas_Class.Gas_Particle)]
        dynamic = [obj for obj in Objects if obj.body.body_type == pymunk.Body.DYNAMIC]


        for obj in water_particles:
            for ob in water_particles:
                if obj is ob:
                    continue
                if (obj.body.position[0] - ob.body.position[0])**2 - (obj.body.position[1] - ob.body.position[1])**2 <= 10000:
                    a = apply_surface_tension_acceleration(obj, ob, 7)
                    obj.body.velocity += pymunk.Vec2d(a[0], a[1]) * (1 / FPS)

        if Allow_Gravity:
            for obj in dynamic:
                for ob in dynamic + water_particles + gas_particles:
                    if ob != obj:
                        a = apply_gravity_acceleration(obj, ob, G)
                        obj.body.velocity += pymunk.Vec2d(a[0], a[1]) * (1 / FPS)

            for obj in water_particles:
                for ob in dynamic + water_particles + gas_particles:
                    if ob != obj:
                        a = apply_gravity_acceleration(obj, ob, G)
                        obj.body.velocity += pymunk.Vec2d(a[0], a[1]) * (1 / FPS)

            for obj in gas_particles:
                for ob in  dynamic + water_particles + gas_particles:
                    if ob != obj:
                        a = apply_gravity_acceleration(obj, ob, G)
                        obj.body.velocity += pymunk.Vec2d(a[0], a[1]) * (1 / FPS)

        if Show_Temperature:
            for obj in gas_particles:
                grad = math.exp(-0.0005 * obj.body.velocity.length)
                obj.particle.color = ((1 - grad) * 255, 0, 0, 255)

        for obj in Objects:
            if obj.body in space.bodies:
                if obj.body.position[0] < 300:
                    if obj in Velocity_Tracing_Objects:
                        Velocity_Tracing_Objects.remove(obj)

                    if obj in Acceleration_Tracing_Objects:
                        Acceleration_Tracing_Objects.remove(obj)

                    if obj in Kinetic_Tracing_Objects:
                        Kinetic_Tracing_Objects.remove(obj)

                    if obj in Potential_Tracing_Objects:
                        Potential_Tracing_Objects.remove(obj)

                    if obj in Full_Tracing_Objects:
                        Full_Tracing_Objects.remove(obj)

                    if obj in Position_Tracing_Objects:
                        ind = Position_Tracing_Objects.index(obj)
                        del trace_points_list[ind]
                        del trace_point_colors[ind]
                        Position_Tracing_Objects.remove(obj)

                    if isinstance(obj, pymunk.Segment):
                        pass
                    elif isinstance(obj, Water_Particle):
                        space.remove(obj.particle, obj.body)
                        Objects.remove(obj)
                    elif isinstance(obj, gas_Class.Gas_Particle):
                        space.remove(obj.particle, obj.body)
                        Objects.remove(obj)
                    else:
                        space.remove(obj, obj.body)
                        Objects.remove(obj)

            if obj.body in space.bodies:
                if obj.body.position[1] > 10000:

                    if obj in Velocity_Tracing_Objects:
                        Velocity_Tracing_Objects.remove(obj)

                    if obj in Acceleration_Tracing_Objects:
                        Acceleration_Tracing_Objects.remove(obj)

                    if obj in Kinetic_Tracing_Objects:
                        Kinetic_Tracing_Objects.remove(obj)

                    if obj in Potential_Tracing_Objects:
                        Potential_Tracing_Objects.remove(obj)

                    if obj in Full_Tracing_Objects:
                        Full_Tracing_Objects.remove(obj)

                    if obj in Position_Tracing_Objects:
                        ind = Position_Tracing_Objects.index(obj)
                        del trace_points_list[ind]
                        del trace_point_colors[ind]
                        Position_Tracing_Objects.remove(obj)

                    if isinstance(obj, pymunk.Segment):
                        space.remove(obj)
                    if obj.body in space.bodies:
                        if isinstance(obj, Water_Particle):
                            space.remove(obj.particle, obj.body)
                        elif isinstance(obj, gas_Class.Gas_Particle):
                            space.remove(obj.particle, obj.body)
                        else:
                            space.remove(obj, obj.body)

        if len(Objects) > 2000:
            last_obj = Objects.pop()
            if last_obj in Velocity_Tracing_Objects:
                Velocity_Tracing_Objects.remove(last_obj)

            if last_obj in Acceleration_Tracing_Objects:
                Acceleration_Tracing_Objects.remove(last_obj)

            if last_obj in Kinetic_Tracing_Objects:
                Kinetic_Tracing_Objects.remove(last_obj)

            if last_obj in Potential_Tracing_Objects:
                Potential_Tracing_Objects.remove(last_obj)

            if last_obj in Full_Tracing_Objects:
                Full_Tracing_Objects.remove(last_obj)

            if last_obj in Position_Tracing_Objects:
                ind = Position_Tracing_Objects.index(last_obj)
                del trace_points_list[ind]
                del trace_point_colors[ind]
                Position_Tracing_Objects.remove(last_obj)

            if isinstance(last_obj, pymunk.Segment):
                space.remove(last_obj)
            if last_obj.body in space.bodies:
                if isinstance(last_obj, Water_Particle):
                    space.remove(last_obj.particle, last_obj.body)
                elif isinstance(last_obj, gas_Class.Gas_Particle):
                    space.remove(last_obj.particle, last_obj.body)
                else:
                    space.remove(last_obj, last_obj.body)

    if Position_Tracing_Objects:
        for ball_for_trace, trace_points, color in zip(Position_Tracing_Objects, trace_points_list, trace_point_colors):
            trace_points.append((int(ball_for_trace.body.position.x), int(ball_for_trace.body.position.y)))
            if len(trace_points) > 1:
                pygame.draw.lines(screen, color, False, trace_points, 2)

    for obj in Kinetic_Tracing_Objects:
        start = obj.body.position
        vx, vy = obj.body.velocity
        length = obj.body.mass * (vy ** 2 + vx ** 2)/2
        draw_text(screen, start, 0.2*length, math.radians(30),-30, color = (0, 255, 0))

    for obj in Potential_Tracing_Objects:
        if not Allow_Gravity:
            start = obj.body.position
            length = obj.body.mass * Gravity_Y * (HEIGHT - obj.body.position[1]) + obj.body.mass * Gravity_X * (WIDTH - obj.body.position[0])
            draw_text(screen, start, 0.2*length, math.radians(30),0, color = (255, 0, 255))

    for obj in Full_Tracing_Objects:
        start = obj.body.position
        vx, vy = obj.body.velocity
        length1 = obj.body.mass * (vy ** 2 + vx ** 2) / 2
        if not Allow_Gravity:
            length2 = obj.body.mass * Gravity_Y * (HEIGHT - obj.body.position[1]) + obj.body.mass * Gravity_X * (WIDTH - obj.body.position[0])
        length = length1 + length2
        draw_text(screen, start, 0.2 * length, math.radians(30), 30, color=(255, 155, 0))


    for obj in Velocity_Tracing_Objects:
        start = obj.body.position
        vx, vy = obj.body.velocity
        length = math.sqrt(vy ** 2 + vx ** 2)
        if vx == 0 and vy == 0:
            pass
        else:
            angle = math.atan2(vy, vx)
            draw_arrow_angle(screen, start, 0.2 * length, angle, (0, 0, 255))

    for obj_index in range(len(Acceleration_Tracing_Objects)):
        obj = Acceleration_Tracing_Objects[obj_index]
        start = obj.body.position
        vx, vy = obj.body.velocity
        if prev_vx and prev_vy:
            vx_prev = prev_vx[obj_index]
            vy_prev = prev_vy[obj_index]
            dvx = vx - vx_prev
            dvy = vy - vy_prev
            length = math.sqrt(dvy ** 2 + dvx ** 2) * FPS
            if dvx == 0 and dvy == 0:
                pass
            else:
                angle = math.atan2(dvy, dvx)
                draw_arrow_angle(screen, start, 0.2 * length, angle)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if Button_Settings.is_clicked(event) and Button_Settings.is_seen:
            open_settings_window(screen, settings, save_callback)

        if Button_Show_Potential_Energy.is_clicked(event) and Button_Show_Potential_Energy.is_seen:
            if Showing_Potential_Energy == False:
                for button_ in Button_Show_Velocity.layer:
                    button_.button_color = (169, 169, 169)
                Button_Show_Potential_Energy.button_color = (119, 136, 153)
                Showing_Potential_Energy = True
                mouse.state = 'Showing Potential Energy'
            else:
                Button_Show_Potential_Energy.button_color = (169, 169, 169)
                Showing_Potential_Energy = False
                mouse.state = None

        if Button_Data.is_clicked(event) and Button_Data.is_seen:
            for button in Button_Data.layer:
                button.is_seen = False
            for button in Button_Data.childrens:
                button.is_seen = True
            Button_GoBack.layer = Button_Data.childrens
            Button_GoBack.childrens = Button_Data.layer
            Button_GoBack.parent = Button_Data

        if Button_Map1.is_clicked(event) and Button_Map1.is_seen:
            Tracing = False
            trace_points = []
            Velocity_Tracing_Objects.clear()
            Acceleration_Tracing_Objects.clear()
            Kinetic_Tracing_Objects.clear()
            Potential_Tracing_Objects.clear()
            Full_Tracing_Objects.clear()
            Position_Tracing_Objects.clear()
            trace_point_colors.clear()
            trace_points_list.clear()
            for joint_ in Joints:
                space.remove(joint_)
            for obj in Objects:
                if isinstance(obj, pymunk.Segment):
                    space.remove(obj)
                if obj.body in space.bodies:
                    if isinstance(obj, Water_Particle):
                        space.remove(obj.particle, obj.body)
                    elif isinstance(obj, gas_Class.Gas_Particle):
                        space.remove(obj.particle, obj.body)
                    else:
                        space.remove(obj, obj.body)
            Objects = CreateMap1(space)
            Joints.clear()

        if Button_Pendulum.is_clicked(event) and Button_Pendulum.is_seen:
            Velocity_Tracing_Objects.clear()
            Acceleration_Tracing_Objects.clear()
            Kinetic_Tracing_Objects.clear()
            Potential_Tracing_Objects.clear()
            Full_Tracing_Objects.clear()
            Position_Tracing_Objects.clear()
            trace_point_colors.clear()
            trace_points_list.clear()
            for joint_ in Joints:
                space.remove(joint_)
            for obj in Objects:
                if isinstance(obj, pymunk.Segment):
                    space.remove(obj)
                if obj.body in space.bodies:
                    if isinstance(obj, Water_Particle):
                        space.remove(obj.particle, obj.body)
                    elif isinstance(obj, gas_Class.Gas_Particle):
                        space.remove(obj.particle, obj.body)
                    else:
                        space.remove(obj, obj.body)
            Map = CreateMap3(space)
            Objects = Map[0]
            Position_Tracing_Objects = Map[0].copy()
            Joints = Map[1]

        if Button_Map2.is_clicked(event) and Button_Map2.is_seen:
            Velocity_Tracing_Objects.clear()
            Acceleration_Tracing_Objects.clear()
            Kinetic_Tracing_Objects.clear()
            Potential_Tracing_Objects.clear()
            Full_Tracing_Objects.clear()
            Position_Tracing_Objects.clear()
            Tracing = False
            trace_point_colors.clear()
            trace_points_list.clear()
            for joint_ in Joints:
                space.remove(joint_)
            for obj in Objects:
                if isinstance(obj, pymunk.Segment):
                    space.remove(obj)
                if obj.body in space.bodies:
                    if isinstance(obj, Water_Particle):
                        space.remove(obj.particle, obj.body)
                    elif isinstance(obj, gas_Class.Gas_Particle):
                        space.remove(obj.particle, obj.body)
                    else:
                        space.remove(obj, obj.body)
            Map = CreateMap2(space)
            Objects = Map[0]
            Joints = Map[1]

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            paused = not paused
            if Button_Pause.image == Button_Pause.image1:
                Button_Pause.image = Button_Pause.image2
            elif Button_Pause.image == Button_Pause.image2:
                Button_Pause.image = Button_Pause.image1

        if Button_Gas_Size.is_clicked(event) and Button_Gas_Size.is_seen and Button_Gas_Size.activated == False:
            for button in Button_Gas_Size.layer:
                button.activated = False
            Button_Gas_Size.activated = True
            ActivatedButton = Button_Gas_Size

        if Button_Cube_Dynamic.is_clicked(event) and Button_Cube_Dynamic.is_seen:
            if Cube_Dynamic == False:
                Button_Cube_Dynamic.button_color = (119, 136, 153)
                Cube_Dynamic = True
            else:
                Button_Cube_Dynamic.button_color = (169, 169, 169)
                Cube_Dynamic = False

        if Button_Cube_Mass.is_clicked(event) and Button_Cube_Mass.is_seen and Button_Cube_Mass.activated == False:
            for button in Button_Cube_Mass.layer:
                button.activated = False
            Button_Cube_Mass.activated = True
            ActivatedButton = Button_Cube_Mass

        if Button_Temperature.is_clicked(event) and Button_Temperature.is_seen and Button_Temperature.activated == False:
            for button in Button_Temperature.layer:
                button.activated = False
            Button_Temperature.activated = True
            ActivatedButton = Button_Temperature

        if Button_Gas_Mass.is_clicked(event) and Button_Gas_Mass.is_seen and Button_Gas_Mass.activated == False:
            for button in Button_Gas_Mass.layer:
                button.activated = False
            Button_Gas_Mass.activated = True
            ActivatedButton = Button_Gas_Mass

        if Button_Add_Gas.is_clicked(event) and Button_Add_Gas.is_seen and event.button == 3:
            for button in Button_Add_Gas.layer:
                button.is_seen = False
            for button in Button_Add_Gas.childrens:
                button.is_seen = True
            Button_GoBack.layer = Button_Add_Gas.childrens
            Button_GoBack.childrens = Button_Add_Gas.layer
            Button_GoBack.parent = Button_Add_Gas

        if Button_Pause.is_clicked(event) and Button_Pause.is_seen:
            paused = not paused

        if Button_Add_Gas.is_clicked(event) and Button_Add_Gas.is_seen and event.button != 3 and not Deleting:
            mouse.state = 'ReadyToAddGas'

        if Button_Object1.is_clicked(event) and Button_Object1.is_seen and event.button != 3 and not Deleting:
            mouse.state = 'ReadyToAddBall'

        if Button_Object2.is_clicked(event) and Button_Object2.is_seen and not Deleting:
            mouse.state = 'ReadyToAddCube'

        if Button_Draw.is_clicked(event) and Button_Draw.is_seen and event.button != 3 and not Deleting:
            mouse.state = 'ReadyToAddDraw'

        if Button_Add_Liquid.is_clicked(event) and Button_Add_Liquid.is_seen and event.button != 3 and not Deleting:
            mouse.state = 'ReadyToAddLiquid'

        if Button_Add_Rope.is_clicked(event) and Button_Add_Rope.is_seen and event.button != 3 and not Deleting:
            mouse.state = 'ReadyToAddRope'

        if Button_Draw_Size.is_clicked(event) and Button_Draw_Size.is_seen and Button_Draw_Size.activated == False:
            for button in Button_Draw_Size.layer:
                button.activated = False
            Button_Draw_Size.activated = True
            ActivatedButton = Button_Draw_Size

        if Button_Draw.is_clicked(event) and Button_Draw.is_seen and event.button == 3:
            for button in Button_Draw.layer:
                button.is_seen = False
            for button in Button_Draw.childrens:
                button.is_seen = True
            Button_GoBack.layer = Button_Draw.childrens
            Button_GoBack.childrens = Button_Draw.layer
            Button_GoBack.parent = Button_Draw

        if Button_Object1.is_clicked(event) and Button_Object1.is_seen and event.button == 3:
            for button in Button_Object1.layer:
                button.is_seen = False
            for button in Button_Object1.childrens:
                button.is_seen = True
            Button_GoBack.layer = Button_Object1.childrens
            Button_GoBack.childrens = Button_Object1.layer
            Button_GoBack.parent = Button_Object1

        if Button_Object2.is_clicked(event) and Button_Object2.is_seen and event.button == 3:
            for button in Button_Object2.layer:
                button.is_seen = False
            for button in Button_Object2.childrens:
                button.is_seen = True
            Button_GoBack.layer = Button_Object2.childrens
            Button_GoBack.childrens = Button_Object2.layer
            Button_GoBack.parent = Button_Object2

        if Button_Cube_Size.is_clicked(event) and Button_Cube_Size.is_seen and Button_Cube_Size.activated == False:
            for button in Button_Cube_Size.layer:
                button.activated = False
            Button_Cube_Size.activated = True
            ActivatedButton = Button_Cube_Size

        if Button_Cube_Elasticity.is_clicked(event) and Button_Cube_Elasticity.is_seen and Button_Cube_Elasticity.activated == False and event.button != 3:
            for button in Button_Cube_Elasticity.layer:
                button.activated = False
            Button_Cube_Elasticity.activated = True
            ActivatedButton = Button_Cube_Elasticity

        if Button_Ball_Radius.is_clicked(event) and Button_Ball_Radius.is_seen and Button_Ball_Radius.activated == False and event.button != 3:
            for button in Button_Ball_Radius.layer:
                button.activated = False
            Button_Ball_Radius.activated = True
            ActivatedButton = Button_Ball_Radius

        if Button_Ball_Elasticity.is_clicked(event) and Button_Ball_Elasticity.is_seen and Button_Ball_Elasticity.activated == False:
            for button in Button_Ball_Elasticity.layer:
                button.activated = False
            Button_Ball_Elasticity.activated = True
            ActivatedButton = Button_Ball_Elasticity

        if Button_Ball_Mass.is_clicked(event) and Button_Ball_Mass.is_seen and Button_Ball_Mass.activated == False:
            for button in Button_Ball_Mass.layer:
                button.activated = False
            Button_Ball_Mass.activated = True
            ActivatedButton = Button_Ball_Mass

        if Button_Const1.is_clicked(event) and Button_Const1.is_seen and Button_Const1.activated == False:
            for button in Button_Const1.layer:
                button.activated = False
            Button_Const1.activated = True
            ActivatedButton = Button_Const1

        if Button_Const3.is_clicked(event) and Button_Const3.is_seen and Button_Const3.activated == False:
            for button in Button_Const3.layer:
                button.activated = False
            Button_Const3.activated = True
            ActivatedButton = Button_Const3

        if Button_Gravity_Between_Objects.is_clicked(event) and Button_Gravity_Between_Objects.is_seen:
            if Allow_Gravity == False:
                Button_Gravity_Between_Objects.button_color = (119,136,153)
                Allow_Gravity = True
            else:
                Button_Gravity_Between_Objects.button_color = (169, 169, 169)
                Allow_Gravity = False

        if Button_Show_Tempreature.is_clicked(event) and Button_Show_Tempreature.is_seen:
            if Show_Temperature == False:
                Button_Show_Tempreature.button_color = (119, 136, 153)
                Show_Temperature = True
            else:
                for gaspart in gas_particles:
                    gaspart.particle.color = (100, 255, 255, 255)
                Button_Show_Tempreature.button_color = (169, 169, 169)
                Show_Temperature = False

        if Button_Forces.is_clicked(event) and Button_Forces.is_seen:
            for button in Button_Forces.layer:
                button.is_seen = False
            for button in Button_Forces.childrens:
                button.is_seen = True
            Button_GoBack.layer = Button_Forces.childrens
            Button_GoBack.childrens = Button_Forces.layer
            Button_GoBack.parent = Button_Forces

        if Button_Const2.is_clicked(event) and Button_Const2.is_seen:
            wall1 = create_wall(space, 40, HEIGHT*10/9, (WIDTH, 500), (255, 255, 255), 1, 0)
            wall2 = create_wall(space, WIDTH, 40, (WIDTH / 2, 0), (255, 255, 255), 1, 0)
            wall3 = create_wall(space, WIDTH, 40, (WIDTH / 2, HEIGHT), (255, 255, 255), 1, 0)
            Objects.append(wall1)
            Objects.append(wall2)
            Objects.append(wall3)

        if Button_CleanAll.is_clicked(event) and Button_CleanAll.is_seen:
            Tracing = False
            trace_point_colors.clear()
            trace_points_list.clear()
            Velocity_Tracing_Objects.clear()
            Acceleration_Tracing_Objects.clear()
            Kinetic_Tracing_Objects.clear()
            Potential_Tracing_Objects.clear()
            Full_Tracing_Objects.clear()
            Position_Tracing_Objects.clear()
            for joint_ in Joints:
                space.remove(joint_)
            for obj in Objects:
                if isinstance(obj, pymunk.Segment):
                    space.remove(obj)
                if obj.body in space.bodies:
                    if isinstance(obj, Water_Particle):
                        space.remove(obj.particle, obj.body)
                    elif isinstance(obj,gas_Class.Gas_Particle):
                        space.remove(obj.particle, obj.body)
                    else:
                        space.remove(obj, obj.body)
            Objects.clear()
            Joints.clear()

        if Button_WorldSettings.is_clicked(event) and Button_WorldSettings.is_seen:
            for button in Button_WorldSettings.layer:
                button.is_seen = False
            for button in Button_WorldSettings.childrens:
                button.is_seen = True
            Button_GoBack.layer = Button_WorldSettings.childrens
            Button_GoBack.childrens = Button_WorldSettings.layer
            Button_GoBack.parent = Button_WorldSettings

        if Button_Tools.is_clicked(event) and Button_Tools.is_seen:
            for button in Button_Tools.layer:
                button.is_seen = False
            for button in Button_Tools.childrens:
                button.is_seen = True
            Button_GoBack.layer = Button_Tools.childrens
            Button_GoBack.childrens = Button_Tools.layer
            Button_GoBack.parent = Button_Tools

        if Button_Maps.is_clicked(event) and Button_Maps.is_seen:
            for button in Button_Maps.layer:
                button.is_seen = False
            for button in Button_Maps.childrens:
                button.is_seen = True
            Button_GoBack.layer = Button_Maps.childrens
            Button_GoBack.childrens = Button_Maps.layer
            Button_GoBack.parent = Button_Maps

        if Button_AddObject.is_clicked(event) and Button_AddObject.is_seen:
            for button in Button_AddObject.layer:
                button.is_seen = False
            for button in Button_AddObject.childrens:
                button.is_seen = True
            Button_GoBack.layer = Button_AddObject.childrens
            Button_GoBack.childrens = Button_AddObject.layer
            Button_GoBack.parent = Button_AddObject

        if Button_GoBack.is_clicked(event) and Button_GoBack.is_seen:
            mouse.state = None
            ActivatedButton = None
            Button_Show_Velocity.button_color = (169, 169, 169)
            Button_Show_Acceleration.button_color = (169, 169, 169)
            Button_Show_Kinetic_Energy.button_color = (169, 169, 169)
            Button_Show_Potential_Energy.button_color = (169, 169, 169)
            Button_Show_Full_Energy.button_color = (169, 169, 169)
            Button_Tracing.button_color = (169, 169, 169)
            for button in Button_GoBack.layer:
                button.activated = False
                button.is_seen = False
            for button in Button_GoBack.childrens:
                button.is_seen = True
            Button_GoBack.layer = Button_GoBack.childrens
            if Button_GoBack.parent.parent:
                Button_GoBack.childrens = Button_GoBack.parent.parent.layer
                Button_GoBack.parent = Button_GoBack.parent.parent

        state = mouse.getstate(event, screen)

        if Button_Tracing.is_clicked(event) and Button_Tracing.is_seen:
            if Tracing == False:
                for button_ in Button_Tracing.layer:
                    button_.button_color = (169, 169, 169)
                Button_Tracing.button_color = (119, 136, 153)
                Tracing = True
                mouse.state = 'Trace Prep'
            else:
                Button_Tracing.button_color = (169, 169, 169)
                Tracing = False
                mouse.state = None

        if Button_Show_Velocity.is_clicked(event) and Button_Show_Velocity.is_seen:
            if Showing_Velocity == False:
                for button_ in Button_Show_Velocity.layer:
                    button_.button_color = (169, 169, 169)
                Button_Show_Velocity.button_color = (119, 136, 153)
                Showing_Velocity = True
                mouse.state = 'Showing Velocity'
            else:
                Button_Show_Velocity.button_color = (169, 169, 169)
                Showing_Velocity = False
                mouse.state = None

        if Button_Show_Acceleration.is_clicked(event) and Button_Show_Acceleration.is_seen:
            if Showing_Acceleration == False:
                for button_ in Button_Show_Velocity.layer:
                    button_.button_color = (169, 169, 169)
                Button_Show_Acceleration.button_color = (119, 136, 153)
                Showing_Acceleration = True
                mouse.state = 'Showing Acceleration'
            else:
                Button_Show_Acceleration.button_color = (169, 169, 169)
                Showing_Acceleration = False
                mouse.state = None

        if Button_Show_Full_Energy.is_clicked(event) and Button_Show_Full_Energy.is_seen:
            if Showing_Full_Energy == False:
                for button_ in Button_Show_Velocity.layer:
                    button_.button_color = (169, 169, 169)
                Button_Show_Full_Energy.button_color = (119, 136, 153)
                Showing_Full_Energy = True
                mouse.state = 'Showing Full Energy'
            else:
                Button_Show_Full_Energy.button_color = (169, 169, 169)
                Showing_Full_Energy = False
                mouse.state = None

        if Button_Show_Kinetic_Energy.is_clicked(event) and Button_Show_Kinetic_Energy.is_seen:
            if Showing_Kinetic_Energy == False:
                for button_ in Button_Show_Velocity.layer:
                    button_.button_color = (169, 169, 169)
                Button_Show_Kinetic_Energy.button_color = (119, 136, 153)
                Showing_Kinetic_Energy = True
                mouse.state = 'Showing Kinetic Energy'
            else:
                Button_Show_Kinetic_Energy.button_color = (169, 169, 169)
                Showing_Kinetic_Energy = False
                mouse.state = None


        if Button_Delete.is_clicked(event) and Button_Delete.is_seen:
            if Deleting == False:
                Button_Delete.button_color = (119, 136, 153)
                Deleting = True
                mouse.state = 'Deleting'
            else:
                Button_Delete.button_color = (169, 169, 169)
                Deleting = False
                mouse.state = None

        if state == 'DrawBall' and  event.button != 3:
            ball = mouse.Add_Ball(space, (mouse.mouse_x, mouse.mouse_y), Ball_Radius, mass=Ball_Mass, elasticity=Ball_Elasticity, friction=0.5, color=(255, 255, 255, 100))
            Objects.append(ball)

        if state == 'Show Velocity':
            p = Vec2d(*event.pos)
            hit = space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if hit:
                hit_shape = hit.shape
                body = hit_shape.body
                if (hit_shape in Objects or hit_shape in water_particles_shapes or hit_shape in gas_particles_shapes) and (hit_shape not in Velocity_Tracing_Objects):
                    Velocity_Tracing_Objects.append(hit_shape)
                elif hit_shape in Velocity_Tracing_Objects:
                    Velocity_Tracing_Objects.remove(hit_shape)

        if state == 'Show Acceleration':
            p = Vec2d(*event.pos)
            hit = space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if hit:
                hit_shape = hit.shape
                body = hit_shape.body
                if (hit_shape in Objects or hit_shape in water_particles_shapes or hit_shape in gas_particles_shapes) and (hit_shape not in Acceleration_Tracing_Objects):
                    Acceleration_Tracing_Objects.append(hit_shape)
                elif hit_shape in Acceleration_Tracing_Objects:
                    Acceleration_Tracing_Objects.remove(hit_shape)

        if state == 'Show Kinetic Energy':
            p = Vec2d(*event.pos)
            hit = space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if hit:
                hit_shape = hit.shape
                body = hit_shape.body
                if (hit_shape in Objects or hit_shape in water_particles_shapes or hit_shape in gas_particles_shapes) and (hit_shape not in Kinetic_Tracing_Objects):
                    Kinetic_Tracing_Objects.append(hit_shape)
                elif hit_shape in Kinetic_Tracing_Objects:
                    Kinetic_Tracing_Objects.remove(hit_shape)

        if state == 'Show Potential Energy':
            p = Vec2d(*event.pos)
            hit = space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if hit:
                hit_shape = hit.shape
                body = hit_shape.body
                if (hit_shape in Objects or hit_shape in water_particles_shapes or hit_shape in gas_particles_shapes) and (hit_shape not in Potential_Tracing_Objects):
                    Potential_Tracing_Objects.append(hit_shape)
                elif hit_shape in Potential_Tracing_Objects:
                    Potential_Tracing_Objects.remove(hit_shape)

        if state == 'Show Full Energy':
            p = Vec2d(*event.pos)
            hit = space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if hit:
                hit_shape = hit.shape
                body = hit_shape.body
                if (hit_shape in Objects or hit_shape in water_particles_shapes or hit_shape in gas_particles_shapes) and (hit_shape not in Full_Tracing_Objects):
                    Full_Tracing_Objects.append(hit_shape)
                elif hit_shape in Full_Tracing_Objects:
                    Full_Tracing_Objects.remove(hit_shape)

        if state == 'Trace':
            p = Vec2d(*event.pos)
            hit = space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if hit:
                hit_shape = hit.shape
                body = hit_shape.body
                if (hit_shape in Objects or hit_shape in water_particles_shapes or hit_shape in gas_particles_shapes) and (hit_shape not in Position_Tracing_Objects):
                    Position_Tracing_Objects.append(hit_shape)
                    trace_points_list.append([])
                    rnd_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                    trace_point_colors.append(rnd_color)
                elif hit_shape in Position_Tracing_Objects:
                    ind = Position_Tracing_Objects.index(hit_shape)
                    del trace_points_list[ind]
                    del trace_point_colors[ind]
                    Position_Tracing_Objects.remove(hit_shape)


        if state == 'Delete':
            p = Vec2d(*event.pos)
            hit = space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if hit:
                hit_shape = hit.shape
                body = hit_shape.body
                if hit_shape in Velocity_Tracing_Objects:
                    Velocity_Tracing_Objects.remove(hit_shape)

                if hit_shape in Acceleration_Tracing_Objects:
                    Acceleration_Tracing_Objects.remove(hit_shape)

                if hit_shape in Kinetic_Tracing_Objects:
                    Kinetic_Tracing_Objects.remove(hit_shape)

                if hit_shape in Potential_Tracing_Objects:
                    Potential_Tracing_Objects.remove(hit_shape)

                if hit_shape in Full_Tracing_Objects:
                    Full_Tracing_Objects.remove(hit_shape)

                if hit_shape in Position_Tracing_Objects:
                    ind = Position_Tracing_Objects.index(hit_shape)
                    del trace_points_list[ind]
                    del trace_point_colors[ind]
                    Position_Tracing_Objects.remove(hit_shape)

                # Check if it's a static segment
                if isinstance(hit_shape, pymunk.Segment):
                    if hit_shape in space.shapes:
                        space.remove(hit_shape)
                    if hit_shape in Objects:
                        Objects.remove(hit_shape)
                # If it's not a segment, handle dynamic objects (balls, liquids, gases)
                elif hit_shape in Objects or hit_shape in water_particles_shapes or hit_shape in gas_particles_shapes:
                    for constraint in space.constraints[:]:
                        if constraint.a == body or constraint.b == body:
                            space.remove(constraint)
                            Joints.remove(constraint)
                    if body in space.bodies:
                        space.remove(hit_shape, body)
                    if hit_shape in Objects:
                        Objects.remove(hit_shape)
                    if hit_shape in water_particles_shapes:
                        ind = water_particles_shapes.index(hit_shape)
                        water_particles_shapes.remove(hit_shape)
                        # Use the simpler way to remove by element!
                        Objects.remove(water_particles[ind])
                        water_particles.remove(water_particles[ind])
                    if hit_shape in gas_particles_shapes:
                        ind = gas_particles_shapes.index(hit_shape)
                        gas_particles_shapes.remove(hit_shape)
                        # Use the simpler way to remove by element!
                        Objects.remove(gas_particles[ind])
                        gas_particles.remove(gas_particles[ind])

        if state == 'DrawCube' and  event.button != 3:
            if Cube_Dynamic == False:
                cube = mouse.Add_Cube(space, (mouse.mouse_x, mouse.mouse_y), (Cube_Size, Cube_Size), elasticity=Cube_Elasticity, friction=0.5, color=(255, 255, 255, 100))
                Objects.append(cube)
            else:
                cube = mouse.Add_Cube_Dynamic(space, (mouse.mouse_x, mouse.mouse_y), (Cube_Size, Cube_Size), elasticity=Cube_Elasticity, friction=0.5, color=(255, 255, 255, 100), mass=Cube_Mass)
                Objects.append(cube)
        if state == 'DrawModeCube':
            cube = mouse.Add_Cube(space, (mouse.mouse_x, mouse.mouse_y), (Draw_Size, Draw_Size), elasticity=1, friction=0, color=(255, 255, 255, 100))
            Objects.append(cube)
        if state == 'DrawLiquid' and len(Objects) < 1001 and event.button != 3:
            liquid = mouse.Add_Liquid(space, (mouse.mouse_x, mouse.mouse_y), Liquid_Mass, Liquid_Radiuss, surface_tension=0.1, color=(255, 255, 255, 100))
            Objects += liquid
        if state == 'DrawGas' and len(Objects) < 1001 and event.button != 3:
            gas = mouse.Add_Gas(space, (mouse.mouse_x, mouse.mouse_y), Gas_Mass, Gas_Radiuss, temperature=Gas_Temp, color=(100, 255, 255, 100))
            Objects += gas
        if state == 'DrawRope' and event.button != 3:
            p = Vec2d(*event.pos)
            body2 = space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if body2 != None:
                body2 =body2.shape.body
            body1 = mouse.body1
            if body1 != None and body2 != None and body1 != body2:
                joint =  pymunk.PinJoint(body1, body2, (0, 0), (0, 0))
                Joints.append(joint)
                space.add(joint)

        if event.type == pygame.KEYDOWN and ActivatedButton != None:
            if event.key == pygame.K_BACKSPACE:
                ActivatedButton.user_text = ActivatedButton.user_text[:-1]
            if event.key == pygame.K_RETURN:
                if ActivatedButton == Button_Cube_Mass:
                    try:
                        val = abs(float(ActivatedButton.user_text))
                        if val != 0:
                            Cube_Mass = val
                            mouse.cube_mass= Cube_Mass
                    except ValueError:
                        pass
                if ActivatedButton == Button_Draw_Size:
                    try:
                        val = abs(float(ActivatedButton.user_text))
                        if val != 0:
                            Draw_Size = val
                            mouse.draw_size = Draw_Size
                    except ValueError:
                        pass

                if ActivatedButton == Button_Const1:
                    try:
                        Gravity_Y = float(ActivatedButton.user_text)
                    except ValueError:
                        pass
                    space.gravity = (Gravity_X, Gravity_Y)

                if ActivatedButton == Button_Const3:
                    try:
                        Gravity_X = float(ActivatedButton.user_text)
                    except ValueError:
                        pass
                    space.gravity = (Gravity_X, Gravity_Y)

                if ActivatedButton == Button_Ball_Radius:
                    try:
                        val = abs(float(ActivatedButton.user_text))
                        if val != 0:
                            Ball_Radius = val
                            mouse.ball_radius = Ball_Radius
                    except ValueError:
                        pass

                if ActivatedButton == Button_Ball_Mass:
                    try:
                        val = abs(float(ActivatedButton.user_text))
                        if val != 0:
                            Ball_Mass = val
                    except ValueError:
                        pass

                if ActivatedButton == Button_Cube_Size:
                    try:
                        val = abs(float(ActivatedButton.user_text))
                        if val != 0:
                            Cube_Size = val
                            mouse.cube_size = Cube_Size
                    except ValueError:
                        pass

                if ActivatedButton == Button_Ball_Elasticity:
                    try:
                        Ball_Elasticity = abs(float(ActivatedButton.user_text))
                    except ValueError:
                        pass


                if ActivatedButton == Button_Cube_Elasticity:
                    try:
                        Cube_Elasticity = abs(float(ActivatedButton.user_text))
                    except ValueError:
                        pass

                if ActivatedButton == Button_Gas_Mass:
                    try:
                        val = abs(float(ActivatedButton.user_text))
                        if val != 0:
                            Gas_Mass = val
                    except ValueError:
                        pass

                if ActivatedButton == Button_Temperature:
                    try:
                        Gas_Temp = abs(float(ActivatedButton.user_text))
                    except ValueError:
                        pass

                if ActivatedButton == Button_Gas_Size:
                    try:
                        val = abs(float(ActivatedButton.user_text))
                        if val != 0:
                            Gas_Radiuss = val
                            mouse.gas_radius = Gas_Radiuss
                    except ValueError:
                        pass

                ActivatedButton.activated = False
                ActivatedButton = None
            elif event.key != pygame.K_BACKSPACE and event.key != pygame.K_RETURN:
                ActivatedButton.user_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN and state != 'DrawRopeStart':
            if mouse_joint is not None:
                space.remove(mouse_joint)
                mouse_joint = None

            p = Vec2d(*event.pos)
            # Query for the nearest dynamic shape under the mouse pointer
            hit = space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if hit is not None and hit.shape.body.body_type == pymunk.Body.DYNAMIC:
                shape = hit.shape
                # Determine the closest point on the shape
                if hit.distance > 0:
                    nearest = hit.point
                else:
                    nearest = p
                # Create a PivotJoint between mouse_body and the shape’s body
                mouse_joint = pymunk.PivotJoint(
                    mouse_body,
                    shape.body,
                    (0, 0),
                    shape.body.world_to_local(nearest),
                    )
                desired_acceleration = 50000
                mouse_joint.max_force = shape.body.mass * desired_acceleration   # Limits the force to avoid jerky movements
                # mouse_joint.error_bias = (1 - 0.15) ** 60
                space.add(mouse_joint)

        elif event.type == pygame.MOUSEBUTTONUP:
                # Remove the mouse joint when the button is released
            if mouse_joint is not None:
                space.remove(mouse_joint)
                mouse_joint = None
            # pygame.display.flip()
            # clock.tick(FPS)
    for button in Buttons:
        if button.activated:
            button.draw(screen, button.user_text)
        else:
            button.draw(screen, button.text)
    pygame.display.flip()
    pygame.display.set_caption(f"fps: {clock.get_fps()}")
    clock.tick(FPS)
pygame.quit()