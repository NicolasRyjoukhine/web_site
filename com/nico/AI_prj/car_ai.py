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


class Car:
    def __init__(self, x, y, width, height, what_screen, what_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = what_screen
        self.color = what_color

    def draw_car(self):
        pg.draw.rect(self.screen, self.color, [[self.x, self.y],
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


def eval_genomes(cars_list, walls, x, reduce_x, y, y_width, genomes_list, is_pipe_behind):
    rem = []
    cars = []
    nn_s = []

    for i in genomes_list:
        i.fitness = 0
        nn = neat.nn.FeedForwardNetwork(i, config_path)
        nn_s.append(Car)
        cars.append(Car(10, overide_y, 10, 10, screen, RED))

    for wall in walls:
        for car in cars_list:
            print(wall, cars_list, nn_s, genomes_list)
            car.draw_car()
            time.sleep(2)
            if x - reduce_x >= car.x >= reduce_x or y >= car.y >= y + y_width:
                print(genomes_list[cars.index(car)].fitness)

                genomes_list[cars.index(car)].fitness -= 1
                nn_s.pop(cars.index(car))
                genomes_list.pop(cars.index(car))
                cars.pop(cars.index(car))
            if car.x > reduce_x:
                genomes_list[cars.index(car)].fitness += 3

    for x, car in enumerate(cars):
        genomes_list[x].fitness += 0.1
        output = nn_s[
            cars.index(car)].activate((car.y, abs(car.y - walls.y), abs(car.y - walls.y)))

        if output[0] > 0.5:
            go_up = True

        if output[0] < 0.5:
            go_up = False


def configAI(config_path, cars, walls, defaul_wall_x, reducing_x, overide_y, ywidth, genomes, is_pip_behind):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes(cars, walls, defaul_wall_x, reducing_x, overide_y, ywidth, genomes, is_pip_behind), 50)
    print(winner)


def main():
    pg.init()  # initializing the Simulation
    pg.display.set_caption("Bouncy Balls Simulation")
    global cars, walls, defaul_wall_x, reducing_x, overide_y, ywidth, genomes, is_pip_behind


    are_all_dead = False
    need_for_wall = False
    is_pip_behind = False


    cars = []
    walls = []
    genomes = []
    pop = 50
    overide_x = 0
    overide_y = 100
    ywidth = 100
    new_y_wall = random.randint(0, 400)

    defaul_wall_x = SCREEN_WIDTH
    reducing_x = 0

    while not are_all_dead:
        print('Generation still alive')
        print('SPEED of loop: {}'.format(FPS))
        screen.fill(GREY)
        wall = Wall(defaul_wall_x - reducing_x, new_y_wall, 10, RED, screen, ywidth, SCREEN_HEIGHT)

        eval_genomes(cars, walls, defaul_wall_x, reducing_x, overide_y, ywidth, genomes, is_pip_behind)

        keys = pg.key.get_pressed()
        if keys[K_DOWN]:
            overide_y += 10
        if keys[K_UP]:
            overide_y -= 10

        if reducing_x == SCREEN_WIDTH:
            reducing_x = 0
            need_for_wall = True

        if go_up:
            overide_y -= 3

        if need_for_wall:
            new_y_wall = random.randint(0, 400)
            need_for_wall = False
            is_pip_behind = True
            walls.clear()
            walls.append(wall)

        wall.draw_wall()

        reducing_x += 10

        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    config_path = 'D:\\nicoPrj\web_site\com\\nico\AI_prj\\neat-requirements-text\configaicar'
    configAI(config_path, cars, walls, defaul_wall_x, reducing_x, overide_y, ywidth, genomes, is_pip_behind)
    main()



