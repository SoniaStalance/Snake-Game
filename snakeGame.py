import pygame
import sys
import time
import random
import pathlib

pygame.init()

startgame=pygame.mixer.Sound('startgame.wav')
eat=pygame.mixer.Sound('eat.wav')
gameover=pygame.mixer.Sound('gameover.wav')
gamewin=pygame.mixer.Sound('gamewin.wav')

white = (250,250,250)
green = (10,150,0)
black = (0,0,0)
red   = (255,0,0)
yellow= (250,200,0)

font = pygame.font.SysFont(None, 50)

window_width = 800
window_height = 600

gameDisplay = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Snake Game')

blockSize = 20
clock = pygame.time.Clock()
FPS = 5


def snake(blockSize, snakelist):
    length = len(snakelist)
    color = black

    for size in snakelist:
        if length == 1:
            color = yellow
        else:
            color = black
        
        pygame.draw.rect(gameDisplay, color,[size[0] ,size[1] ,blockSize,blockSize])
        length -= 1
# end def snake


def message_to_screen(x,y, msg, color):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [x, y])
# end def message_to_screen

def generateRandomApple():
    randomAppleX = round(random.randrange(0, window_width-blockSize)/10.0)*10.0
    randomAppleY = round(random.randrange(0, window_height-blockSize)/10.0)*10.0
    return [randomAppleX,randomAppleY,blockSize,blockSize]
# end def generateRandomApple

def gameOver(score):
    winner = False

    # if score.txt doesn't exist then create it
    file = pathlib.Path("score.txt")
    if not (file.exists()):
        f = open('score.txt','w')
        f.write(str(0))
        f.close()

    f = open('score.txt','r')
    highScore=int(f.read())
    f.close()
    
    if score >= highScore:
        f = open('score.txt','w')
        f.write(str(score))
        f.close()
        winner = True
        pygame.mixer.Sound.play(gamewin)
    else:
        pygame.mixer.Sound.play(gameover)

    while True:
        gameDisplay.fill(green)
        message_to_screen(280,200,"GAME OVER",white)
        message_to_screen(120,250,"Press 'C' cont / 'Q' quit / 'R' reset",white)
        message_to_screen(280,300,"High Score "+str(highScore),(200,5,5))
        message_to_screen(280,350,"Your Score "+str(score),(150,5,5))
        if winner == True:
            message_to_screen(240,400,"Congratulations",white)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    f = open('score.txt', 'w')
                    f.write(str(0))
                    f.close()

                if event.key == pygame.K_q:
                    gameQuit()

                if event.key == pygame.K_c:
                    gameLoop()
# end def gameOver

def gameQuit():
    pygame.quit()
    sys.exit(0)
# end def gameQuit

def gameLoop():
    pygame.mixer.Sound.play(startgame)

    gameExit = False

    # starting x,y at center of screen
    lead_x = window_width/2
    lead_y = window_height/2

    change_pixels_of_x = 0
    change_pixels_of_y = 0

    snakelist = []
    snakeLength = 1
    score = 0

    # initial dimensions of apple (i.e. [x, y, l, b])
    dimensions = generateRandomApple()

    while not gameExit:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            # end if

            if event.type == pygame.KEYDOWN:

                leftArrow = event.key == pygame.K_LEFT
                rightArrow = event.key == pygame.K_RIGHT
                upArrow = event.key == pygame.K_UP
                downArrow = event.key == pygame.K_DOWN

                if leftArrow:
                    change_pixels_of_x = - blockSize
                    change_pixels_of_y = 0

                elif rightArrow:
                    change_pixels_of_x = blockSize
                    change_pixels_of_y = 0

                elif upArrow:
                    change_pixels_of_y = - blockSize
                    change_pixels_of_x = 0

                elif downArrow:
                    change_pixels_of_y = blockSize
                    change_pixels_of_x = 0
            # end if

            if lead_x >= window_width or lead_x < 0 or lead_y >= window_height or lead_y < 0:
                gameOver(score)
        # end for

        lead_x += change_pixels_of_x
        lead_y += change_pixels_of_y

        allspriteslist = []
        allspriteslist.append(lead_x)
        allspriteslist.append(lead_y)
        snakelist.append(allspriteslist)

        #maintains the no of units in snakelist, which should not excced length of snake
        if len(snakelist) > snakeLength:
            del snakelist[0]

        #if snake eats it's body, then game over    
        #segment is each unit of snake
        #allspriteslist has the posn of snake's head
        #therefore if any body unit(i.e segment)==posn.of head(i.e allspriteslist)
        #that indicates that the snake has bit its body

        gameDisplay.fill(green)
        pygame.draw.rect(gameDisplay, red, dimensions)
        snake(blockSize, snakelist)
        message_to_screen(740,20,str(score),white)
        pygame.display.update()

        if lead_x >= dimensions[0] and lead_x <= dimensions[0] + blockSize:
            if lead_y >= dimensions[1] and lead_y <= dimensions[1] + blockSize:
                dimensions = generateRandomApple()
                pygame.mixer.Sound.play(eat)
                snakeLength += 1
                score += 1
        
        #if snake eats it's body, then game over    
        #segment is each unit of snake
        #allspriteslist has the posn of snake's head
        #therefore if any body unit(i.e segment)==posn.of head(i.e allspriteslist)
        #that indicates that the snake has bit its body
        #if a snake goes backward in the same path, that means it has bit its head

        for segment in snakelist [:-1]:
            if segment == allspriteslist:
                gameOver(score) 

        clock.tick(FPS)
    # end while not gameExit

    # the following stmts exec when gameExit==True
    gameDisplay.fill(green)
    pygame.display.flip()
    gameQuit()
# end def gameLoop

# invoking gameLoop
gameLoop()