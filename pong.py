import pygame, sys
from pygame.locals import *

#the number of frames per second
#can be changed to speed up or slow down the game!
FPS = 200

#global variable
WINDOWWIDTH= 400
WINDOWHEIGHT = 300
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20

#set up our cloours
BLACK   = (0  ,0  ,0  )
WHITE   = (255,255,255)

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
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
    if ball.left == (LINETHICKNESS) or ball.right == (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY

#our main function.
def main():
    pygame.init()
    global DISPLAYSURF

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Jordans pong game. -_-')

    #set starting positions
    ballX = WINDOWWIDTH//2 - LINETHICKNESS//2
    ballY = WINDOWHEIGHT//2 - LINETHICKNESS//2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) //2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) //2
   
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
    #main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()




