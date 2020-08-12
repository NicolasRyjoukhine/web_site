import pygame, sys, time
from sys import exit

width = 600
height = 480
fps = 1
color_blanc = (225, 225, 225)
color_jaune = (225, 225, 0)
color_noir = (0, 0, 0)

# box_surace

color_box_surface = (99, 57, 47)
size_box_surface = (24, 96)
box_position = (50, 200)
# circle(Surface, color, pos, radius, width=0) -> Rect


# box_surface_1

color_box_surface_1 = (25, 99, 55)
size_box_surface_1 = (24, 96)

clock = pygame.time.Clock()


def event_action(evt):
    if evt.type == pygame.KEYUP:
        if evt.key == pygame.K_SPACE:
            print('up')
    if evt.type == pygame.KEYDOWN:
        if evt.key == pygame.K_SPACE:
            print('down')


def main():
    pygame.init()
    running = True
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tennis")

    box_surface = pygame.Surface(size_box_surface)
    box_rect = box_surface.get_rect()
    box_rect.center = box_position
    box_surface.fill((25, 0, 100))

    box_surface_1 = pygame.Surface(size_box_surface_1)
    box_rect_1 = box_surface_1.get_rect()
    box_rect_1.center = (300, 240)
    box_surface_1.fill(color_box_surface_1)
    circle_surface = pygame.Surface((100, 100))

    draw_circle(circle_surface, color_jaune, (50, 50), 50, )

    y_change = 0

    while running:

        screen.fill(color_noir)
        screen.blit(box_surface, (560, 10))
        screen.blit(box_surface_1, (20, 10))
        pygame.display.flip()

        for evt in pygame.event.get():
            event_action(evt)
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_ESCAPE:
                    running = False
                elif evt.key == pygame.K_DOWN:
                    print('key hit', box_rect)
                    y_change = 5
                elif evt.key == pygame.K_UP:
                    print('key hit', box_rect)
                    y_change = -5

        box_rect.y = box_rect.y + y_change
        screen.blit(box_surface, (box_rect.x, box_rect.y))
        screen.blit(box_surface_1, (200, 200))
        print(box_rect)

        pygame.display.update()
        clock.tick(60)

    time.sleep(2)
    pygame.quit()
    exit()


def draw_circle(image, colour, origin, radius, width=0):
    if width == 0:
        pygame.draw.circle(image, colour, origin, int(radius))
    else:
        if radius > 65534 / 5: radius = 65534 / 5
        circle = pygame.Surface([radius * 2 + width, radius * 2 + width]).convert_alpha()
        circle.fill([0, 0, 0, 0])
        pygame.draw.circle(circle, colour, [circle.get_width() / 2, circle.get_height() / 2]), int(radius + (width / 2))
        if int(radius - (width / 2)) > 0: pygame.draw.circle(circle, [0, 0, 0, 0],
                                                             [circle.get_width() / 2, circle.get_height() / 2]), abs(
            int(radius - (width / 2)))
        image.blit(circle, [origin[0] - (circle.get_width() / 2), origin[1] - (circle.get_height() / 2)])


if __name__ == '__main__':
    main()

    pygame.init()

    display_width = 800
    display_height = 600
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('A bit Racey')

    black = (0, 0, 0)
    white = (255, 255, 255)

    clock = pygame.time.Clock()
    crashed = False
    carImg = pygame.image.load('racecar.png')


    def car(x, y):
        gameDisplay.blit(carImg, (x, y))


    x = (display_width * 0.05)
    y = (display_height * 0.8)
    x_change = 0
    car_speed = 0

    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            ############################
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
            ######################
        ##
        x += x_change
        ##
        gameDisplay.fill(white)
        car(x, y)

        pygame.display.update()
        clock.tick(600)

    pygame.quit()
    quit()
