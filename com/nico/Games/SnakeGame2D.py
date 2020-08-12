import sys
import pygame
import pygame.font
import pygame as pg
from pygame.locals import *
import random
import time


BLACK = pg.Color('black')
WHITE = pg.Color('white')
RED = pg.Color('red')
clock = pg.time.Clock()
screen = pygame.display.set_mode((800, 800))
grid_rows = 145
square_size = 30
grid_colomns = 17
grid_COORDS = (0, 0)
gameover = pg.draw.rect(screen, RED, [350, - 400, 850, -400])
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3
newfruit = False
fruiteaten = False

#bg = pygame.image.load("downloads\grass_snake_bg.png")


## if objectHitGround():
##

class Snake(object):
    def __init__(self, x, y, initial_direction, init_color):
        self.body = [[x, y]]
        self.initial_direction = initial_direction
        self.color = init_color

    def move(self, move_value):
        last = self.body[len(self.body) - 1]
        first = self.body[0]
        if move_value == RIGHT:
            snake_new = [first[0] + 1, first[1]]
        if move_value == LEFT:
            snake_new = [first[0] - 1, first[1]]
        if move_value == UP:
            snake_new = [first[0], first[1] - 1]
        if move_value == DOWN:
            snake_new = [first[0], first[1] + 1]

        print(self.body)
        self.body.insert(0, snake_new)
        self.body.remove(last)
        return last

    def eat(self, fruit, last):
        global fruiteaten
        if fruit == self.body[0]:
            self.body.append(last)
            fruiteaten = True

    def hit_wall(self, x1, x2, y1, y2):
        if self.body[0][0] < x1 or self.body[0][0] > x2 or self.body[0][1] < y1 or self.body[0][1] > y2 :
            return True

    def hit_itself(self):
        pass
        for i in self.body:
            if len(self.body) == 1:
                return False
            if self.body[0] < i:
                return True


class Cell(object):
    def __init__(self, x, y, cell_color, grid_position):
        self.x = x
        self.y = y
        self.color = cell_color
        self.grid_position = grid_position


def draw_snake(snake, grid, screen_for_snake):
    for case in snake.body:
        for row in grid:
            for cell in row:
                if case[0] == cell.grid_position[0] and case[1] == cell.grid_position[1]:
                    print('snake')
                    rect = pg.rect.Rect(cell.y, cell.x, square_size, square_size)
                    pg.draw.rect(screen_for_snake, cell.color, rect)


def draw_fruitxy(grid, fruit, screen_for_fruit):
    global fruiteaten
    if fruiteaten:
        fruit = [random.randint(1, 10), random.randint(1, 10)]
        fruiteaten = False
    for row in grid:
         for cell in row:
            if fruit[0] == cell.grid_position[0] and fruit[1] == cell.grid_position[1]:
                rect = pg.rect.Rect(cell.y, cell.x, square_size, square_size)
                pg.draw.rect(screen_for_fruit, BLACK, rect)
            if fruiteaten == True:
                pg.draw.rect(screen_for_fruit, WHITE, rect)
                FBD = True


def draw_end(surface):
    pygame.draw.rect(surface, BLACK, [150, 100, 500, 100])


def main():
    move_value = RIGHT
    pygame.init()
    grid = []
    screen.fill(WHITE)
    pygame.display.set_caption("Snakes")
    fruit = [random.randint(1, 10), random.randint(1, 10)]
    snake= Snake(random.randint(2, 2),random.randint(2, 2), move_value, RED)

    for k in range(grid_rows):
        row = []
        for i in range(grid_colomns):
            cell = Cell(grid_COORDS[0] + i * square_size, grid_COORDS[1] + k * square_size, RED, (k, i))
            row.append(cell)
        grid.append(row)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    while True:

        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            move_value = RIGHT
        if keys[K_LEFT]:
            move_value = LEFT
        if keys[K_UP]:
            move_value = UP
        if keys[K_DOWN]:
            move_value = DOWN
        if keys[K_SPACE]:
            time.sleep(5)

        last = snake.move(move_value)
        snake.eat(fruit, last)
        if snake.hit_itself() == True:
            print('dead')
            break
        if fruiteaten:
            fruit = [random.randint(1, 10), random.randint(1, 10)]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        pg.draw.rect(screen, WHITE, [0, 0, 800, 800])
        pg.draw.line(screen, BLACK, [0, 0], [0, 510])
        pg.draw.line(screen, BLACK, [0, 0], [510, 0])
        pg.draw.line(screen, BLACK, [510, 510], [510, 0])
        pg.draw.line(screen, BLACK, [0, 510], [510, 510])
        if snake.hit_wall(0, 16, 0, 16) == True:
            print('crashed')
            break
        if snake.hit_itself() == True:
            print('killed')
            break
        draw_snake(snake, grid, screen)
        draw_fruitxy(grid, fruit, screen)
        pygame.display.update()
        clock.tick(5)

if __name__ == "__main__":
    main()