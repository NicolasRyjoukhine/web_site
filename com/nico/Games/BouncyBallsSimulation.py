import pygame as pg
from pygame.locals import *
from tkinter import *
import random
import math
import time

clock = pg.time.Clock()
pg.font.init()  # you have to call this at the start

root = Tk()
screenWidth = 800
screenHeight = 800
screen = pg.display.set_mode((screenWidth, screenHeight))

circle_img = pg.image.load("D:\\nicoPrj\web_site\com\\nico\Games\Images\circleround.png").convert_alpha()
line_img = pg.image.load("D:\\nicoPrj\web_site\com\\nico\Games\Images\Line.png").convert_alpha()

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


totalLines = []
total_line_points = []
safe_val_y = []
current_y_add = [2]

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


def draw_line(p1x, p1y, p2x, p2y, what_color):
    pg.draw.line(screen, what_color, [p1x, p1y], [p2x, p2y])


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
    print(angle)

    if angle <= 0:
        angle = angle * -1
        print(angle)
    get_cos = math.asin(angle) * 180 / math.pi
    print(get_cos)
    return round(get_cos - 180)


def gravity_acting(y, x, trampoline_x, trampoline_y):
    current_y_add.append(y+x)
    if y < 0:
        new_y = y - (y/10*9.8)  # I want to remove 0.98 but i can t because i can t remove .98 pixel for but only one
        return new_y
    else:
        if 350 < trampoline_x < 450 and y < trampoline_y-y+5 and y > trampoline_y+y+5 and y < 10:
            new_y = 1
            return new_y
        else:
            '''
                y -= 0.98
            '''
            new_y = y + 1  # I want to add 0.98 but i can t because i can t add .98 pixel
            return new_y


def draw_button(x, y, radius):
    circle = Circle(screen, radius + 20, [x, y], SHADOW, False)
    circle.drawcircle()
    circle2 = Circle(screen, radius, [x, y], RED, False)
    circle2.drawcircle()


def get_all_points_line(point1, point2):
    """
    This function saves all the points in a line
    using the ratio that can be using with the angle.
    It returns a list with all the values in it
    """
    add_values = []
    angle = get_angle(point1, point2)
    ratio = return_ration_using_angle(angle)
    for i in range(point2-point1):
        add_values.append(point1+ratio[0] + i)  # } adding the X coords
        add_values.append(point1+ratio[1] + i)  # } adding the Y coords
        add_values.append(angle)            # Saving the angle for future use

        total_line_points.append(add_values)  # saving them to a list with all the points

        add_values.clear()  # clearing the list


def return_ration_using_angle(angle):
    return_list = []
    get_y_up = round(angle * 100)
    get_x_up = 100
    return_list.append(get_x_up)
    return_list.append(get_y_up)
    return return_list


def switch_modes(ismode, mode):
    mode.clear()
    if ismode:
        mode.append(2)
        return False
    elif not ismode:
        mode.append(1)
        return True


def return_minus_in_pos(first, second=0):
    return_val = first-second
    if return_val < 0:
        return return_val * -1
    return return_val


def get_return_angle_with_slope(line_angle):
    return line_angle * -1


class Line:
    def __init__(self, first_pos, second_pos, game_screen):
        self.x1 = first_pos[0]
        self.y1 = first_pos[1]
        self.x2 = second_pos[0]
        self.y2 = second_pos[1]
        self.image = line_img
        self.screen = game_screen
        self.mask = pg.mask.from_surface(self.image)
        self.angle = get_angle(first_pos, second_pos)
        self.scaled_img = pg.transform.scale(self.image, (return_minus_in_pos(self.x2, self.x1), 50))

    def drawline(self, what_color):
        try:
            angled_image = pg.transform.rotate(self.scaled_img, self.angle+90)
            self.screen.blit(angled_image, [return_minus_in_pos(self.x1 + self.x2/2),
                                            return_minus_in_pos(self.y1 + self.y2/2)])
        except Exception as e:
            print(e)
            pg.draw.line(screen, what_color, [self.x1, self.y1], [self.x2, self.y2])

    def return_mask(self, circle):
        bird_mask = circle_img.get_mask()
        top_mask = pg.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pg.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - circle.x, self.top - round(circle.y))
        #bottom_offset = (self.x - circle.x, self.bottom - round(bird.y))

        #b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)


class TkinterWindow:
    def __init__(self, height, width, name_of_window, tkinter_root):
        self.root = tkinter_root
        self.height = height
        self.width = width
        self.name = name_of_window

    def init_window(self):
        root.title(self.name)
        root.geometry('{}x{}'.format(self.width, self.height))

    def create_button(self, text, command, pos_x, pos_y):
        button = Button(self.root, text=text, command=command)
        button.grid(row=pos_y, column=pos_x)


