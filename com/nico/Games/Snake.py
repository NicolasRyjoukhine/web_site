import pygame.font
import pygame as pg


BLACK = pg.Color('black')
WHITE = pg.Color('white')
RED = pg.Color('red')
clock = pg.time.Clock()
screen = pygame.display.set_mode((800, 800))


class Snake(object):
    def __init__(self, color, init_x, init_y,):
        self.color = color
        self.pos = [init_x, init_y]

    def move(self):
        pass


def main():
    pygame.init()
    screen.fill(WHITE)
    pygame.display.set_caption("Snakes")

    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        pygame.display.update()
        clock.tick(5)


if __name__ == "__main__":
    main()
