import pygame, sys
from pygame.locals import *

#the number of frames per second
#can be changed to speed up or slow down the game!
FPS = 200
INCREASESPEED = 5

#global variable
WINDOWWIDTH= 400
WINDOWHEIGHT = 300
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20

#set up our cloours
BLACK   = (0  ,0  ,0  )
WHITE   = (255,255,255)
BLUE    = (0,191,255)

#this draws the arena in which the game is played.
def drawArena():
    DISPLAYSURF.fill((0,0,0))
    #draws the outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    #our center line
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH//2),0),((WINDOWWIDTH//2),WINDOWHEIGHT), (LINETHICKNESS//4))

#draw our paddles man!
def drawPaddle(paddle):
    #stops paddle from moving too low
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    #stops it from getting to high ;)
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS

    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

#time to draw the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)
#moves the ball and returns a new position
def moveBall(ball, ballDirX, ballDirY):
    ball.x += (ballDirX * INCREASESPEED)
    ball.y += (ballDirY * INCREASESPEED)
    return ball

def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
    if ball.left == (LINETHICKNESS) or ball.right == (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY

def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else:
        return 1

def checkPointScored(paddle1, ball, score, ballDirX):
    #resets points if the left wall is hit
    if ball.left == LINETHICKNESS:
        return 0
    #adds a point for hitting the ball.
    elif ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom:
        score += 1
        return score
    #adds 5 points for beating the other player
    elif ball.right == WINDOWWIDTH - LINETHICKNESS:
        score += 5
        return score
    else:
        return score
# AI of computer player
def artificialIntelligence(ball, ballDirX, paddle2):
    #centers paddle if ball is moving away from computer
    if ballDirX == -1:
        if paddle2.centery < (WINDOWHEIGHT//2):
            paddle2.y += INCREASESPEED
        elif paddle2.centery > (WINDOWHEIGHT//2):
            paddle2.y -= INCREASESPEED
    #makes the AI track the balls movements if its moving towards the computer
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += INCREASESPEED
        else:
            paddle2.y -= INCREASESPEED
    return paddle2

#displays the current score on screen
def displayScore(score):
    resultSurf = BASICFONT.render('score = %s' %(score), True, BLUE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft =(WINDOWWIDTH - 150, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)
#our main function.
def main():
    pygame.init()
    global DISPLAYSURF
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Jordans pong game. -_-')

    #set starting positions
    ballX = WINDOWWIDTH//2 - LINETHICKNESS//2
    ballY = WINDOWHEIGHT//2 - LINETHICKNESS//2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) //2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) //2
    score = 0
   
    #keeps track of the ball
    ballDirX = -1 # 1- = left 1 = right
    ballDirY = -1 # -1 = up 1 = down


    paddle1 = pygame.Rect(PADDLEOFFSET,playerOnePosition, LINETHICKNESS, PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS,PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    #draws arena

    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    pygame.mouse.set_visible(0)
    #main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey

        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        score = checkPointScored(paddle1, ball, score, ballDirX)
        ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
        paddle2 = artificialIntelligence (ball, ballDirX, paddle2)
        
        displayScore(score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()




