import pygame
import pymunk
import pymunk.pygame_util
import pyautogui
from liquid_Class import *
import gas_Class
from Mouse import Mouse
from VectorClass import Vector
from Gravity import *
from map1 import CreateMap1
from map2 import CreateMap2
from pymunk.vec2d import Vec2d
import math
from settings import *


WIDTH = pyautogui.size()[0] * 0.95
HEIGHT = pyautogui.size()[1] * 0.95
pygame.init()
FPS = 60
# WIDTH, HEIGHT = 1600, 1000
# GRAVITY = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics-simulator")
pygame.mixer.init()
pygame.mixer.music.load(r'Music/Music1.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 1000)
running = True
draw_options = pymunk.pygame_util.DrawOptions(screen)
MouseState = None
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

Button_Add_Rope = Button(False, 40, 630, 200, 80, 'Add Joint', 40)
Button_Cube_Mass = Button(False, 40, 270, 200, 80, 'Mass', 40)
Button_Cube_Dynamic = Button(False, 40, 390, 200, 80, 'Dynamic', 40)
Button_Gas_Size = Button_with_Image(False, 40, 270, 200, 80, 'Sprites/size.png', hover_image_path='Sprites/hovers/size2.png', image_path2='Sprites/hovers/da.png')
Button_Temperature = Button(False, 40, 150, 200, 80, 'Temperature', 40)
Button_Gas_Mass = Button(False, 40, 30, 200, 80, 'Mass', 40)
Button_Add_Gas = Button(False, 40, 510, 200, 80, 'Add Gas', 40)
Button_Add_Liquid = Button(False, 40, 390, 200, 80, 'Add Liquid', 40)
Button_Settings = Button_with_Image(True, WIDTH - 90, 15, 80, 80,  'Sprites/settings.png')
Button_Pause = Button_with_Image(True, 340, 15, 80, 80,  'Sprites/pause1.png', 'Sprites/pause2.png', special_need=True)
Button_Draw_Size = Button_with_Image(False, 40, 30, 200, 80, 'Sprites/size.png',  hover_image_path='Sprites/hovers/size2.png', image_path2='Sprites/hovers/da.png')
Button_Forces = Button(False, 40, 270, 200, 80, 'Forces', 40)
Button_Gravity_Between_Objects = Button_with_Image(False, 40, 30, 200, 80, 'Sprites/allow_gravity.png',  hover_image_path='Sprites/hovers/allow_gravity2.png', image_path2='Sprites/hovers/allow_gravity2.png', special_need=True)
Button_Cube_Elasticity = Button_with_Image(False, 40, 150, 200, 80, 'Sprites/elasticity.png', hover_image_path='Sprites/hovers/elasticity2.png', image_path2='Sprites/hovers/da.png')
Button_Ball_Elasticity = Button_with_Image(False, 40, 270, 200, 80, 'Sprites/elasticity.png', hover_image_path='Sprites/hovers/elasticity2.png', image_path2='Sprites/hovers/da.png')
Button_Cube_Size = Button_with_Image(False, 40, 30, 200, 80, 'Sprites/size.png',  hover_image_path='Sprites/hovers/size2.png', image_path2='Sprites/hovers/da.png')
Button_Ball_Mass = Button(False, 40, 150, 200, 80, 'Mass', 40)
Button_Ball_Radius = Button_with_Image(False, 40, 30, 200, 80, 'Sprites/radius.png', hover_image_path='Sprites/hovers/radius2.png', text_color='white', image_path2='Sprites/hovers/da.png')
Button_Draw = Button(False, 40, 270, 200, 80, 'Draw', 40)
Button_CleanAll = Button_with_Image(False, 40, HEIGHT*0.88 - 120, 200, 80, 'Sprites/clean_all.png', hover_image_path='Sprites/hovers/clean_all2.png', image_path2='Sprites/hovers/da.png')
Button_Const1 = Button_with_Image(False, 40, 30, 200, 80, 'Sprites/gravity_y.png',  hover_image_path='Sprites/hovers/gravity_y2.png', image_path2='Sprites/hovers/da.png')
Button_Const3 = Button_with_Image(False, 40, 150, 200, 80, 'Sprites/gravity_x.png',  hover_image_path='Sprites/hovers/gravity_x2.png', image_path2='Sprites/hovers/da.png')
Button_Const2 = Button_with_Image(False, 40, 270, 200, 80, 'Sprites/add_walls.png',  hover_image_path='Sprites/hovers/add_walls2.png', image_path2='Sprites/hovers/da.png')
Button_Object1 = Button(False, 40, 30, 200, 80, 'Add Ball', 40)
Button_Object2 = Button(False, 40, 150, 200, 80, 'Add Cube', 40)
Button_Map1 = Button(False, 40, 30, 200, 80, 'Galton board', 40)
Button_Map2 = Button(False, 40, 150, 200, 80, "Newton's cradle", 30)
Button_Maps = Button_with_Image(True, 40, 150, 200, 80, 'Sprites/maps.png',  hover_image_path='Sprites/hovers/maps2.png', image_path2='Sprites/hovers/da.png')
Button_Tools = Button_with_Image(True, 40, 30, 200, 80, 'Sprites/tools.png',  hover_image_path='Sprites/hovers/tools2.png', image_path2='Sprites/hovers/da.png')
Button_WorldSettings = Button(False, 40, 30, 200, 80, 'World Settings', 30)
Button_AddObject = Button(False, 40, 150, 200, 80, 'Add Object', 30)
Button_GoBack = Button_with_Image(False, 40, HEIGHT*0.88, 200, 80, 'Sprites/go_back.png', hover_image_path='Sprites/hovers/go_back2.png', image_path2='Sprites/hovers/da.png')
Button_Show_Tempreature = Button(False, 40, 390, 200, 80, 'Show Temperature', 28)

Button_Show_Tempreature.layer = [Button_CleanAll, Button_Const1, Button_Const2, Button_Const3, Button_GoBack, Button_Show_Tempreature]
Button_Show_Tempreature.childrens = []

Button_Gas_Size.layer = [Button_CleanAll, Button_GoBack, Button_Gas_Mass, Button_Temperature, Button_Gas_Size]
Button_Gas_Size.childrens = []

Button_Temperature.layer = [Button_CleanAll, Button_GoBack, Button_Gas_Mass, Button_Temperature, Button_Gas_Size]
Button_Temperature.childrens = []

Button_Gas_Mass.layer = [Button_CleanAll, Button_GoBack, Button_Gas_Mass, Button_Temperature, Button_Gas_Size]
Button_Gas_Mass.childrens = []

Button_Tools.childrens = [Button_WorldSettings, Button_Forces, Button_AddObject, Button_GoBack, Button_CleanAll]
Button_Tools.layer = [Button_Tools, Button_Maps]

Button_Maps.layer = [Button_Tools, Button_Maps]
Button_Maps.childrens = [Button_Map1, Button_Map2, Button_GoBack, Button_CleanAll]

Button_AddObject.layer = [Button_Forces, Button_CleanAll, Button_AddObject, Button_WorldSettings, Button_GoBack]
Button_AddObject.childrens = [Button_Add_Rope, Button_Add_Gas, Button_Add_Liquid, Button_Draw, Button_CleanAll, Button_Object1, Button_Object2, Button_GoBack]

Button_WorldSettings.layer = [Button_Forces, Button_CleanAll, Button_WorldSettings, Button_AddObject, Button_GoBack]
Button_WorldSettings.childrens = [Button_CleanAll, Button_Const1, Button_Const2, Button_Const3, Button_GoBack, Button_Show_Tempreature]

Button_Object1.layer = [Button_Add_Rope, Button_Add_Gas, Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll]
Button_Object1.childrens = [Button_Ball_Elasticity, Button_Ball_Radius, Button_Ball_Mass, Button_GoBack, Button_CleanAll]

Button_Object2.layer = [Button_Add_Rope, Button_Add_Gas, Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll]
Button_Object2.childrens = [Button_Cube_Mass, Button_Cube_Dynamic, Button_Cube_Elasticity, Button_Cube_Size, Button_GoBack, Button_CleanAll]

Button_Add_Liquid.layer = [Button_Add_Rope, Button_Add_Gas, Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll]
Button_Add_Liquid.childrens = []

Button_Add_Gas.layer = [Button_Add_Rope, Button_Add_Gas, Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll]
Button_Add_Gas.childrens = [Button_Gas_Size, Button_Temperature, Button_Gas_Mass, Button_GoBack, Button_CleanAll]

Button_Draw.layer = [Button_Add_Rope, Button_Add_Gas, Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll]
Button_Draw.childrens = [Button_Draw_Size, Button_GoBack, Button_CleanAll]

Button_Add_Rope.layer = [Button_Add_Rope, Button_Add_Gas, Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll]

Button_Forces.childrens = [Button_GoBack, Button_CleanAll, Button_Gravity_Between_Objects]
Button_Forces.layer = [Button_Forces, Button_CleanAll, Button_AddObject, Button_WorldSettings, Button_GoBack]

Button_Const1.layer = [Button_CleanAll, Button_Const1, Button_Const2, Button_Const3, Button_GoBack, Button_Show_Tempreature]
Button_Const3.layer = [Button_CleanAll, Button_Const1, Button_Const2, Button_Const3, Button_GoBack, Button_Show_Tempreature]
Button_Gravity_Between_Objects.layer = [Button_CleanAll, Button_Const1, Button_Const2, Button_Const3, Button_GoBack, Button_Show_Tempreature]

Button_Ball_Radius.layer = [Button_CleanAll, Button_GoBack, Button_Ball_Mass, Button_Ball_Radius, Button_Ball_Elasticity]
Button_Ball_Mass.layer = [Button_CleanAll, Button_GoBack, Button_Ball_Mass, Button_Ball_Radius, Button_Ball_Elasticity]
Button_Cube_Size.layer = [Button_Cube_Mass, Button_Cube_Dynamic, Button_Cube_Elasticity, Button_Cube_Size, Button_GoBack, Button_CleanAll]
Button_Cube_Elasticity.layer = [Button_Cube_Mass, Button_Cube_Dynamic, Button_Cube_Elasticity, Button_Cube_Size, Button_GoBack, Button_CleanAll]
Button_Cube_Dynamic.layer = [Button_Cube_Mass, Button_Cube_Dynamic, Button_Cube_Elasticity, Button_Cube_Size, Button_GoBack, Button_CleanAll]
Button_Ball_Elasticity.layer = [Button_CleanAll, Button_GoBack, Button_Ball_Mass, Button_Ball_Radius, Button_Ball_Elasticity]
Button_Cube_Mass.layer = [Button_Cube_Mass, Button_Cube_Dynamic, Button_Cube_Elasticity, Button_Cube_Size, Button_GoBack, Button_CleanAll]


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
    "volume": 50
}


