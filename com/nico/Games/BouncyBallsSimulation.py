import pygame as pg
from pygame.locals import *
import random
import math
from pathlib import Path
import tkinter


clock = pg.time.Clock()

screenHeight = 800
screenWidth = 800
screen = pg.display.set_mode((screenHeight, screenWidth))
bgImg = pg.image.load("boncingBallsSimulationBG.png")
picture = pg.transform.scale(bgImg, (screenWidth, screenHeight))
img = pg.image.load('arrow_ball_sim.png')
img.set_colorkey((0, 0, 0))

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


def draw_button_line(point_1_x, point_1_y, mouse_pos):
    drawline(point_1_x, point_1_y, mouse_pos[0], mouse_pos[1], SHADOW)


def get_angle(first_point, last_point):
    opposite_of_circle = first_point[1] - last_point[1]
    adjecent_of_circle = last_point[0] - first_point[0]
    hypothenus_of_circle = (adjecent_of_circle ^ 2) + (opposite_of_circle ^ 2)
    get_cos_angle = -45
    if opposite_of_circle != 0 and hypothenus_of_circle != 0:
        get_cos = math.sin(opposite_of_circle/hypothenus_of_circle)
        get_cos_angle = get_cos * 180 / 3.141592653589793238462643383279502884197169399375105820974944592307816406286
    print(get_cos_angle)
    print(opposite_of_circle, adjecent_of_circle, hypothenus_of_circle)


def check_is_odd(number):
  if (number % 2) == 0:
    return True
  else:
    return False


def get_all_points():
    for line in totalLines:
        first_coordinatex = line[0[0]]
        first_coordinatey = line[0[1]]
        second_coodinatex = line[1[0]]
        second_coodinatey = line[1[1]]
        get_ratio = 1
        print(get_ratio)
        return first_coordinatex


def gravity_acting(y, trampoline_x, trampoline_y):
    if y < 0:
        new_y = y - (y/10*9)
        return new_y
    else:
        if 350 < trampoline_x < 450 and y < trampoline_y-y+5 and y > trampoline_y+y+5:
            new_y = 1
            return new_y
        else:
            new_y = y+1
            return new_y


def draw_button(x, y, radius, mousepos):
    circle = CreateCircle(screen, radius+20, [x, y], BLUE, False)
    circle.drawcircle()
    circle2 = CreateCircle(screen, radius, [x, y], RED, False)
    circle2.drawcircle()
    draw_button_line(x, y, mousepos)


class Trampoline:
    def __init__(self, game_screen, left_corner_up, right_corner_down, strenght, chosen_color, ):
        self.screen = game_screen
        self.positionx = left_corner_up
        self.positiony = right_corner_down
        self.strenght = strenght
        self.color = chosen_color

    def draw_trampoline(self):
        """
        This Function Uses the PyGame Module
         to create A Trampoline.
        """
        try:
            tramp = pg.image.load('trampoline.png').convert_alpha()
            self.screen.blit(tramp, [0, 1])
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
    circle_radius = 20
    circle_save_coordinates = [250, 250]
    button_coords = [700, 700]

    add_x = 0
    add_y = 0

    pg.init()  # initializing the Simulation
    pg.display.set_caption("Bouncy Balls Simulation")

    while is_simulation_running:
        print("The Simulation is running")
        screen.fill(SHADOW)
        screen.blit(picture, [0, 0])
        # deletes all circles to replace with new affected by physics

        for event in pg.event.get():
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
                print(circle_save_coordinates)

            if event.type == pg.QUIT:
                pg.quit()

        # create new trampoline at these positions and use physics let things jump on it..
        trampoline = Trampoline(screen, [350, 750], [450, 800], 10, BLUE)

        # create new circle at these positions and use physics to move it.
        circle = CreateCircle(screen, circle_radius,
                              [circle_save_coordinates[0], circle_save_coordinates[1]],
                              RED, False)

        trampoline.draw_trampoline()
        draw_button(button_coords[0], button_coords[1], 20, current_mouse_position())
        screen.blit(img, (button_coords[0], button_coords[1]))
        get_angle(button_coords, current_mouse_position())

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
            print(add_x, add_y)
            circle.drawcircle()

        print("Updating Physics")
        print(add_x, add_y)
        if circle_save_coordinates[0] + circle_radius >= screenHeight:
            print("The Circle has Touched the {} line".format('right'))
            add_x = -2
            is_need_for_update = False

        if circle_save_coordinates[0] - circle_radius <= screenHeight - screenHeight:
            print("The Circle has Touched the {} line".format('left'))
            add_x = 2
            is_need_for_update = False

        if circle_save_coordinates[1] + circle_radius >= screenHeight:
            print("The Circle has Touched the {} line".format('bottom'))
            add_y = -2
            is_need_for_update = False

        if circle_save_coordinates[1] - circle_radius <= screenHeight - screenHeight:
            print("The Circle has Touched the {} line".format('top'))
            add_y = 2
            is_need_for_update = False

        if 350 < circle_save_coordinates[0] < 450:
            if circle_save_coordinates[1] >= 750:
                if circle_save_coordinates[1] < 760:
                    print("The Circle has Touched the trampoline line")
                    add_y = -2
                    is_need_for_update = False
                    anti_gravity = True

        if add_y == 0 and is_need_for_update:
            add_y = 2

        if is_circle_appeared:
            print(add_x, add_y)
            circle_save_coordinates[0] += add_x
            circle_save_coordinates[1] += add_y

        pg.display.update()
        clock.tick(144)


if __name__ == "__main__":
    main()