class TextOnScreen:
    def __init__(self, text, x, y, chosen_color):
        self.text = text
        self.x = x
        self.y = y
        self.color = chosen_color

    def draw_text(self):
        try:
            text_font = pg.font.SysFont('Comic Sans MS', 30)
            text_surface = text_font.render(self.text, False, self.color)
            screen.blit(text_surface, (self.x, self.y))
        except Exception as e:
            print('TextOnScreen Error:', e)


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
            self.screen.blit(tramp, [self.positionx[0] + 16, self.positionx[1] - 20])
        except Exception as e:
            print(e)
            draw_line(self.positionx[0], self.positionx[1], self.positiony[0], self.positionx[1], BLUE)
            draw_line(self.positionx[0], self.positionx[1], self.positionx[0], self.positiony[1], BLUE)
            draw_line(self.positiony[0], self.positiony[1], self.positiony[0], self.positionx[1], BLUE)

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
            draw_line(self.positionx[0], self.positionx[1], self.positiony[0], self.positionx[1], BLUE)
            draw_line(self.positionx[0], self.positionx[1], self.positionx[0], self.positiony[1], BLUE)
            draw_line(self.positiony[0], self.positiony[1], self.positiony[0], self.positionx[1], BLUE)


class Circle:
    def __init__(self, game_screen, circle_radius, position, chosen_color, is_random):
        self.is_random = is_random
        self.screen = game_screen
        self.circleradius = circle_radius
        self.position = position
        self.color = chosen_color
        self.img = circle_img
        self.rescale = pg.transform.scale(self.img, (self.circleradius*2, self.circleradius*2))
        self.circle_width = self.img.get_width()
        self.mask = pg.mask.from_surface(self.img)

    def drawcircle(self):
        """This Function Uses the PyGame Module to create Circle.
                 it will use 'try' to try and load a ball image
                 and if it can't, it will draw a normal circle"""
        try:
            self.screen.blit(self.img, [self.position[0] + self.circle_width,
                                            self.position[1]])
            print(' A circle has appeared at: {}, {}'.format(self.position[0], self.position[1]))
        except Exception as e:
            print(e)
            if self.is_random:
                pg.draw.circle(
                    self.screen, self.color, self.position, get_numb(5, 50)
                )
            else:
                pg.draw.circle(
                    self.screen, self.color, self.position, self.circleradius
                )

    def move_ball(self):
        if self.position[0] + self.circleradius >= screenWidth:
            print("The Circle has Touched the {} line".format('right'))
            add_x = 2
            self.position[0] += add_x

        if self.position[0] + self.circleradius <= screenWidth- screenWidth:
            print("The Circle has Touched the {} line".format('left'))
            add_x = 2
            self.position[0] -= add_x

        if self.position[1] + self.circleradius >= screenHeight:
            print("The Circle has Touched the {} line".format('bottom'))
            add_y = 2
            self.position[1] += add_y

        if self.position[1] + self.circleradius <= screenHeight:
            print("The Circle has Touched the {} line".format('top'))
            add_y = 2
            self.position[1] -= add_y

        if 350 < self.position[0] < 450:
            if self.position[1] >= 750 - self.circleradius or self.position[1] >= 750 + self.circleradius:
                if self.position[1] < 774:
                    print("The Circle has Touched the trampoline line")
                    add_y = 2
                    self.position[1] -= add_y

    def check_mask(self, terrain_mask):
        overlap_mask = self.mask.overlap_mask(terrain_mask, (0, 0))
        print(overlap_mask.count())
        if overlap_mask:
            print('I AM CALLED\n')
            angle_of_arrow = get_angle([self.position[0], self.position[1]], current_mouse_position())
            self.position[0] += return_ration_using_angle(angle_of_arrow)[0]
            self.position[0] += return_ration_using_angle(angle_of_arrow)[1]
        else:
            return False


