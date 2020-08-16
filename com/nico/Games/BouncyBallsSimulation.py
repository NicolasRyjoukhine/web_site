import pygame as pg
import pygame.font
from pygame.locals import *
import random
import math
import time
import sys
import tkinter

clock = pg.time.Clock()
pg.font.init() # you have to call this at the start,


screenWidth = 800
screenHeight = 800
screen = pg.display.set_mode((screenWidth, screenHeight))
bgImg = pg.image.load("D:\\nicoPrj\web_site\com\\nico\Games\Images\\boncingBallsSimulationBG.png")
picture = pg.transform.scale(bgImg, (screenHeight + 400, screenWidth))
arrow1 = pg.image.load('D:\\nicoPrj\web_site\com\\nico\Games\Images\\arrow_default.png')
arrow2 = pg.image.load('D:\\nicoPrj\web_site\com\\nico\Games\Images\\arrow_green.png')
arrow3 = pg.image.load('D:\\nicoPrj\web_site\com\\nico\Games\Images\\arrow_orange.png')
arrow4 = pg.image.load('D:\\nicoPrj\web_site\com\\nico\Games\Images\\arrow_red.png')

picture_arrow1 = pg.transform.scale(arrow1, (100, 20))
picture_arrow2 = pg.transform.scale(arrow2, (100, 20))
picture_arrow3 = pg.transform.scale(arrow3, (100, 20))
picture_arrow4 = pg.transform.scale(arrow4, (100, 20))


myfont = pg.font.SysFont('maison Sans MS', 30)


i = 20
totalLines = []

SHADOW = (192, 192, 192)
WHITE = (255, 255, 255)
LIGHTGREEN = (0, 255, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 128)
LIGHTBLUE = (0, 0, 255)
RED = (200, 0, 0)
LIGHTRED = (255, 100, 100)
PURPLE = (102, 0, 102)
LIGHTPURPLE = (153, 0, 153)


def current_mouse_position():
    mouse_position = pg.mouse.get_pos()
    return mouse_position


def get_numb(min_value, max_value):
    return random.randint(min_value, max_value)


def drawline(f_posx, f_posy, s_posx, s_posy, what_color):
    pg.draw.line(screen, what_color, [f_posx, f_posy], [s_posx, s_posy])


def get_angle(first_point, last_point, screen_width=800, screen_height=800):
    opposite_of_circle = (screen_height - first_point[1]) - (screen_height - last_point[1])
    adjecent_of_circle = (screen_width - first_point[0]) - (screen_width - last_point[0])

    if adjecent_of_circle <= 0:
        adjecent_of_circle = -1 * adjecent_of_circle
    if opposite_of_circle <= 0:
        opposite_of_circle = -1 * opposite_of_circle

    hypothenus_of_circle_squared = ((adjecent_of_circle**2) + (opposite_of_circle**2))

    if hypothenus_of_circle_squared <= 0:
        hypothenus_of_circle_squared *= -1

    hypothenus_of_circle = round(math.sqrt(hypothenus_of_circle_squared))

    print('Opposite is {}, \nAdjecent is {}\nHypothenus is {} and squared is {}'.format(opposite_of_circle,
                                                                      adjecent_of_circle,
                                                                      hypothenus_of_circle,
                                                                      hypothenus_of_circle_squared))

    angle = (opposite_of_circle / hypothenus_of_circle)
    print(angle)

    if angle <= 0:
        angle = angle * -1
        print(angle)
    get_cos = math.asin(angle) * 180/math.pi
    print(get_cos)
    return round(get_cos - 180)


def check_is_odd(number):
  if (number % 2) == 0:
    return True
  else:
    return False


def get_all_points():
    for line in totalLines:
        # first_coordinatex = line[0[0]]
        # first_coordinatey = line[0[1]]
        # second_coodinatex = line[1[0]]
        # second_coodinatey = line[1[1]]
        get_ratio = 1
        print(get_ratio)
        return None


