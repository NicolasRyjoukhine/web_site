import pygame.font
import pygame as pg
from turtle import *
from pygame.locals import *
import random
import copy

CAPTION = "Tetris"
SCREEN_SIZE = (1200, 1000)
SQUARE_SIZE = 40
BOX_COORDS = (740, 40)
BOX_HEIGHT = 24
BOX_WIDTH = 8
BACKGROUND_COLOR = pg.Color("White")

score = 0

YELLOW = pg.Color("yellow")
RED = pg.Color("red")
BLUE = pg.Color("blue")
BLACK = pg.Color("black")
WHITE = pg.Color("white")
GREEN = pg.Color('green')
clock = pg.time.Clock()
pg.font.init()
myfont = pg.font.SysFont('maison Sans MS', 30)


cube = [[[0, 0], [0, 1], [1, 0], [1, 1]],
       [[0, 0], [0, 1], [1, 0], [1, 1]],
       [[0, 0], [0, 1], [1, 0], [1, 1]],
       [[0, 0], [0, 1], [1, 0], [1, 1]]]

line = [[[0, 0], [0, 1], [0, 2]],
        [[0, 0], [1, 0], [2, 0]],
        [[2, 0], [2, 1], [2, 2]],
        [[0, 2], [1, 2], [2, 2]]]
pyramide = [[[0, 0], [0, 1], [0, 2], [1, 1]],
            [[0, 0], [1, 0], [2, 0], [1, 1]],
            [[2, 0], [2, 1], [2, 2], [1, 1]],
            [[0, 2], [1, 2], [2, 2], [1, 1]]]
angle = [[[0, 0], [0, 1], [0, 2], [1, 0]],
         [[0, 0], [1, 0], [2, 0], [2, 1]],
         [[2, 2], [2, 1], [2, 0], [1, 2]],
         [[0, 1], [0, 2], [2, 2], [1, 2]]]

shapes_structure = [cube, line, pyramide, angle]
selected_shapes = []

class Square(object):

    def __init__(self, x, y, size, color = RED):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.rect = pg.rect.Rect((self.x, self.y, self.size, self.size))

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)


class Circle(object):
    def __init__(self, circle_color, x, y, rad, thickness, shape=None):
        self.x = x
        self.y = y
        self.rad = rad
        self.circleColor = circle_color
        self.thickness = thickness
        self.shape = shape

    def drawcircle(self, screen):
        pg.draw.circle(screen, RED, (self.x, self.y), self.rad, self.thickness)
        if self.shape is not None:
            shape = Shape(self.x + 20, self.y, SQUARE_SIZE, self.shape, BLUE, WHITE)
            shape.draw(screen, True)


class Shape(object):
    def __init__(self, x, y, square_size, states, fill_color, background_color):
        self.states = states
        self.select_color = fill_color
        self.delete_color = background_color
        self.index = 0
        self.state = states[self.index]
        self.x = x
        self.y = y
        self.square_size = square_size

    def rotate(self, screen):
        if self.index == 3:
            self.index = 0
        else:
            self.index = self.index + 1
        self.state = self.states[self.index]

    def can_move(self, fix_states):
        result = True
        for coordinates in self.state:
            if coordinates[0] == BOX_WIDTH - 1:
                result = False
        return result

    def move_side(self, fix_states):
        for coordinates in self.state:
            if coordinates[1] == BOX_HEIGHT - 1:
                result = False

    def fall(self, fix_states):
        for state in self.states:
            for cell in state:
                cell[1] = cell[1] + 1

    def draw(self, screen, show):
        current_color = self.select_color
        if not show:
            current_color = self.delete_color
        for coordinates in self.state:
            x, y = self.x + coordinates[0] * self.square_size, self.y + coordinates[1] * self.square_size
            rect = Square(x, y, self.square_size, current_color)
            rect.draw(screen)


def text_to_screen(screen, text, x, y, size=50, color=(2, 2, 25)):
    try:
        text = str(text)
        text = myfont.render(text, True, color)
        screen.blit(text, (x, y))
    except:
        print('Font Error, saw it coming')


