# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

#---------------------------------------------> changes for 3
def get_bad_apple_time():
    # create a bad apple every 5 to 15 seconds
    return random.randrange(5, 16) * 15
#-----------------------------------------------------------

#----------------------> changes for 4
FPS = 15
#-------------------------------------------

#---------------------------------------> Changes for 2
WINDOWWIDTH = 840
WINDOWHEIGHT = 680
#---------------------------------------

CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

#-------------------- changes for 3
YELLOW = (255, 255, 0)
#--------------------------------

#---------------------> changes for 5
BLUE = (0, 0, 255)
#-------------------------------------------

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
HEAD = 0 # syntactic sugar: index of the worm's head


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.

    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()
    #------------------ changes for 3
    yellowApple = getRandomLocation()
    next_bad_apple = get_bad_apple_time()
    yellow_is_eaten = False
    #----------------------------------------->
    #----------------------> changes for 4
    time_ctr = 30
    speedup_time = 2
    #---------------------------------------------
    #------------------------------------> changes for 5
    blueApple = getRandomLocation()
    next_timeslow_apple = get_bad_apple_time()
    blue_is_eaten = False
    #-------------------------------------------

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

    #-------------------------------------> changes for 5
        color = GREEN
    #--------------------------------------> Changes for 4
        time_ctr -= 1
        print(time_ctr)
        if not time_ctr:
            time_ctr = 30
            print("speed up by")
            print(speedup_time)
            FPSCLOCK.tick(speedup_time)
            speedup_time+=5
            #------------- Changes for 6
            color = BLUE
            #-----------------------
    #---------------------------------------------

        #-------------------------------->Changes for 3
        next_bad_apple -= 1
        #print(next_bad_apple)

        if not next_bad_apple:
            yellowApple = getRandomLocation()
            next_bad_apple = get_bad_apple_time()
            yellow_is_eaten = False
        #-----------------------------------------------------
        #-------------------------------> Changes for 5
        next_timeslow_apple -= 1
        if not next_timeslow_apple:
            blueApple = getRandomLocation()
            next_timeslow_apple = get_bad_apple_time()
            blue_is_eaten = False
        #----------------------------------------------------

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
            #-----------------------> changes for 7
            pygame.mixer.Sound("../../Labs/Lab2/beep3.ogg").play()
            #----------------------------------
        else:
            del wormCoords[-1] # remove worm's tail segment

        #----------------------------------------> changes for 3 eating yellow apple
        if yellow_is_eaten == False:
            if wormCoords[HEAD]['x'] == yellowApple['x'] and wormCoords[HEAD]['y'] == yellowApple['y']:
                del wormCoords[-1]
                next_bad_apple = get_bad_apple_time()
                yellow_is_eaten = True
                yellowApple.clear()
                #-----------------------> changes for 7
                pygame.mixer.Sound("../../Labs/Lab2/beep1.ogg").play()
                #----------------------------------
                #yellowApple = getRandomLocation()
        #--------------------------------------------------------------------------------------------

        #--------------------------------------> changes for 5
        if blue_is_eaten == False:
            if wormCoords[HEAD]['x'] == blueApple['x'] and wormCoords[HEAD]['y'] == blueApple['y']:
                FPSCLOCK.tick(speedup_time - 5)
                next_timeslow_apple = get_bad_apple_time()
                blue_is_eaten = True
                #---------------------> changes for 6
                color = RED
                #----------------------------
                # -----------------------> changes for 7
                pygame.mixer.Sound("../../Labs/Lab2/beep2.ogg").play()
                # ----------------------------------
                blueApple.clear()
        #----------------------------------------------------------------------------

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        #---------------------------------------> changes for 6
        drawWorm(wormCoords, color)
        #----------------------------------------------------
        drawApple(apple)
        #---------------------- changes for 3
        if yellow_is_eaten == False:
            drawYellowApple(yellowApple)
        #-----------------------------------
        #-----------------------> chnages for 5
        if blue_is_eaten == False:
            drawBlueApple(blueApple)
        #------------------------------------------
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(speedup_time)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


#---------------------------------- changes for 6
def drawWorm(wormCoords, color):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, color, wormInnerSegmentRect)
#--------------------------------------------------------------

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

#---------------------------------------> changes for 3
def drawYellowApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, YELLOW, appleRect)

#--------------------------------------------------------

#------------------------------------> changes for 5
def drawBlueApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, BLUE, appleRect)
#------------------------------------------------------


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()