def gravity_acting(y, trampoline_x, trampoline_y):
    if y < 0:
        new_y = y - (y/10*9.8)  # I want to remove 0.98 but i can t because i can t remove .98 pixel for but only one
        return new_y
    else:
        if 350 < trampoline_x < 450 and y < trampoline_y-y+5 and y > trampoline_y+y+5:
            new_y = 1
            return new_y
        else:
            new_y = y + 1  # I want to add 0.98 but i can t because i can t add .98 pixel
            return new_y


def draw_button(x, y, radius, mousepos):
    circle = CreateCircle(screen, radius+20, [x, y], SHADOW, False)
    circle.drawcircle()
    circle2 = CreateCircle(screen, radius, [x, y], RED, False)
    circle2.drawcircle()


class Cube(pg.sprite.Sprite):
    pass


class Trampoline:
    def __init__(self, game_screen, left_corner_up, right_corner_down, strenght, chosen_color):
        self.screen = game_screen
        self.positionx = left_corner_up
        self.positiony = right_corner_down
        self.strenght = strenght
        self.color = chosen_color

    def draw_trampoline_top(self):
        """
        This Function Uses the PyGame Module
         to create A transparent Trampoline.
        """
        try:
            tramp = pg.image.load(
                'D:\\nicoPrj\web_site\com\\nico\Games\Images\\trampoline_top-removebg-preview.png'
                ).convert_alpha()
            self.screen.blit(tramp, [self.positionx[0]+16, self.positionx[1]-20])
        except Exception as e:
            print(e)
            drawline(self.positionx[0], self.positionx[1], self.positiony[0], self.positionx[1], BLUE)
            drawline(self.positionx[0], self.positionx[1], self.positionx[0], self.positiony[1], BLUE)
            drawline(self.positiony[0], self.positiony[1], self.positiony[0], self.positionx[1], BLUE)

    def draw_trampoline_bottom(self):
        """
        This Function Uses the PyGame Module
         to create the non-transparent to of a Trampoline .
        """
        try:
            tramp = pg.image.load(
                'D:\\nicoPrj\web_site\com\\nico\Games\Images\\trampoline_bottom-removebg-preview.png'
                ).convert_alpha()
            self.screen.blit(tramp, [self.positionx[0], self.positionx[1]])
        except Exception as e:
            print(e)
            drawline(self.positionx[0], self.positionx[1], self.positiony[0], self.positionx[1], BLUE)
            drawline(self.positionx[0], self.positionx[1], self.positionx[0], self.positiony[1], BLUE)
            drawline(self.positiony[0], self.positiony[1], self.positiony[0], self.positionx[1], BLUE)


class CreateCircle:
    def __init__(self, game_screen, circle_radius, position, chosen_color, is_random):
        self.is_random = is_random
        self.screen = game_screen
        self.circleradius = circle_radius
        self.position = position
        self.color = chosen_color

    def drawcircle(self):
        """This Function Uses the PyGame Module to create Circle.
                It has a random function build in"""
        if self.is_random:
            pg.draw.circle(
                self.screen, self.color, self.position, get_numb(5, 50)
            )
        else:
            pg.draw.circle(
                self.screen, self.color, self.position, self.circleradius
            )


