
"""
The classic game of flappy bird. Make with python
and pygame. Features pixel perfect collision using masks :o
Date Modified:  Jul 30, 2019
Author: Tech With Tim
Estimated Work Time: 5 hours (1 just for that damn collision)
"""
import pygame
import random
import os
import time
import neat
import pickle

pygame.font.init()  # init font

WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.png")).convert_alpha(), (600, 900))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird" + str(x) + ".png"))) for x in
               range(1, 4)]
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")).convert_alpha())

gen = 0


def eval_genomes(genomes, config):
    global WIN, gen
    win = WIN
    gen += 1

    nets = []
    birds = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(genome)

    base = Base(FLOOR)
    pipes = [Pipe(700)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(birds) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[
                0].PIPE_TOP.get_width():  # determine whether to use the first or second
                pipe_ind = 1  # pipe on the screen for neural network input

        for x, bird in enumerate(birds):  # give each bird a fitness of 0.1 for each frame it stays alive
            ge[x].fitness += 0.1
            bird.move()

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[birds.index(bird)].activate(
                (bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[
                0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                bird.jump()

        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            for bird in birds:
                if pipe.collide(bird, win):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))



        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))


        # break if score gets large enough
        '''if score > 20:
            pickle.dump(nets[0],open("best.pickle", "wb"))
            break'''


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)

'''
import math

total_line_points = []


def get_angle(first_point, last_point, screen_width=800, screen_height=800):
    if first_point[0] < last_point[0] and first_point[1] < last_point[1]:
        opposite_of_circle = (screen_height - first_point[1]) - (screen_height - last_point[1])
        adjecent_of_circle = (screen_width - first_point[0]) - (screen_width - last_point[0])

    else:
        opposite_of_circle = (screen_height - last_point[1]) - (screen_height - first_point[1])
        adjecent_of_circle = (screen_width - last_point[0]) - (screen_width - first_point[0])

    if adjecent_of_circle <= 0:
        adjecent_of_circle = -1 * adjecent_of_circle
    if opposite_of_circle <= 0:
        opposite_of_circle = -1 * opposite_of_circle

    hypothenus_of_circle_squared = ((adjecent_of_circle ** 2) + (opposite_of_circle ** 2))

    if hypothenus_of_circle_squared <= 0:
        hypothenus_of_circle_squared *= -1

    hypothenus_of_circle = round(math.sqrt(hypothenus_of_circle_squared))

    print('Opposite is {}, \nAdjecent is {}\nHypothenus is {} and squared is {}'.format(opposite_of_circle,
                                                                                        adjecent_of_circle,
                                                                                        hypothenus_of_circle,
                                                                                        hypothenus_of_circle_squared))

    angle = (opposite_of_circle / hypothenus_of_circle)
    if angle <= 0:
        angle = angle * -1
    get_cos = math.asin(angle) * 180 / math.pi
    print(get_cos)
    return round(get_cos)


def return_ration_using_angle(angle):
    return_list = []
    get_y_up = angle * 10
    get_x_up = 10 * 100
    return_list.append(get_x_up/1000)
    return_list.append(get_y_up/1000)
    return return_list


def get_all_points_line(point1, point2):
    """
    This function saves all the points in a line
    using the ratio that can be using with the angle.
    It returns a list with all the values in it
    """
    add_values = []
    angle = get_angle(point1, point2)
    ratio = return_ration_using_angle(angle)
    if point1 < point2:
        biggest = point2
        smallest = point1
    else:
        biggest = point1
        smallest = point2
    add_values.append(point1[0] + ratio[0])  # } adding the X coords
    add_values.append(point1[1] + ratio[1])  # } adding the Y coords
    total_line_points.append(add_values)  # saving them to a list with all the points
    r_x = ratio[0]
    r_y = ratio[1]
    print(r_y, r_x)
    for i in range(biggest[0] - smallest[0] + 1):
        get_last_point_x = total_line_points[i][0]
        get_last_point_y = total_line_points[i][1]
        add_x = get_last_point_x + r_x
        add_y = get_last_point_y + r_y
        point = [add_x, add_y, angle]
        total_line_points.append(point)


p1 = [250, 250]
p2 = [255, 255]
total_line_points.append(p1)
print(total_line_points)
print(total_line_points, 'total line points', total_line_points[0][1])
get_all_points_line(p1, p2)


print(total_line_points)'''