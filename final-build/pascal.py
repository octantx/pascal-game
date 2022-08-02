import pygame, pascalengine, math, os
from pascalengine.eventlistener import EventListener
from pascalengine.player import Camera
from pascalengine.spriterenderer import Text
from pascalengine.texturerenderer import Texture
from pascalengine.cube import Cube
from maps.levels import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

mapReturnees = createBSP(map0)
solidBsp = mapReturnees[0]
allLineDefs = mapReturnees[1]

# ! ------------------------------------------------------------------------------------------------------------------
def setup():
    pass

# ? GAME SETUP
pygame.init()
clock = pygame.time.Clock()

# ? get os resolution
displayInfo = pygame.display.Info()
resolutionWidth = displayInfo.current_w
resolutionHeight = displayInfo.current_h

# ? start with this resolution in windowed
targetWidth = 1280
targetHeight = 720

# ? FONT DECLARATION
font = pygame.font.SysFont('arial', 16)

# * colours!
yellow = (255, 255, 66, 255)

displayWidth = targetWidth
displayHeight = targetHeight

# ? PYGAME & OPENGL SETUPS

os.environ['SDL_VIDEO_CENTERED'] = '1' # center window on screen

screen = pygame.display.set_mode((displayWidth, displayHeight), DOUBLEBUF|OPENGL) # build window with opengl
pygame.display.set_caption("Pascal")
icon = pygame.image.load("final-build/assets/textures/tim.png")
pygame.display.set_icon(icon)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

glEnable(GL_BLEND) # allows for alpha transparency on color
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

listener = EventListener()
camera = Camera(solidBsp)
cubeclass = Cube()

# ? set base camera application for matrix
glMatrixMode(GL_MODELVIEW) # set us into the 3d matrix
camera.setPosition(72, 2, 104)
camera.setYaw(-math.pi/2)

# ? RENDER MODE OPTIONS
mode = 0
max_modes = 4
collisionDetection = True
fullscreen = False

# ! ------------------------------------------------------------------------------------------------------------------

# ? KEY OPERATIONS

# * change mode 1 up
def mode_up():
    global mode
    mode = (mode + 1) % max_modes
    
# ? await mode up key
listener.onKeyUp(pygame.K_UP, mode_up)

# * change mode 1 down
def mode_down():
    global mode
    mode = (mode - 1) % max_modes
    
# ? await mode up key
listener.onKeyUp(pygame.K_DOWN, mode_down)

# * define what happens when the x key is clicked (turns on noclip)
def on_x():
    global camera
    camera.collisionDetection = not camera.collisionDetection
    camera.lockFlight = not camera.lockFlight
    
# ? await x key
listener.onKeyUp(pygame.K_x, on_x)

# * define what happens when the f key is clicked (fullscreen or back to windowed)
def on_f():
    global fullscreen, screen, displayWidth, displayHeight
    global resolutionWidth, resolutionHeight, targetWidth, targetHeight
    fullscreen = not fullscreen
    # get world model matrix
    m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
    if fullscreen:
        displayWidth, displayHeight = resolutionWidth, resolutionHeight
        screen = pygame.display.set_mode((displayWidth,displayHeight), DOUBLEBUF|OPENGL|FULLSCREEN) # build window with opengl
    else:
        displayWidth, displayHeight = targetWidth, targetHeight
        screen = pygame.display.set_mode((displayWidth,displayHeight), DOUBLEBUF|OPENGL) # build window with opengl
    # if fullscreen take over mouse
    pygame.mouse.set_visible(not fullscreen)
    pygame.event.set_grab(fullscreen)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    # reapply window matrix
    glLoadMatrixf(m)
    
# ? await fullscreen key
listener.onKeyUp(pygame.K_f, on_f)

isDashing = False

def on_space():
    global isDashing
    if isDashing == False:
        isDashing = True
    else:
        isDashing = False

listener.onKeyUp(pygame.K_SPACE, on_space)

# ? move controls
listener.onKeyHold(pygame.K_a, camera.strafeLeft)
listener.onKeyHold(pygame.K_d, camera.strafeRight)
listener.onKeyHold(pygame.K_w, camera.moveForward)
listener.onKeyHold(pygame.K_s, camera.moveBackward)
listener.onMouseMove(camera.applyMouseMove)

# ! ------------------------------------------------------------------------------------------------------------------

# ? controls and info
print("x (noclip)")
print("f (fullscreen)")
print("up_arrow (map mode up)")
print("down_arrow (map mode down)")
print("wasd (movement)", flush=True)

# ! TEXTURES! (NEED A BETTER PLACE FOR THIS)

texturePath = "final-build/assets/textures/"