class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def main():
    """The script allows the user to create one or more circles
        and to see them react in an environment with real-life
        physics using the PyGame interface"""

    is_simulation_running = True
    is_circle_appeared = False
    is_need_for_update = True
    anti_gravity = False
    reset = False







    teSTCOOORSDS_DEL_ME = [0, 120, 160, 200, 240, 300, 240, 260]









    circle_radius = 20
    circle_save_coordinates = [250, 250]
    button_coords = [700, 700]

    all_arrows = [picture_arrow1, picture_arrow2, picture_arrow3, picture_arrow4]
    current_arrow = picture_arrow1

    a = 0
    add_x = 0
    add_y = 0

    arrow_val_temp = 0

    pg.init()  # initializing the Simulation
    pg.display.set_caption("Bouncy Balls Simulation")

    while is_simulation_running:
        screen.fill(SHADOW)
        screen.blit(picture, [0 - 400, 0])
        # deletes all circles to replace with new affected by physics

        for event in pg.event.get():
            keys = pg.key.get_pressed()
            if event.type == pg.MOUSEBUTTONDOWN:
                new_coords_circle_x = current_mouse_position()[0]
                new_coords_circle_y = current_mouse_position()[1]
                circle_save_coordinates.clear()
                circle_save_coordinates.append(new_coords_circle_x)
                circle_save_coordinates.append(new_coords_circle_y)
                is_circle_appeared = True
                reset = True
                add_y = 0
                add_x = 0

            if keys[K_SPACE]:
                if arrow_val_temp == 2:
                    arrow_val_temp = 0
                time.sleep(1)
                current_arrow = all_arrows[arrow_val_temp]
                arrow_val_temp += 1

            if event.type == pg.QUIT:
                pg.quit()

        # create new trampoline at these positions and use physics let things jump on it..
        trampoline = Trampoline(screen, [350, 750], [450, 800], 10, BLUE)

        # create new circle at these positions and use physics to move it.
        circle = CreateCircle(screen, circle_radius,
                              [circle_save_coordinates[0], circle_save_coordinates[1]],
                              RED, False)

        try:
            trampoline.draw_trampoline_top()
            draw_button(button_coords[0], button_coords[1], 20, current_mouse_position())
            angle_of_arrow = get_angle(button_coords, current_mouse_position())
            arrow_img_draw = pg.transform.rotate(current_arrow, teSTCOOORSDS_DEL_ME[a])
            screen.blit(arrow_img_draw, [button_coords[0]-int(round(arrow_img_draw.get_width()/2)),
                                         button_coords[1]-int(round(arrow_img_draw.get_height()/2))])
        except Exception as e:
            print(e)

        a += 1
        if a == len(teSTCOOORSDS_DEL_ME)-1:
            a = 0
        if add_y == 0 and is_need_for_update:
            add_y = 2

        if is_circle_appeared:
            if anti_gravity:
                if reset:
                    add_y = -1 * (int(float(gravity_acting(add_y,
                                                           circle_save_coordinates[0],
                                                           circle_save_coordinates[1]))))
                    anti_gravity = False
                    reset = False
            else:
                add_y = 1 * (int(float(gravity_acting(add_y,
                                                      circle_save_coordinates[0],
                                                      circle_save_coordinates[1]))))
            circle_save_coordinates[0] += add_x
            circle_save_coordinates[1] += add_y
            circle.drawcircle()
        trampoline.draw_trampoline_bottom()

        if circle_save_coordinates[0] + circle_radius >= screenWidth:
            print("The Circle has Touched the {} line".format('right'))
            add_x = -2
            is_need_for_update = False

        if circle_save_coordinates[0] - circle_radius <= screenWidth - screenWidth:
            print("The Circle has Touched the {} line".format('left'))
            add_x = 2
            is_need_for_update = False

        if circle_save_coordinates[1] + circle_radius >= screenWidth:
            print("The Circle has Touched the {} line".format('bottom'))
            add_y = -2
            is_need_for_update = False

        if circle_save_coordinates[1] - circle_radius <= screenWidth - screenWidth:
            print("The Circle has Touched the {} line".format('top'))
            add_y = 2
            is_need_for_update = False

        if 350 < circle_save_coordinates[0] < 450:
            if circle_save_coordinates[1] >= 750-circle_radius or circle_save_coordinates[1] >= 750 + circle_radius:
                if circle_save_coordinates[1] < 774:
                    print("The Circle has Touched the trampoline line")
                    add_y = -2
                    is_need_for_update = False
                    anti_gravity = True

        if add_y == 0 and is_need_for_update:
            add_y = 2

        if is_circle_appeared:
            circle_save_coordinates[0] += add_x
            circle_save_coordinates[1] += add_y

        pg.display.update()
        clock.tick(1)


if __name__ == "__main__":
    main()