def draw_circles(screen):

    circle1 = Circle(RED, 65, 200, 10, 10, cube)
    circle2 = Circle(RED, 65, 520, 10, 10, pyramide)
    circle3 = Circle(RED, 305, 200, 10, 10, angle)
    circle4 = Circle(RED, 305, 520, 10, 10, line)

    pg.draw.line(screen, (0, 0, 255), (0, 40), (1200, 40))
    pg.draw.line(screen, (0, 0, 255), (0, 0), (1200, 0))
    pg.draw.line(screen, (255, 0, 255), (740, 40), (740, 1000))
    pg.draw.line(screen, (255, 0, 255), (1060, 40), (1060, 1000))
    pg.draw.line(screen, (0, 0, 255), (600, 0), (600, 1000))
    pg.draw.line(screen, (0, 0, 255), (600, 0), (600, 1000))

    circle1.drawcircle(screen)
    circle2.drawcircle(screen)
    circle3.drawcircle(screen)
    circle4.drawcircle(screen)

    return [circle1, circle2, circle3, circle4]


def selected_circles(circles):
    for circle in circles:
        if circle.thickness == 2:
            return True
    return False


def main():
    running = True
    start_pressed = False
    grid = []
    fix_states = []
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    screen = pg.display.get_surface()
    screen.fill((75, 75, 75))
    pg.font.init()
    basicfont = pygame.font.SysFont(None, 60)
    text = basicfont.render('         Choose your forms.                     Press SPACE start.', True, (55, 0, 0), BLACK)
    text1 = basicfont.render('Start', True, (55, 0, 0), BLACK)

    for k in range(BOX_HEIGHT):
        row = []
        for i in range(BOX_WIDTH):
            cell = (BOX_COORDS[0] + i * BOX_COORDS[1], BOX_COORDS[1] + k * SQUARE_SIZE, RED, (k, i))
            row.append(cell)
            sq = Square(cell[0], cell[1], SQUARE_SIZE)
            sq.draw(screen)
        grid.append(row)

    circles = draw_circles(screen)

    shape = None
    start_circle = Circle(WHITE, 250, 800, 150, 10)
    start_circle.drawcircle(screen)
    while running:
        keys = pygame.key.get_pressed()
        if keys[K_SPACE] and shape:
                shape.draw(screen, False)
                shape.rotate(screen)
                shape.draw(screen, True)
        evt = pygame.event.get()
        for event in evt:
            if event.type == pygame.MOUSEBUTTONDOWN and not start_pressed:
                pos = pygame.mouse.get_pos()
                for circle in circles:
                    if circle.x - circle.rad < pos[0] < circle.x + circle.rad and \
                            circle.y - circle.rad < pos[1] < circle.y + circle.rad:
                        pg.draw.circle(screen, YELLOW, (circle.x, circle.y), circle.rad, circle.thickness)
                        if circle.thickness == 10:
                            circle.thickness = 2
                            if not circle.shape in selected_shapes:
                                selected_shapes.append(circle.shape)
                        else:
                            circle.thickness = 10
                            if circle.shape in selected_shapes:
                                selected_shapes.remove(circle.shape)
                        circle.drawcircle(screen)

                if selected_circles(circles) and not start_pressed:
                    pg.draw.circle(screen, GREEN, (start_circle.x, start_circle.y), start_circle.rad, start_circle.thickness)
                    start_circle.thickness = 1
                    start_circle.drawcircle(screen)
                    text_to_screen(screen, 'Start', start_circle.x - 25, start_circle.y, 500, BLACK)
                    if start_circle.x - start_circle.rad < pos[0] < start_circle.x + start_circle.rad\
                            and start_circle.y - start_circle.rad < pos[1] < start_circle.y + start_circle.rad:
                        start_pressed = True

                else:
                    start_circle.thickness = 150
                    start_circle.drawcircle(screen)
                    text_to_screen(screen, 'Choose your forms', start_circle.x - 100, start_circle.y, 500, BLACK)

            if event.type == pygame.K_r:
                print('mmkuffykfkufkuhkrrrr')

        if start_pressed and not shape:
            shape_structure = copy.deepcopy(selected_shapes[random.randint(0, len(selected_shapes) - 1)])
            shape = Shape(BOX_COORDS[0], BOX_COORDS[1], SQUARE_SIZE, shape_structure, YELLOW, RED)
            print('new shape created', shape.state)

        if shape and shape.can_move(fix_states):
            shape.draw(screen, False)
            shape.fall(fix_states)
            shape.draw(screen, True)
            print('keep drawing shape...')
        else:
            shape = None

        pg.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main()
