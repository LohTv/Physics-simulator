import pygame
import pymunk
import pymunk.pygame_util
import pyautogui
import liquid_Class
from Mouse import Mouse
from VectorClass import Vector
from Gravity import *
from map1 import CreateMap1


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
    def __init__(self, is_seen, x, y, width, height, image_path1='', image_path2='', text='', font='', text_color=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image_path2 = image_path2
        self.image_path1 = image_path1
        self.image_path = image_path1
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

        if image_path1:
            self.image1 = pygame.image.load(image_path1)
            self.image1 = pygame.transform.scale(self.image1, (width, height))  # Scale image to button size
            self.image = self.image1  # Set the initial image

        if image_path2:
            self.image2 = pygame.image.load(image_path2)
            self.image2 = pygame.transform.scale(self.image2, (width, height))  # Scale image to button size

    def draw(self, screen, text=''):
        if self.is_seen:
            screen.blit(self.image, (self.x, self.y))
        if text:  # If text is provided, render it
            text_surf = self.font.render(text, True, self.text_color)
            text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if self.is_seen and event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                if self.image_path2:
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


Button_Add_Liquid = Button(False, 40, 390, 200, 80, 'Add Liquid', 40)
Button_Settings = Button_with_Image(True, WIDTH - 90, 15, 80, 80,  r'Sprites/settings.png')
Button_Pause = Button_with_Image(True, 340, 15, 80, 80,  r'Sprites/pause1.png', 'Sprites/pause2.png')
Button_Draw_Size = Button(False, 40, 30, 200, 80, 'Size', 40)
Button_Forces = Button(False, 40, 270, 200, 80, 'Forces', 40)
Button_Gravity_Between_Objects = Button(False, 40, 390, 200, 80, 'Allow Gravity', 40)
Button_Cube_Elasticity = Button(False, 40, 150, 200, 80, 'Elasticity', 40)
Button_Ball_Elasticity = Button(False, 40, 270, 200, 80, 'Elasticity', 40)
Button_Cube_Size = Button(False, 40, 30, 200, 80, 'Size', 40)
Button_Ball_Mass = Button(False, 40, 150, 200, 80, 'Mass', 40)
Button_Ball_Radius = Button(False, 40, 30, 200, 80, 'Radius', 40)
Button_Draw = Button(False, 40, 270, 200, 80, 'Draw', 40)
Button_CleanAll = Button(False, 40, HEIGHT*0.88 - 120, 200, 80, 'Clean All', 40)
Button_Const1 = Button(False, 40, 30, 200, 80, 'Gravity - Y', 40)
Button_Const3 = Button(False, 40, 150, 200, 80, 'Gravity - X', 40)
Button_Const2 = Button(False, 40, 270, 200, 80, 'Add Walls', 40)
Button_Object1 = Button(False, 40, 30, 200, 80, 'Add Ball', 40)
Button_Object2 = Button(False, 40, 150, 200, 80, 'Add Cube', 40)
Button_Map1 = Button(False, 40, 30, 200, 80, 'Galton board', 40)
Button_Map2 = Button(False, 40, 150, 200, 80, 'Map2', 40)
Button_Maps = Button(True, 40, 150, 200, 80, 'Maps', 40)
Button_Tools = Button(True, 40, 30, 200, 80, 'Tools', 40)
Button_WorldSettings = Button(False, 40, 30, 200, 80, 'World Settings', 30)
Button_AddObject = Button(False, 40, 150, 200, 80, 'Add Object', 30)
Button_GoBack = Button(False, 40, HEIGHT*0.88, 200, 80, 'Go Back', 40)

Button_Tools.childrens = [Button_WorldSettings, Button_Forces, Button_AddObject, Button_GoBack, Button_CleanAll]
Button_Tools.layer = [Button_Tools, Button_Maps]

Button_Maps.layer = [Button_Tools, Button_Maps]
Button_Maps.childrens = [Button_Map1, Button_Map2, Button_GoBack, Button_CleanAll]

Button_AddObject.layer = [Button_Forces, Button_CleanAll, Button_AddObject, Button_WorldSettings, Button_GoBack]
Button_AddObject.childrens = [Button_Add_Liquid, Button_Draw, Button_CleanAll, Button_Object1, Button_Object2, Button_GoBack]

Button_WorldSettings.layer = [Button_Forces, Button_CleanAll, Button_WorldSettings, Button_AddObject, Button_GoBack]
Button_WorldSettings.childrens = [Button_Gravity_Between_Objects, Button_CleanAll, Button_Const1, Button_Const2, Button_Const3, Button_GoBack]

Button_Object1.layer = [Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll]
Button_Object1.childrens = [Button_Ball_Elasticity, Button_Ball_Radius, Button_Ball_Mass, Button_GoBack, Button_CleanAll]

Button_Object2.layer = [Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll]
Button_Object2.childrens = [Button_Cube_Elasticity, Button_Cube_Size, Button_GoBack, Button_CleanAll]

Button_Add_Liquid.layer = [Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll]
Button_Add_Liquid.childrens = []

Button_Draw.layer = [Button_Add_Liquid, Button_Object1, Button_Object2, Button_Draw, Button_GoBack, Button_CleanAll]
Button_Draw.childrens = [Button_Draw_Size, Button_GoBack, Button_CleanAll]

Button_Const1.layer = [Button_CleanAll, Button_Const1, Button_Const2, Button_Const3, Button_GoBack, Button_Gravity_Between_Objects]
Button_Const3.layer = [Button_CleanAll, Button_Const1, Button_Const2, Button_Const3, Button_GoBack, Button_Gravity_Between_Objects]
Button_Gravity_Between_Objects.layer = [Button_CleanAll, Button_Const1, Button_Const2, Button_Const3, Button_GoBack, Button_Gravity_Between_Objects]

Button_Ball_Radius.layer = [Button_CleanAll, Button_GoBack, Button_Ball_Mass, Button_Ball_Radius, Button_Ball_Elasticity]
Button_Ball_Mass.layer = [Button_CleanAll, Button_GoBack, Button_Ball_Mass, Button_Ball_Radius, Button_Ball_Elasticity]
Button_Cube_Size.layer = [Button_Cube_Size, Button_Cube_Elasticity, Button_CleanAll, Button_GoBack]
Button_Cube_Elasticity.layer = [Button_Cube_Size, Button_Cube_Elasticity, Button_CleanAll, Button_GoBack]
Button_Ball_Elasticity.layer = [Button_CleanAll, Button_GoBack, Button_Ball_Mass, Button_Ball_Radius, Button_Ball_Elasticity]

Button_Add_Liquid.parent = Button_AddObject
Button_Gravity_Between_Objects.parent = Button_WorldSettings
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
Buttons = [Button_Add_Liquid, Button_Pause, Button_Settings, Button_Draw_Size, Button_Forces, Button_Gravity_Between_Objects, Button_Cube_Elasticity, Button_Ball_Elasticity, Button_Cube_Size, Button_Ball_Radius, Button_Ball_Mass ,Button_Const3, Button_Draw, Button_Tools, Button_GoBack, Button_AddObject, Button_WorldSettings, Button_Maps, Button_Map1, Button_Map2, Button_Object1, Button_Object2, Button_Const2, Button_Const1, Button_CleanAll,]
Top_Layer = Button_Tools.layer
ActivatedButton = None
Gravity_Y = 1000
Gravity_X = 0
Ball_Radius = 30
Liquid_Radiuss = 30
Liquid_Mass = 1
Cube_Size = 50
Draw_Size = 20
Ball_Mass = 1
Ball_Elasticity = 1
Cube_Elasticity = 1
Allow_Gravity = False
G = 10000
mouse = Mouse(None, Ball_Radius, Cube_Size, Draw_Size, Liquid_Radiuss)
paused = False
while running:
    screen.fill((0, 0, 0))
    space.debug_draw(draw_options)
    if paused == False:
        space.step(1 / FPS)
        water_particles = [obj for obj in Objects if isinstance(obj, liquid_Class.Water_Particle)]
        circles = [obj for obj in Objects if isinstance(obj, pymunk.Circle)]

        for i, obj in enumerate(water_particles):
            for j in range(i + 1, len(water_particles)):
                liquid_Class.Apply_Tension(obj, water_particles[j])


        if Allow_Gravity:
            for obj in circles:
                for ob in Objects:
                    if ob != obj:
                        a = apply_gravity_acceleration(obj, ob, G)
                        obj.body.velocity += pymunk.Vec2d(a[0], a[1]) * (1 / FPS)

            for obj in water_particles:
                for ob in Objects:
                    if ob != obj:
                        a = apply_gravity_acceleration(obj, ob, G)
                        obj.body.velocity += pymunk.Vec2d(a[0], a[1]) * (1 / FPS)
                if obj.body in space.bodies:
                    if obj.body.position[0] < 300:
                        if isinstance(obj, pymunk.Segment):
                            pass
                        if isinstance(obj, liquid_Class.Water_Particle):
                            space.remove(obj.particle, obj.body)
                            Objects.remove(obj)
                        else:
                            space.remove(obj, obj.body)
                            Objects.remove(obj)
                if obj.body in space.bodies:
                    if obj.body.position[1] > 1000000:
                        if isinstance(obj, pymunk.Segment):
                            pass
                        if isinstance(obj, liquid_Class.Water_Particle):
                            space.remove(obj.particle, obj.body)
                            Objects.remove(obj)
                        else:
                            space.remove(obj, obj.body)
                            Objects.remove(obj)

        if len(Objects) > 1000:
            last_obj = Objects.pop()
            if isinstance(last_obj, pymunk.Segment):
                space.remove(last_obj)
            if isinstance(last_obj, liquid_Class.Water_Particle):
                space.remove(last_obj.particle, last_obj.body)
            else:
                space.remove(last_obj, last_obj.body)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if Button_Settings.is_clicked(event) and Button_Settings.is_seen:
            pass
            # print("Settings button clicked")
            # open_settings_thread(root, settings, save_callback)

        if Button_Map1.is_clicked(event) and Button_Map1.is_seen:
            for obj in Objects:
                if isinstance(obj, pymunk.Segment):
                    space.remove(obj)
                if obj.body in space.bodies:
                    if isinstance(obj, liquid_Class.Water_Particle):
                        space.remove(obj.particle, obj.body)
                    else:
                        space.remove(obj, obj.body)
            Objects = CreateMap1(space)

        if Button_Pause.is_clicked(event) and Button_Pause.is_seen:
            paused = not paused

        if Button_Object1.is_clicked(event) and Button_Object1.is_seen and event.button != 3:
            mouse.state = 'ReadyToAddBall'

        if Button_Object2.is_clicked(event) and Button_Object2.is_seen:
            mouse.state = 'ReadyToAddCube'

        if Button_Draw.is_clicked(event) and Button_Draw.is_seen and event.button != 3:
            mouse.state = 'ReadyToAddDraw'

        if Button_Add_Liquid.is_clicked(event) and Button_Add_Liquid.is_seen and event.button != 3:
            mouse.state = 'ReadyToAddLiquid'

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

        if Button_Const2.is_clicked(event) and Button_Const2.is_seen:
            wall1 = create_wall(space, 40, 2000, (1800, 500), (255, 255, 255), 1, 0)
            wall2 = create_wall(space, WIDTH, 40, (WIDTH / 2, 0), (255, 255, 255), 1, 0)
            wall3 = create_wall(space, WIDTH, 40, (WIDTH / 2, HEIGHT), (255, 255, 255), 1, 0)
            Objects.append(wall1)
            Objects.append(wall2)
            Objects.append(wall3)

        if Button_CleanAll.is_clicked(event) and Button_CleanAll.is_seen:
            for obj in Objects:
                if isinstance(obj, pymunk.Segment):
                    space.remove(obj)
                if obj.body in space.bodies:
                    if isinstance(obj, liquid_Class.Water_Particle):
                        space.remove(obj.particle, obj.body)
                    else:
                        space.remove(obj, obj.body)
            Objects.clear()

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

        if state == 'DrawBall':
            ball = mouse.Add_Ball(space, (mouse.mouse_x, mouse.mouse_y), Ball_Radius, mass=Ball_Mass, elasticity=Ball_Elasticity, friction=0.5, color=(255, 255, 255, 100))
            Objects.append(ball)
        if state == 'DrawCube':
            cube = mouse.Add_Cube(space, (mouse.mouse_x, mouse.mouse_y), (Cube_Size, Cube_Size), elasticity=Cube_Elasticity, friction=0.5, color=(255, 255, 255, 100))
            Objects.append(cube)
        if state == 'DrawModeCube':
            cube = mouse.Add_Cube(space, (mouse.mouse_x, mouse.mouse_y), (Draw_Size, Draw_Size), elasticity=1, friction=0.5, color=(255, 255, 255, 100))
            Objects.append(cube)
        if state == 'DrawLiquid':
            liquid = mouse.Add_Liquid(space, (mouse.mouse_x, mouse.mouse_y), Liquid_Mass, Liquid_Radiuss, surface_tension=25, color=(255, 255, 255, 100))
            Objects += liquid
        if event.type == pygame.KEYDOWN and ActivatedButton != None:
            if event.key == pygame.K_BACKSPACE:
                ActivatedButton.user_text = ActivatedButton.user_text[:-1]
            if event.key == pygame.K_RETURN:
                if ActivatedButton == Button_Draw_Size:
                    try:
                        Draw_Size = abs(float(ActivatedButton.user_text))
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
                        Ball_Radius = abs(float(ActivatedButton.user_text))
                        mouse.ball_radius = Ball_Radius
                    except ValueError:
                        pass

                if ActivatedButton == Button_Ball_Mass:
                    try:
                        Ball_Mass = abs(float(ActivatedButton.user_text))
                    except ValueError:
                        pass

                if ActivatedButton == Button_Cube_Size:
                    try:
                        Cube_Size= abs(float(ActivatedButton.user_text))
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

                ActivatedButton.activated = False
                ActivatedButton = None
            elif event.key != pygame.K_BACKSPACE and event.key != pygame.K_RETURN:
                ActivatedButton.user_text += event.unicode
            # pygame.display.flip()
            # clock.tick(FPS)
    for button in Buttons:
        if button.activated:
            button.draw(screen, button.user_text)
        else:
            button.draw(screen, button.text)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()