def main():
    """The script allows the user to create one or more circles
        and to see them react in an environment with real-life
        physics using the PyGame interface"""

    is_simulation_running = True
    is_circle_appeared = False
    is_need_for_update = True
    anti_gravity = False
    reset = False
    is_mode_2 = False
    is_mode_2_aiming = False

    circle_radius = 20
    circle_save_coordinates = [250, 250]
    save_mouse_pos = [0, 0]
    save_last_pos = [1, 2]
    temp_save = []
    mode = [1]

    all_arrows = [picture_arrow1, picture_arrow2, picture_arrow3, picture_arrow4]
    current_arrow = picture_arrow1

    a = 0
    add_x = 0
    add_y = 0
    clock_tick = 60
    tick = 0
    arrow_val_temp = 0

    pg.init()  # initializing the Simulation
    pg.font.init()  # you have to call this at the start,
    pg.display.set_caption("Bouncy Balls Simulation")

    while is_simulation_running:
        screen.blit(picture, [0 - 400, 0])
        # deletes all circles to replace with new affected by physics

        # call all the objects

        # create new Tkinter window with coordinates and set different
        tkinter_window = TkinterWindow(200, 200, 'Switch Mode?', root)

        # create a line terrain that is angled
        line = Line([-50, 200], [150, 300], screen)
        # draw text on screen when changing modes
        text_screen = TextOnScreen('You are in mode {}'.format(mode[0]), 320, 100, BLUE)

        # create new trampoline at these positions and use physics let things jump on it..
        trampoline = Trampoline(screen, [350, 750], [450, 800], 10, BLUE)

        # create new circle at these positions and use physics to move it.
        circle = Circle(screen, circle_radius,
                              [circle_save_coordinates[0], circle_save_coordinates[1]],
                              RED, False)

        for event in pg.event.get():
            keys = pg.key.get_pressed()
            if event.type == pg.MOUSEBUTTONDOWN and not is_mode_2_aiming:
                new_coords_circle_x = current_mouse_position()[0]
                new_coords_circle_y = current_mouse_position()[1]
                circle_save_coordinates.clear()
                circle_save_coordinates.append(new_coords_circle_x)
                circle_save_coordinates.append(new_coords_circle_y)
                is_circle_appeared = True
                reset = True
                add_x = 0
                add_y = 0
                tick = 0

            if keys[K_SPACE]:

                current_arrow = all_arrows[arrow_val_temp]
                arrow_val_temp += 1
                mode.clear()

                if arrow_val_temp == 3:
                    arrow_val_temp = 0

                if is_mode_2:
                    is_mode_2 = False
                    mode.append(2)
                else:
                    is_mode_2 = True
                    mode.append(1)

            if keys[K_1] and is_mode_2:
                save_mouse_pos.clear()
                save_mouse_pos.append(current_mouse_position()[0])
                save_mouse_pos.append(current_mouse_position()[1])
                is_mode_2_aiming = True

            if keys[K_1] and not is_mode_2:
                save_last_pos.append(current_mouse_position())
                is_mode_2_aiming = False

            if event.type == pg.QUIT:
                pg.quit()

        line.drawline(RED)

        try:
            trampoline.draw_trampoline_top()
            tkinter_window.create_button("Do you want to Boost the ball in a direction?",
                                         switch_modes(is_mode_2, mode), 1, 1)
            if is_mode_2:
                draw_button(save_mouse_pos[0], save_mouse_pos[1], 20)
                if is_mode_2:
                    angle_of_arrow = get_angle([save_mouse_pos[0], save_mouse_pos[1]], current_mouse_position())
                    arrow_img_draw = pg.transform.rotate(current_arrow, angle_of_arrow)
                    screen.blit(arrow_img_draw, [save_mouse_pos[0] - int(round(arrow_img_draw.get_width() / 2)),
                                                 save_mouse_pos[1] - int(round(arrow_img_draw.get_height() / 2))])

        except Exception as e:
            print(e)

        text_screen.draw_text()
        a += 1

        if is_mode_2:
            temp_save.append(add_x)
            temp_save.append(add_y)
            add_x = 0
            add_y = 0
            #  This here sets the ball to pause and allows the player to "charge" and add velocity to the ball

        if is_circle_appeared:
            if anti_gravity:
                if reset:
                    add_y = -1 * (int(float(gravity_acting(add_y,
                                                           circle_save_coordinates[0],
                                                           circle_save_coordinates[1], add_x))))
                    anti_gravity = False
                    reset = False
            else:
                if tick <= 180:
                    add_y = 1 * (int(float(gravity_acting(add_y,
                                                          circle_save_coordinates[0],
                                                          circle_save_coordinates[1], add_x))))
                else:
                    add_y = current_y_add[0]

                if circle.check_mask(line.mask):
                    add_x = (line.angle + 45)/100 * 2
                    add_y = (line.angle - 45)/100 * 2

            circle_save_coordinates[0] += add_x
            circle_save_coordinates[1] += add_y
            circle.move_ball()
            circle.drawcircle()
            current_y_add.clear()
            trampoline.draw_trampoline_bottom()


        if is_circle_appeared:
            circle_save_coordinates[0] += add_x
            circle_save_coordinates[1] += add_y

        if tick == 180:
            tick = 0
        else:
            tick += 1

        pg.display.update()
        clock.tick(clock_tick)


if __name__ == "__main__":
    main()
