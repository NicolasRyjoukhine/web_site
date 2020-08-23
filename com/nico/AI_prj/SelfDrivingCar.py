import pygame as pg
import neat
import random
from pygame.locals import *
import os
import time

clock = pg.time.Clock()
FPS = 10

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
go_up = False

GREY = (192, 192, 192)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 0, 128)
RED = (200, 0, 0)
PURPLE = (102, 0, 102)


car_img = pg.image.load('D:\\nicoPrj\web_site\com\\nico\AI_prj\images\car_png-removebg-preview.png').convert_alpha()


class Car:
    def __init__(self, x, y, width, height, what_screen, what_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = what_screen
        self.color = what_color
        self.img = car_img
        self.resized = pg.transform.scale(self.screen, (self.x+self.width, self.y+self.height))

    def draw_car(self, add_y):
        try:
            screen.blit(self.img, (self.x, self.y + add_y))
        except Exception as e:
            print(e)
            pg.draw.rect(self.screen, self.color, [[self.x, self.y + add_y],
                                               [self.width, self.height]])


class Wall:
    def __init__(self, x, y, width, what_color, what_screen, how_wide_in_y, screen_width):
        self.x = x
        self.y = y
        self.color = what_color
        self.width = width
        self.ywidth = how_wide_in_y
        self.screen = what_screen
        self.screeny = screen_width

    def draw_wall(self):
        print(self.x, self.width, self.x + self.width)
        pg.draw.rect(self.screen, self.color, (self.x, 0, self.width, self.y))
        pg.draw.rect(self.screen, self.color, (self.x, self.y + self.ywidth, self.width, self.screeny))


def eval_genomes():
    pass


def configAI(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes(), 50)
    print('Winner for this gen: {}'.format(winner))


def main():
    pg.init()  # initializing the Simulation
    pg.display.set_caption("SelfDrivingCar")
    cars = []

    add_y = 0

    while len(cars)-1 != 0:
        car = Car(100, 100, 100, 100, screen, RED)
        car.draw_car(add_y)
        add_y += 1
        pg.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()