def save_callback(new_settings):
    global settings
    settings.update(new_settings)
    print("Updated settings:", new_settings)


create_wall(space, 40, 2000, (300, 500), (255, 255, 255), 1, 0)
Objects = []
Joints = []
Buttons = [Button_Add_Rope, Button_Cube_Mass, Button_Cube_Dynamic, Button_Show_Tempreature, Button_Gas_Size, Button_Temperature, Button_Gas_Mass, Button_Add_Gas, Button_Add_Liquid, Button_Pause, Button_Settings, Button_Draw_Size, Button_Forces, Button_Gravity_Between_Objects, Button_Cube_Elasticity, Button_Ball_Elasticity, Button_Cube_Size, Button_Ball_Radius, Button_Ball_Mass ,Button_Const3, Button_Draw, Button_Tools, Button_GoBack, Button_AddObject, Button_WorldSettings, Button_Maps, Button_Map1, Button_Map2, Button_Object1, Button_Object2, Button_Const2, Button_Const1, Button_CleanAll,]
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
while running:
    mouse_body.position = pygame.mouse.get_pos()
    screen.fill((0, 0, 0))
    space.debug_draw(draw_options)
    if paused == False:
        space.step(1 / FPS)
        water_particles = [obj for obj in Objects if isinstance(obj, Water_Particle)]
        gas_particles = [obj for obj in Objects if isinstance(obj, gas_Class.Gas_Particle)]
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
                grad = math.exp(-0.001 * obj.body.velocity.length)
                obj.particle.color = ((1 - grad) * 255, 0, grad * 255, 255)

        for obj in Objects:
            if obj.body in space.bodies:
                if obj.body.position[0] < 300:
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
            print(last_obj)
            if isinstance(last_obj, pymunk.Segment):
                space.remove(last_obj)
            if last_obj.body in space.bodies:
                if isinstance(last_obj, Water_Particle):
                    space.remove(last_obj.particle, last_obj.body)
                elif isinstance(last_obj, gas_Class.Gas_Particle):
                    space.remove(last_obj.particle, last_obj.body)
                else:
                    space.remove(last_obj, last_obj.body)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if Button_Settings.is_clicked(event) and Button_Settings.is_seen:
            open_settings_window(screen,settings, save_callback)

        if Button_Map1.is_clicked(event) and Button_Map1.is_seen:
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

        if Button_Map2.is_clicked(event) and Button_Map2.is_seen:
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

        if Button_Add_Gas.is_clicked(event) and Button_Add_Gas.is_seen and event.button != 3:
            mouse.state = 'ReadyToAddGas'

        if Button_Object1.is_clicked(event) and Button_Object1.is_seen and event.button != 3:
            mouse.state = 'ReadyToAddBall'

        if Button_Object2.is_clicked(event) and Button_Object2.is_seen:
            mouse.state = 'ReadyToAddCube'

        if Button_Draw.is_clicked(event) and Button_Draw.is_seen and event.button != 3:
            mouse.state = 'ReadyToAddDraw'

        if Button_Add_Liquid.is_clicked(event) and Button_Add_Liquid.is_seen and event.button != 3:
            mouse.state = 'ReadyToAddLiquid'

        if Button_Add_Rope.is_clicked(event) and Button_Add_Rope.is_seen and event.button != 3:
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
            wall1 = create_wall(space, 40, 2000, (1800, 500), (255, 255, 255), 1, 0)
            wall2 = create_wall(space, WIDTH, 40, (WIDTH / 2, 0), (255, 255, 255), 1, 0)
            wall3 = create_wall(space, WIDTH, 40, (WIDTH / 2, HEIGHT), (255, 255, 255), 1, 0)
            Objects.append(wall1)
            Objects.append(wall2)
            Objects.append(wall3)

        if Button_CleanAll.is_clicked(event) and Button_CleanAll.is_seen:
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

        if state == 'DrawBall' and  event.button != 3:
            ball = mouse.Add_Ball(space, (mouse.mouse_x, mouse.mouse_y), Ball_Radius, mass=Ball_Mass, elasticity=Ball_Elasticity, friction=0.5, color=(255, 255, 255, 100))
            Objects.append(ball)
        if state == 'DrawCube' and  event.button != 3:
            if Cube_Dynamic == False:
                cube = mouse.Add_Cube(space, (mouse.mouse_x, mouse.mouse_y), (Cube_Size, Cube_Size), elasticity=Cube_Elasticity, friction=0.5, color=(255, 255, 255, 100))
                Objects.append(cube)
            else:
                cube = mouse.Add_Cube_Dynamic(space, (mouse.mouse_x, mouse.mouse_y), (Cube_Size, Cube_Size), elasticity=Cube_Elasticity, friction=0.5, color=(255, 255, 255, 100), mass=Cube_Mass)
                Objects.append(cube)
        if state == 'DrawModeCube' and  event.button != 3:
            cube = mouse.Add_Cube(space, (mouse.mouse_x, mouse.mouse_y), (Draw_Size, Draw_Size), elasticity=1, friction=0, color=(255, 255, 255, 100))
            Objects.append(cube)
        if state == 'DrawLiquid' and len(Objects) < 1001 and  event.button != 3:
            liquid = mouse.Add_Liquid(space, (mouse.mouse_x, mouse.mouse_y), Liquid_Mass, Liquid_Radiuss, surface_tension=0.1, color=(255, 255, 255, 100))
            Objects += liquid
        if state == 'DrawGas' and len(Objects) < 1001 and event.button != 3:
            gas = mouse.Add_Gas(space, (mouse.mouse_x, mouse.mouse_y), Gas_Mass, Gas_Radiuss, temperature=Gas_Temp, color=(100, 255, 255, 100))
            Objects += gas


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

        if event.type == pygame.MOUSEBUTTONDOWN:
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