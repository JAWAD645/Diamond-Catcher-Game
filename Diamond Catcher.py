from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random 

catcherX = 250  
catcherY = 30  
diamondX = random.randint(50, 350) 
diamondY = 600 
diamondStop = False
BackButtonChk = False
PlayButtonChk = False
PauseButtonChk = False
CrossButtonChk = False
gameScore = 0 
fallingSpeed = 1
paused = False  # NEW pause flag


# MAIN MID POINT ALGORITHM
def MidPointLine(zone, x1, y1, x2, y2): 
    dx = (x2-x1)
    dy = (y2-y1)
    x = x1
    y = y1

    dInitial = 2*dy - dx
    
    Del_E = 2*dy
    Del_NE = 2*(dy-dx)

    while x <= x2:
        a, b = ConvertToOriginal(zone, x, y)  
        drawpoints(a, b)

        if dInitial <= 0:
            x = x + 1
            dInitial = dInitial + Del_E
        else:
            x = x + 1
            y = y + 1
            dInitial = dInitial + Del_NE


def FindZone(x1, y1, x2, y2):  
    dx = (x2-x1)
    dy = (y2-y1)

    if abs(dx) > abs(dy):   
        if dx > 0 and dy > 0:
            return 0
        elif dx < 0 and dy > 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:                   
        if dx > 0 and dy > 0:
            return 1
        elif dx < 0 and dy > 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6


def ConvertToZoneZero(zone, x, y): 
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def ConvertToOriginal(zone, x, y): 
    if zone == 0:
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return -y, -x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return y, -x
    if zone == 7:
        return x, -y


def DrawLine(x1, y1, x2, y2): 
    zone = FindZone(x1, y1, x2, y2)
    x1, y1 = ConvertToZoneZero(zone, x1, y1)
    x2, y2 = ConvertToZoneZero(zone, x2, y2)
    MidPointLine(zone, x1, y1, x2, y2)


# DRAWING THE CATCHER AND DIAMOND
def catcher():
    glColor3f(0.7, 0.2, 1)
    DrawLine(catcherX - 40, catcherY, catcherX + 40, catcherY)  
    DrawLine(catcherX - 40, catcherY, catcherX - 30, catcherY - 20)  
    DrawLine(catcherX + 40, catcherY, catcherX + 30, catcherY - 20)  
    DrawLine(catcherX - 30, catcherY - 20, catcherX + 30, catcherY - 20)  


def diamond():
    global diamondX, diamondY, catcherX, catcherY 
    global fallingSpeed, gameScore, diamondStop, paused

    if paused:
        return  # stop movement when paused

    DrawLine(diamondX, diamondY, diamondX + 5, diamondY - 10)  
    DrawLine(diamondX, diamondY, diamondX - 5, diamondY - 10)  
    DrawLine(diamondX - 5, diamondY - 10, diamondX, diamondY - 20)
    DrawLine(diamondX, diamondY - 20, diamondX + 5, diamondY - 10)
    diamondY -= fallingSpeed

    if (diamondY - 20 < catcherY and catcherX - 50 <= diamondX <= catcherX + 50): 
        diamondX = random.randint(100, 350) 
        diamondY = 600
        gameScore += 1
        fallingSpeed += 0.3
        print("Game Score: ", gameScore)
    elif diamondY - 20 < 0: 
        fallingSpeed = 0
        diamondY = 20 
        totalScore = gameScore
        gameScore = 0 
        diamondStop = True
        print("=============================")
        print("Game Over!")
        print("Your Total Score: ", totalScore)


# BUTTON DRAWING
def play_button():
    DrawLine(200, 580, 220, 570)  
    DrawLine(200, 560, 220, 570)
    DrawLine(200, 560, 200, 580)
    
def back_button():
    DrawLine(10, 570, 30, 570) 
    DrawLine(10, 570, 20, 580)
    DrawLine(10, 570, 20, 560)

def cross_button():
    DrawLine(390, 580, 370, 560) 
    DrawLine(370, 580, 390, 560)


# KEYBOARD AND MOUSE CONTROL
def specialKeyboardListener(key, x, y): 
    global catcherX, paused
    if paused:
        return  # no movement if paused
    if key == GLUT_KEY_LEFT:
        catcherX -= 10
    elif key == GLUT_KEY_RIGHT:
        catcherX += 10
    catcherX = max(45, min(360, catcherX))  


def mouseListener(button, state, x, y): 
    global BackButtonChk, CrossButtonChk, PlayButtonChk, paused

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 10 <= x <= 30 and (600-580) <= y <= (600-560):  # Back button
            BackButtonChk = True
            resetGame()
            print("Starting Over")
        elif 370 <= x <= 390 and (600-580) <= y <= (600-560):  # Cross button
            CrossButtonChk = True
            print(f"Goodbye. Final Score: {gameScore}")
            glutLeaveMainLoop()
        elif 200 <= x <= 220 and (600-580) <= y <= (600-560):  # Play/Pause button
            paused = not paused  # toggle
            PlayButtonChk = True


# TIMER FOR 60 FPS
def timer(value): 
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0) 


def drawpoints(x, y): 
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def iterate(): 
    glViewport(0, 0, 400, 600)
    glOrtho(0.0, 400, 0.0, 600, 0.0, 1.0) 
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)


def display(): 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    glColor3f(1, 1, 1)
    catcher()

    global diamondStop, paused
    if diamondStop:
        glColor3f(1, 0, 0)
        diamond()
    else:
        glColor3f(1, 1, 0)
        diamond()

    # Back button (bright teal)
    glColor3f(0, 1, 1)
    back_button()

    # Cross button (red)
    glColor3f(1, 0, 0)
    cross_button()

    # Play/Pause button (amber)
    glColor3f(1.0, 0.75, 0.0)
    if paused:
        play_button()
    else:
        DrawLine(200, 580, 200, 560)  # pause bar 1
        DrawLine(210, 580, 210, 560)  # pause bar 2

    glutSwapBuffers()


def resetGame():
    global catcherX, catcherY, diamondX, diamondY, fallingSpeed, diamondStop, paused, gameScore
    catcherX = 250
    catcherY = 30
    diamondX = random.randint(50, 350)
    diamondY = 600
    fallingSpeed = 1
    diamondStop = False
    paused = False
    gameScore = 0


# GLUT setup
glutInit() 
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(400, 600) 
glutInitWindowPosition(1000, 250) 

wind = glutCreateWindow(b"Diamond Catcher Game")
glutTimerFunc(0, timer, 0)   
glutMouseFunc(mouseListener) 
glutSpecialFunc(specialKeyboardListener)
glutDisplayFunc(display)
glutMainLoop()
