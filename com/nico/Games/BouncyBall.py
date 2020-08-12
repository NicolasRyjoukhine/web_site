import pygame as pg
import random
from pathlib import Path
import time
import math

data_folder = Path("source_data/text_files/")

clock = pg.time.Clock()

screenHeight = 800
screenWidth = 800

screen = pg.display.set_mode((screenHeight, screenWidth))
isSimulationRunning = True

# bgImg = pg.image.load("C:/downloads/bouncyBallsSimulationBG.png")

global gforceacting
gforceacting = 0
totalLines = []

firstCoords = []
secondCoords = []


SHADOW = (192, 192, 192)
WHITE = (255, 255, 255)
LIGHTGREEN = (0, 255, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 128)
LIGHTBLUE = (0, 0, 255)
RED = (200, 0, 0)
LIGHTRED = (255, 100, 100)
PURPLE  = (102, 0, 102)
LIGHTPURPLE = (153, 0, 153)


def genNumb(minValue, maxValue):
    return random.randint(minValue, maxValue)


def currentMousePosition():
    mouseposis = pg.mouse.get_pos()
    return mouseposis


def drawLine(f_posX, f_posY, s_posX, s_posY, color):
    return pg.draw.line(screen, color, [f_posX, f_posY], [s_posX, s_posY])


def getAllPoints(pointX1, pointX2, pointY1, pointY2):
  ratioOfXtoY = pointX1 / pointX2
  ratioOfYtoX = pointY1 / pointY2
  ratioTotal = [ratioOfXtoY + ratioOfYtoX]
  print('The Change of X for 1 Y is of :{}\nThe Change of Y to 1 X is of:{}'.format(ratioOfXtoY, ratioOfYtoX))
  return ratioTotal

# find the opposite and the adjecent using pythagorem's theorem and SAHCOHTAH


def checkIsOdd(number):
  if (number % 2) == 0:
    return True
  else:
    return False


def checkIfXorYonLine(circleCoords, x, y):
    v = 0
    for i in totalLines[v]:
      print(v)
      for a in [i]:
        for e in circleCoords:
          if checkIsOdd(a)==False and a == e:
            x += -1
          if checkIsOdd(a) and a == e:
            y += -1
          print(x)
          print(y)
          print('the i value is {}\nthe a value is {}\nthe e value is {}'.format(i, a, e))
          v += 1

def createCircle(radius, position, color, screen, isRandom, minValue, maxValue):
    """This Function Uses the PyGame Module to create Circle.
        It has a random function build in"""
    if isRandom == True:
        pg.draw.circle(screen,
                       (genNumb(minValue, maxValue),
                        genNumb(minValue, maxValue),
                        genNumb(minValue, maxValue)),
                       position,
                       genNumb(minValue, maxValue))
    else:
        pg.draw.circle(screen, color, position, radius)

class Physics():
    """This is the Physics class which will define
       how objects react in the different environments"""

    def __init__(self, screen, weigth, speed, color, gForce, objectX, objectY, circleRadius, position):
        self.screen = screen
        self.weight = weigth
        self.speed = speed
        self.color = color
        self.gForce = gForce
        self.x = objectX
        self.y = objectY
        self.radius = circleRadius
        self.position = position



    def returnAngle(self):
        pass

    def hitAngledWall(self):
        for line in totalLines:
            for perimiter in self.x and self.y:
                if perimiter == self.x or self.y:
                    print('line hit')


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


    isCircleAppeared = False
    isNeedForUpdate = True
    circleRadius = 20
    circleSaveCoords = [250, 250]
    gForce = 2
    addedspeed = 0
    addX = 0
    addY = 0
    yChange = 1
    xChange = 1

    newCoordsCircleX = 0
    newCoordsCircleY = 0

    pg.init()  # initializing the Simulation
    pg.display.set_caption("Bouncy Balls Simulation")

    while isSimulationRunning:
        print("The Simulation is running")
        screen.fill(SHADOW)  # deletes all circles to replace with new affected by physics

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                createCircle(circleRadius, [currentMousePosition()[0],
                                            currentMousePosition()[1]],
                                            RED, screen, False, 0, 0)
                newCoordsCircleX = currentMousePosition()[0]
                newCoordsCircleY = currentMousePosition()[1]
                circleSaveCoords.clear()
                circleSaveCoords.append(newCoordsCircleX)
                circleSaveCoords.append(newCoordsCircleY)
                isCircleAppeared = True
                print(circleSaveCoords)
                # create new circle at these positions and use physics to move it.


            if event.type == pg.QUIT:
                pg.quit()

        isNeedForUpdate = True
        print("Updating Physics")

        if circleSaveCoords[0] + circleRadius == screenHeight:
            print("The Circle has Touched the {} line".format('right'))
            addX = -1
            isNeedForUpdate = False

        if circleSaveCoords[0] - circleRadius == screenHeight - screenHeight:
            print("The Circle has Touched the {} line".format('left'))
            addX = 1
            isNeedForUpdate = False

        if circleSaveCoords[1] + circleRadius == screenHeight:
            print("The Circle has Touched the {} line".format('bottom'))
            addY = -1
            isNeedForUpdate = False

        if circleSaveCoords[1] - circleRadius == screenHeight - screenHeight:
            print("The Circle has Touched the {} line".format('top'))
            addY = 1
            isNeedForUpdate = False


        physics = Physics(
            screen, 2, 2, RED, gForce,
            circleSaveCoords[0], circleSaveCoords[1],
            circleRadius, currentMousePosition()
            )

        if isCircleAppeared:
            addX = 0
            addY = 0
            print(addX, addY)
            circleSaveCoords[0] += addX
            circleSaveCoords[1] += addY
            createCircle(circleRadius, [circleSaveCoords[0],
                                    circleSaveCoords[1]],
                                     RED, screen, False, 0, 0)

        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
