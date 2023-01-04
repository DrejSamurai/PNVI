# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
    # http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
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
YELLOW    = pygame.color.Color('yellow')

#---------------------------------------------> Changes for 1
CRIMSON = (220,20,60)
CRIMSON_FLASH = (205,85,85)
#--------------------------------------------------------------
#-----------------------------------------------> Changes for 2
CARROT = (237 ,145,33)
CARROT_FLASH = (205,102,0)
#----------------------------------------------------------------

BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#---------------------------------------------------------> Changes for 1
directions = [UP, DOWN, LEFT, RIGHT]
directions_dict = {'left': LEFT, 'down': DOWN, 'right':RIGHT, 'up':UP}
HEAD = 0
evilWormHead = 0
show_flag = True
#--------------------------------------------------------------------------


def main(flag=True):
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')
#-------------------------------------------------------> Changes for 3
    if flag:
        showStartScreen()
    while True:
        runGame()
        showGameOverScreen()
#-------------------------------------------------------------

def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]

    #---------------------------------------------------> Changes for 1
    evilWormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]

    direction = RIGHT
    evil_worm_direction = LEFT
    evilWormHead = 0

    start_ticks_worm = pygame.time.get_ticks()
    counter = 20
    flag = 'hidden'
    #--------------------------------------------------------------------------

    #----------------------------------------------------> Changes for 2
    start_ticks_ele = pygame.time.get_ticks()
    counter_elements = 5
    flag_elements = 'hidden'

    start_ticks_ele2 = pygame.time.get_ticks()
    counter_elements2 = 7
    flag_elements2 = 'hidden'
    #------------------------------------------------------------------------

    # Start the apple in a random place.
    apple = getRandomLocation()

    #----------------------------------> Changes for 2
    point_element1 = getRandomLocation()
    point_element2 = getRandomLocation()

    score_sub = 0
    score_plu = 0
    #----------------------------------------------------------

    while True: # main game loop
        #---------------------------------------> Changes for 1
        evil_worm_time = (pygame.time.get_ticks() - start_ticks_worm) / 1000
        evil_worm_time = int(evil_worm_time)
        #---------------------------------------------------------------

        #--------------------------------------------------------> Changes for 2
        five_sec_food = (pygame.time.get_ticks() - start_ticks_ele ) / 1000
        five_sec_food = int(five_sec_food)

        seven_sec_food = (pygame.time.get_ticks() - start_ticks_ele2 ) / 1000
        seven_sec_food = int(seven_sec_food)
        #------------------------------------------------------------------------------

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


        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 \
                or wormCoords[HEAD]['x'] == CELLWIDTH \
                or wormCoords[HEAD]['y'] == -1 \
                or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        #---------------------------------------------------------------> Changes for 1
        if flag == 'shown':
            flag_direction = True
            while flag_direction:
                evil_worm_direction = random.choice(directions)
                position_x = evilWormCoords[0]['x']
                position_y = evilWormCoords[0]['y']
                if evil_worm_direction == 'left' and position_x == 0:
                    if position_y == 0:
                        evil_worm_direction = UP
                        break
                    elif position_y == (CELLHEIGHT-1):
                        evil_worm_direction = DOWN
                        break
                    else:
                        evil_worm_direction = random.choice([UP, DOWN])
                        evil_worm_direction = directions_dict[evil_worm_direction]
                        break
                elif evil_worm_direction == 'right' and position_x == (CELLWIDTH-1):
                    if position_y == 0:
                        evil_worm_direction = UP
                        break
                    elif position_y == (CELLHEIGHT-1):
                        evil_worm_direction = DOWN
                        break
                    else:
                        evil_worm_direction = random.choice([UP, DOWN])
                        evil_worm_direction = directions_dict[evil_worm_direction]
                        break
                elif evil_worm_direction == 'up' and position_y == 0:
                    if position_x == 0:
                        evil_worm_direction = RIGHT
                        break
                    elif position_x == (CELLWIDTH-1):
                        evil_worm_direction = LEFT
                        break
                    else:
                        evil_worm_direction = random.choice([LEFT, RIGHT])
                        evil_worm_direction = directions_dict[evil_worm_direction]
                        break
                elif evil_worm_direction == 'down' and position_y == (CELLHEIGHT-1):
                    if position_x == 0:
                        evil_worm_direction = RIGHT
                        break
                    elif position_x == (CELLWIDTH-1):
                        evil_worm_direction = LEFT
                        break
                    else:
                        evil_worm_direction = random.choice([LEFT, RIGHT])
                        evil_worm_direction = directions_dict[evil_worm_direction]
                        break


                evil_worm_direction = directions_dict[evil_worm_direction]
                flag_direction = False

        jump_flag = False
        for wormBody in wormCoords:
            for wormBody2 in evilWormCoords:
                if wormBody['x'] == wormBody2['x'] and wormBody['y'] == wormBody2['y']:
                    jump_flag = True
                    break
            if jump_flag:
                break

        hit_flag = False
        for wormBody in evilWormCoords:
            if wormCoords[HEAD]['x'] == wormBody['x'] and wormCoords[HEAD]['y'] == wormBody['y']:
                hit_flag = True
                break


        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation()

        elif flag == 'shown' and jump_flag:
            if hit_flag:
                score_sub += 1
            else:
                del wormCoords[-1]

        elif flag == 'shown':
            del wormCoords[-1]
            del evilWormCoords[-1]

        else:
            del wormCoords[-1]

        # -----------------------------------------------------------------------------------

        #--------------------------------------------------------------> Changes for 2
        if wormCoords[HEAD]['x'] == point_element1['x'] and wormCoords[HEAD]['y'] == point_element1['y']:
            score_plu += 3
            point_element1 = getRandomLocation()

        elif wormCoords[HEAD]['x'] == point_element2['x'] and wormCoords[HEAD]['y'] == point_element2['y']:
            score_plu += 3
            point_element2 = getRandomLocation()
        #--------------------------------------------------------------------------------------------------

        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

        #----------------------------------------------------------------------------------> Changes for 1
        if flag == 'shown':
            if evil_worm_direction == UP:
                newEvilHead = {'x': evilWormCoords[evilWormHead]['x'], 'y': evilWormCoords[evilWormHead]['y'] - 1}
            elif evil_worm_direction == DOWN:
                newEvilHead = {'x': evilWormCoords[evilWormHead]['x'], 'y': evilWormCoords[evilWormHead]['y'] + 1}
            elif evil_worm_direction == LEFT:
                newEvilHead = {'x': evilWormCoords[evilWormHead]['x'] - 1, 'y': evilWormCoords[evilWormHead]['y']}
            elif evil_worm_direction == RIGHT:
                newEvilHead = {'x': evilWormCoords[evilWormHead]['x'] + 1, 'y': evilWormCoords[evilWormHead]['y']}
        # ----------------------------------------------------------------------------------------------


        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        #--------------------------------> Changes for 1
        if flag == 'shown':
            evilWormCoords.insert(0, newEvilHead)
            drawWorm(evilWormCoords, CRIMSON, CRIMSON_FLASH)
        #----------------------------------------------------

        #-------------------------------------> Changes for 2
        if flag_elements == 'shown':
            drawApple(point_element1, CARROT)

        if flag_elements2 == 'shown':
            drawApple(point_element2, CARROT)
        #-------------------------------------------------------------


        counter, start_ticks_worm, flag = drawEvilWorm(counter,
                                                       evil_worm_time,
                                                       start_ticks_worm,
                                                       flag)


        #---------------------------------------------------------> Changes for 2
        counter_elements, start_ticks_ele, flag_elements = drawElementsTime(counter_elements,
                                                                            five_sec_food,
                                                                            start_ticks_ele,
                                                                            flag_elements)

        counter_elements2, start_ticks_ele2, flag_elements2 = drawElementsTime(counter_elements2,
                                                                            seven_sec_food,
                                                                            start_ticks_ele2,
                                                                            flag_elements2)


        drawScore(len(wormCoords) - 3 - score_sub + score_plu*2)
        #------------------------------------------------------------------------------------------------

        pygame.display.update()
        FPSCLOCK.tick(FPS)