Texture1=Texture(texturePath + "placeholder.png")
Texture2=Texture(texturePath + "carpet.png")
Texture3=Texture(texturePath + "ceiling.png")

defaultInfo = [displayWidth, displayHeight, font, yellow, screen]

dialogue = False


# ! ------------------------------------------------------------------------------------------------------------------

# ? define how lines are drawn
def drawLine(start, end, width, r, g, b, a):
    glLineWidth(width)
    glColor4f(r, g, b, a)
    glBegin(GL_LINES)
    glVertex2f(start[0], start[1])
    glVertex2f(end[0], end[1])
    glEnd()

# ? define how points are drawn
def drawPoint(pos, radius, r, g, b, a):
    glColor4f(r, g, b, a)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(pos[0], pos[1]);
    for angle in range(10, 3610, 2):
        angle = angle / 10 # convert back down to degrees
        x2 = pos[0] + math.sin(angle) * radius;
        y2 = pos[1] + math.cos(angle) * radius;
        glVertex2f(x2, y2);
    glEnd()

# ? define how everything is drawn in the hud
def drawHud(offsetX, offsetY, width, height, mode, camera, allLineDefs, walls, enemies):
    # wall lines
    # walls are position in with start and in in the x and z coordinates
    if mode == 0:
        for wall in walls:
            start = [wall.start[0] + offsetX, wall.start[1] + offsetY];
            end = [wall.end[0] + offsetX, wall.end[1] + offsetY];
            drawLine(start, end, 1.5, 0, 1, 0.2, 1)
    if mode == 1:
        for lineDef in allLineDefs:
            # draw wall
            mapStart = [lineDef.start[0] + offsetX, lineDef.start[1] + offsetY]
            mapEnd = [lineDef.end[0] + offsetX, lineDef.end[1] + offsetY]
            drawLine(mapStart, mapEnd, 1, 0.0, 0.0, 1.0, 1.0)
            # draw facing dir
            ln = 7
            mx = lineDef.mid[0]
            my = lineDef.mid[1]
            nx = lineDef.normals[lineDef.facing][0] * ln
            ny = lineDef.normals[lineDef.facing][1] * ln
            if lineDef.facing == 1:
                drawLine([mx + offsetX, my + offsetY], [mx + nx + offsetX, my + ny + offsetY], 2, 0.0, 1.0, 1.0, 1.0)
            else:
                drawLine([mx + offsetX, my + offsetY], [mx + nx + offsetX, my + ny + offsetY], 2, 1.0, 0.0, 1.0, 1.0)
    if mode == 2:
        solidBsp.drawSegs(drawLine, offsetX, offsetY)
    if mode == 3:
        solidBsp.drawFaces(drawLine, camera.worldPos[0], camera.worldPos[2], offsetX, offsetY)
            
    for i, v in enumerate(enemies):
        
        drawPoint((enemies[i][0] + offsetX, enemies[i][1] + offsetY), 2, 1, 0, 0, 1)

    # camera
    angleLength = 10
    camOrigin = [camera.worldPos[0] + offsetX, camera.worldPos[2] + offsetY] # mapX is worldX, mapY is worldZ
    camNeedle = [camOrigin[0] + math.cos(camera.yaw - math.pi/2) * angleLength, camOrigin[1] + math.sin(camera.yaw - math.pi/2) * angleLength]
    # yaw at 0 is straight down the positive z, which is down mapY
    # ? draw player on mini map
    drawLine(camOrigin, camNeedle, 1, 1, .5, 1, 1)
    drawPoint(camOrigin, 2, 1, 1, 1, 1)
    
    # ? render crosshair
    drawLine([displayWidth/2, displayHeight/2-8], [displayWidth/2, displayHeight/2-2], 3, 0, 0, 0, 1)
    drawLine([displayWidth/2, displayHeight/2+2], [displayWidth/2, displayHeight/2+8], 3, 0, 0, 0, 1)
    drawLine([displayWidth/2-8, displayHeight/2], [displayWidth/2-2, displayHeight/2], 3, 0, 0, 0, 1)
    drawLine([displayWidth/2+2, displayHeight/2], [displayWidth/2+8, displayHeight/2], 3, 0, 0, 0, 1)

    drawLine([displayWidth/2, displayHeight/2-8], [displayWidth/2, displayHeight/2-2], 2, .3, 1, .3, 1)
    drawLine([displayWidth/2, displayHeight/2+2], [displayWidth/2, displayHeight/2+8], 2, .3, 1, .3, 1)
    drawLine([displayWidth/2-8, displayHeight/2], [displayWidth/2-2, displayHeight/2], 2, .3, 1, .3, 1)
    drawLine([displayWidth/2+2, displayHeight/2], [displayWidth/2+8, displayHeight/2], 2, .3, 1, .3, 1)
    
    # Text.drawImage('final-build/assets/textures/tim.png', defaultInfo)
    
    # Text.dialogue(0, "Hey welcome to ben, my namea jeff and i love to ben in the ben house! yeah oooo yeah and if you enter my house without entering the password i will have to beat you to death with a rock yeah yeah oh yeah yeah!", defaultInfo)

    if dialogue == True:
        Text.dialogue(0, "OH NO OH AH AH OH NO THE FDA ARE GOING TO! TO RAID MY HOUSE!", defaultInfo)

    # ? CURRENT COORDS
    Text.drawText(0, 0, worldPosition, font, yellow)
    
    # ? NOCLIP TOGGLE INDICATOR
    if camera.collisionDetection:
        Text.drawText(0, 20, "NOCLIP: OFF", font, yellow)
    else:
        Text.drawText(0, 20, "NOCLIP: ON", font, yellow)
        
    Text.drawText(0, 40, f"FPS: {currentFPS}", font, yellow)
    
    Text.drawText(0, 60, f"SPEED: {currentSpeed}", font, yellow)
    
    Text.drawText(0,80, str(var), font, yellow)
        
