import pygame
import pymunk
import pymunk.pygame_util
import pyautogui
from Mouse import Mouse

WIDTH = pyautogui.size()[0] * 0.95
HEIGHT = pyautogui.size()[1] * 0.95
pygame.init()
FPS = 60
# WIDTH, HEIGHT = 1600, 1000
# GRAVITY = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics-simulator")
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 1000)
running = True
draw_options = pymunk.pygame_util.DrawOptions(screen)
MouseState = None

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

    def draw(self, screen):
        if self.is_seen:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, self.hover_color, self.rect)
            else:
                pygame.draw.rect(screen, self.button_color, self.rect)

            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if self.is_seen and event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
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


Button_CleanAll = Button(False, 40, HEIGHT*0.88 - 120, 200, 80, 'Clean All', 40)
Button_Const1 = Button(False, 40, 30, 200, 80, 'Gravity', 40)
Button_Const2 = Button(False, 40, 150, 200, 80, 'Const2', 40)
Button_Object1 = Button(False, 40, 30, 200, 80, 'Add Ball', 40)
Button_Object2 = Button(False, 40, 150, 200, 80, 'Add Cube', 40)
Button_Map1 = Button(False, 40, 30, 200, 80, 'Map1', 40)
Button_Map2 = Button(False, 40, 150, 200, 80, 'Map2', 40)
Button_Maps = Button(True, 40, 150, 200, 80, 'Maps', 40)
Button_Tools = Button(True, 40, 30, 200, 80, 'Tools', 40)
Button_WorldSettings = Button(False, 40, 30, 200, 80, 'World Settings', 30)
Button_AddObject = Button(False, 40, 150, 200, 80, 'Add Object', 30)
Button_GoBack = Button(False, 40, HEIGHT*0.88, 200, 80, 'Go Back', 40)

Button_Tools.childrens = [Button_WorldSettings, Button_AddObject, Button_GoBack, Button_CleanAll]
Button_Tools.layer = [Button_Tools, Button_Maps]

Button_Maps.layer = [Button_Tools, Button_Maps]
Button_Maps.childrens = [Button_Map1, Button_Map2, Button_GoBack]

Button_AddObject.layer = [Button_CleanAll, Button_AddObject, Button_WorldSettings, Button_GoBack]
Button_AddObject.childrens = [Button_CleanAll, Button_Object1, Button_Object2, Button_GoBack]

Button_WorldSettings.layer = [Button_CleanAll, Button_WorldSettings, Button_AddObject, Button_GoBack]
Button_WorldSettings.childrens = [Button_CleanAll, Button_Const1, Button_Const2, Button_GoBack]


Button_Const1.parent = Button_WorldSettings
Button_Const2.parent = Button_WorldSettings
Button_Object2.parent = Button_AddObject
Button_Object1.parent = Button_AddObject
Button_WorldSettings.parent = Button_Tools
Button_AddObject.parent = Button_Tools
Button_Map2.parent = Button_Maps


create_wall(space, 40, 2000, (300, 500), (255, 255, 255), 1, 0)

Objects = []
Buttons = [Button_Tools, Button_GoBack, Button_AddObject, Button_WorldSettings, Button_Maps, Button_Map1, Button_Map2, Button_Object1, Button_Object2, Button_Const2, Button_Const1, Button_CleanAll]
mouse = Mouse(None)
Top_Layer = Button_Tools.layer
while running:
    screen.fill((0, 0, 0))
    space.step(1 / FPS)
    space.debug_draw(draw_options)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if Button_Object1.is_clicked(event) and Button_Object1.is_seen:
            mouse.state = 'ReadyToAddBall'

        if Button_Object2.is_clicked(event) and Button_Object2.is_seen:
            mouse.state = 'ReadyToAddCube'

        if Button_CleanAll.is_clicked(event) and Button_CleanAll.is_seen:
            to_remove = []
            for obj in Objects:
                to_remove.append(obj)
            for obj in to_remove:
                space.remove(obj.body, obj)
                Objects.remove(obj)

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
            for button in Button_GoBack.layer:
                button.is_seen = False
            for button in Button_GoBack.childrens:
                button.is_seen = True
            Button_GoBack.layer = Button_GoBack.childrens
            if Button_GoBack.parent.parent:
                Button_GoBack.childrens = Button_GoBack.parent.parent.layer

        state = mouse.getstate(event, screen)
        if state == 'DrawBall':
            ball = mouse.Add_Ball(space, (mouse.mouse_x, mouse.mouse_y), 30, mass=1, elasticity=0.5, friction=0.5, color=(255, 255, 255, 100))
            Objects.append(ball)
        if state == 'DrawCube':
            cube = mouse.Add_Cube(space, (mouse.mouse_x, mouse.mouse_y), (50, 50), elasticity=0.5, friction=0.5, color=(255, 255, 255, 100))
            Objects.append(cube)

        for obj in Objects:
            if obj.body.position[0] < 300:
                space.remove(obj.body, obj)
                Objects.remove(obj)


    for button in Buttons:
        button.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()