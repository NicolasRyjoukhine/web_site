import os
import sys
import time
import pygame.font
import pygame as pg
from random import randrange



CAPTION = "tennis"
SCREEN_SIZE = (600, 400)
MENU_Y = 50
score_right = 0
score_left = 0

BACKGROUND_COLOR = pg.Color("slategray")
BAR_COLOR = pg.Color("red")
COLOR_KEY = pg.Color("magenta")



clock = pg.time.Clock()
pg.font.init() # you have to call this at the start,
                   # if you want to use this module.
myfont = pg.font.SysFont('Comic Sans MS', 30)
reset_key = pg.K_r

class Circle(object):

    v_x = 5
    v_y = 10
    score_right = 0
    score_left = 0
    freeze = False

    def __init__(self, canvas, circleColor, x, y, rad, thickness, bar1, bar2):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.rad = rad
        self.circleColor = circleColor
        self.thickness = thickness
        self.bar1 = bar1
        self.bar2 = bar2


    def drawcircle(self, screen):
       # cercle = canvas.create_oval(x - rad, y - rad, x + rad, y + rad, width=0, fill=cercleColor)
        pg.draw.circle(screen, self.circleColor, (self.x, self.y), self.rad, self.thickness)
        if self.y + self.rad >= SCREEN_SIZE[1] or self.y <= self.rad + MENU_Y:
            self.v_y = -self.v_y
        if self.x + self.rad >= SCREEN_SIZE[0] or self.x <= self.rad:
            self.v_x = -self.v_x

        if(self.x - self.rad <=  self.bar1.x + self.bar1.width and self.y >=  self.bar1.y and self.y <=  self.bar1.y +  self.bar1.height):
            self.v_x = -self.v_x
        if(self.x + self.rad >=  self.bar2.x and self.y >=  self.bar2.y and self.y <=  self.bar2.y +  self.bar2.height):
            self.v_x = -self.v_x
        if(SCREEN_SIZE[0] - self.x <= self.rad):#right
            self.v_x = 0
            self.v_y = 0
            if not self.freeze:
                self.score_right += 1 ; print("score right", self.score_right)
                self.freeze = True

        if(self.x <= self.rad):#left
            self.v_x = 0
            self.v_y = 0
            if not self.freeze:
                self.score_left += 1 ; print("score left:", self.score_left)
                self.freeze = True

        self.x += self.v_x
        self.y += self.v_y

class Bar(object):

    def __init__(self, x, y, width, height, key_up, key_own):
        self.x = x
        self.y = y
        self.width = width
        self.height= height
        self.key_up = key_up
        self.key_own = key_own
        self.move_up = False
        self.move_down = False

        self.rect = pg.rect.Rect((self.x, self.y, self.width, self.height))


    def handle_keys(self):
        key = pg.key.get_pressed()

        if key[self.key_up] or self.move_up:
            if self.y > 0 + MENU_Y:
                self.rect.move_ip(0, -5)
                self.y -= 5
                self.move_up = False
        if key[self.key_own] or self.move_down:
            if self.y < SCREEN_SIZE[1] - self.height:
                self.rect.move_ip(0, 5)
                self.y += 5
                self.move_down = False

    def draw(self, screen):
        """
        Draws the player to the target surface.
        """
        pg.draw.rect(screen, (0, 0, 128), self.rect)



def computer_player(bar, circle):
    if bar.y + bar.height / 2 >= circle.y:
        bar.move_up = True
    if bar.y + bar.height / 2 <= circle.y:
        bar.move_down = True


def main():

    running = True
    pg.init()

    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    bar1 = Bar(10, 80, 20, 100, pg.K_q, pg.K_a)
    bar2 = Bar(570, 80, 20, 150, pg.K_UP, pg.K_DOWN)
    screen = pg.display.get_surface()
    circle = Circle(screen, COLOR_KEY, 150, 80, 15,  1, bar1, bar2)

    pg.font.init()  # you have to call this at the start,
    # if you want to use this module.
    basicfont = pygame.font.SysFont(None, 28)
    text = basicfont.render(str(Circle.score_left) + '|' + str(Circle.score_right), True, (0, 0, 0), (255, 255, 255))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = 50

    pg.draw.line(screen, (0, 225, 255), (20, 50), (20, 550))
    pg.display.update()


    y_change = 0

    while running:

        for evt in pg.event.get():
            if evt.type == pg.KEYDOWN:
                if evt.key == pg.K_ESCAPE:
                    running = False
                if evt.key == pg.K_r:
                    circle.v_x = 5
                    circle.v_y = 10
                    circle.x = randrange(150, 450)
                    circle.y = randrange(50, 350)

        screen.fill((255, 255, 255))

        bar1.draw(screen)
        bar2.draw(screen)
        circle.drawcircle(screen)
        bar1.handle_keys()
        bar2.handle_keys()
        pg.draw.line(screen, (0, 225, 255), (0, 50), (600, 50))
        pg.draw.line(screen, (0, 225, 255), (0, 51), (600, 51))
        text = basicfont.render(str(circle.score_left) + '|' + str(circle.score_right) + '  (press "R" to restart) use "a" move up and "q" to move down ', True, (255, 0, 0), (255, 255, 255))
        textrect = text.get_rect()
        screen.blit(text, textrect)
        computer_player(bar2, circle)
        pg.display.update()
        clock.tick(40)




    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()