# ? define which walls are drawn
def drawWalls(walls):
    for i, wall in enumerate(walls):
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,Texture1.texID)
        
        glBegin(GL_QUADS)
        glColor3f(255, 0, 255)
        
        glTexCoord2f(1, 0)
        glVertex3f(wall.start[0],   0,              wall.start[1]) # low lef
        
        glTexCoord2f(1, 1)
        glVertex3f(wall.start[0],   wall.height,    wall.start[1]) # up lef
        
        glTexCoord2f(0, 1)
        glVertex3f(wall.end[0],     wall.height,    wall.end[1]) # up rig
        
        glTexCoord2f(0, 0)
        glVertex3f(wall.end[0],     0,              wall.end[1]) # up lef
        
        glEnd()
        glDisable(GL_TEXTURE_2D)
        
def drawEnemies(enemies):
    for i, enemy in enumerate(enemies):
        cubeclass.cubeDraw(enemies[i][0], 2, enemies[i][1], enemies[i][2])
        
# ? catch all update functions into one
def update():
    listener.update()
    camera.update()

# ? define everything to be drawn in the game
def draw():
    
    # sort walls around camera x and z
    walls = []
    solidBsp.getWallsSorted(camera.worldPos[0], camera.worldPos[2], walls)

    # RENDER 3D
    glPushMatrix() # copies matrix below stack (in this case, our base camera matrix transformation)

    # projection
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, displayWidth, displayHeight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, (displayWidth/displayHeight), 0.00001, 5000)
    # models
    glMatrixMode(GL_MODELVIEW) # set us into the 3d matrix

    drawWalls(walls)
    drawEnemies(map0enemies)

    glPopMatrix()
    # END 3D

    # RENDER 2D - reference this: https://stackoverflow.com/questions/43130842/python-opengl-issues-displaying-2d-graphics-over-a-3d-scene
    glPushMatrix()

    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, displayWidth, displayHeight, 0.0)
    
    # models
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    drawHud(20, 20, 400, 300, mode, camera, allLineDefs, walls, map0enemies)
    # Text.dialogue(0, "your mother is particularly good looking", defaultInfo)
    
    glPopMatrix()
    # END 2D

    # update display
    pygame.display.flip() # buffer swap

timer = 0
actualTime = pygame.time.get_ticks() # ms
FPS = 60
dt = int(1 / FPS * 1000) # 60 fps in ms
updateCounter = 0
drawCounter = 0
var = 0
dashLength = 5
# ? game loop
while True:

    # UPDATE at fixed intervals
    newTime = pygame.time.get_ticks() # ms
    frameTime = newTime - actualTime
    
    if frameTime > 250:
        frameTime = 250 # avoid spiral of death
        
    timer += frameTime
    
    while timer >= dt:
        update()
        updateCounter += 1
        timer -= dt
        
    # ? WORLD POSITION
    worldPosition = str(camera.worldPos)
    
    # ? fps
    clock.tick(FPS)
    currentFPS = str(round(clock.get_fps()))
    
    # # ? speed 
    currentSpeed = str(camera.moveSpeed)
    
    if isDashing:
        var = var + 1
        while var < dashLength:
            camera.moveSpeed = 2
            break
        if var > dashLength:
            camera.moveSpeed = .65
            var = 0
            isDashing = False
    
    # ? drawing of everything in the game
    draw()
    
    drawCounter += 1

    actualTime = newTime # ms
    
    # glRotatef(0.01, 5, 0.1, 0.1)
    