#--------------------------------------------------------------------------------> Changes for 1
def drawEvilWorm(counter, seconds, start_ticks, flag):
    if flag == 'hidden' and seconds == counter:
            counter = 20
            start_ticks = pygame.time.get_ticks()
            flag = 'shown'
            return counter, start_ticks, flag
    else:
        return counter, start_ticks, flag
#----------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------> Changes for 2
def drawElementsTime(counter, seconds, start_ticks, flag):
    if flag == 'hidden':
        if seconds == counter:
            counter = 5
            start_ticks = pygame.time.get_ticks()
            flag = 'shown'
            return counter, start_ticks, flag
        else:
            return counter, start_ticks, flag

    else:
        if seconds == counter:
            counter = 5
            start_ticks = pygame.time.get_ticks()
            flag = 'hidden'
            return counter, start_ticks, flag
        else:
            return counter, start_ticks, flag
#--------------------------------------------------------------------------------------------------------------------


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
    basicFont = pygame.font.Font('freesansbold.ttf', 40)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)
    #----------------------------------------------------------------------------> Changes for 3
    startSurf = basicFont.render('Start from the beginning', True, YELLOW)
    quitSurf = basicFont.render('Quit', True, YELLOW)
    startRect = startSurf.get_rect()
    quitRect = quitSurf.get_rect()

    startRect.midtop = (WINDOWWIDTH / 2, 320)
    quitRect.midtop = (WINDOWWIDTH / 2, 360)
    #------------------------------------------------------------------------------
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)

    DISPLAYSURF.blit(startSurf, startRect)
    DISPLAYSURF.blit(quitSurf, quitRect)

    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                if startRect.collidepoint(event.pos):
                    show_flag = False
                    main(show_flag)
                elif quitRect.collidepoint(event.pos):
                    terminate()
            if checkForKeyPress():
                pygame.event.get() # clear event queue
                return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords, colorOutside=DARKGREEN, colorIniside=GREEN):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, colorOutside, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, colorIniside, wormInnerSegmentRect)


def drawApple(coord, color=RED):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, color, appleRect)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()