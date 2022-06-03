import pygame, pascalengine, math, os
from pascalengine.eventlistener import EventListener
from pascalengine.linedef import LineDef
from pascalengine.solidbspnode import SolidBSPNode
from pascalengine.camera import Camera
from pascalengine.textrendering import TextRendering
from pascalengine.texturerendering import Texture
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# ? MAP ROOM CONFIGURATIONS

# MAP ROOMS
# Lines, each vertex connects to the next one in CW fashion
# third element is direction its facing, when CW facing 1 = left
polygons = [
    
    # ? 1) HOUSE LAYOUT
    
    [
        [30, 30, 1, 9], #1
        [30, 80, 1, 9], #2
        [42.5, 80, 1, 9], #3
        [42.5, 90, 1, 9], #4
        [30, 90, 1, 9], #5
        [30, 110, 1 , 9], #6
        [52.5, 110, 1, 9], #7
        [52.5, 80, 1, 9], #8
        [57.5, 80, 1, 9], #9
        [57.5, 110, 1, 9], #10
        [80, 110, 1, 9], #11
        [80, 90, 1, 9], #12
        [67.5, 90, 1, 9], #13
        [67.5, 80, 1, 9], #14
        [80, 80, 1, 9], #15
        [80, 30, 1, 9] #16
    ],

]

# ? COLLISION DEFINITIONS

# Create SolidBSP for Level
allLineDefs = []
for i, v in enumerate(polygons):
    polygon = polygons[i]
    lineDefs = []
    for idx, val in enumerate(polygon):
        lineDef = LineDef()

        # first point, connect to second point
        if idx == 0:
            lineDef.asRoot(polygon[idx][0], polygon[idx][1], polygon[idx + 1][0], polygon[idx + 1][1], polygon[idx + 1][2], polygon[idx + 1][3])
            lineDefs.append(lineDef)
            allLineDefs.append(lineDef)

        # some point in the middle
        elif idx < len(polygon) - 1:
            lineDef.asChild(lineDefs[-1], polygon[idx + 1][0], polygon[idx + 1][1], polygon[idx + 1][2], polygon[idx + 1][3])
            lineDefs.append(lineDef)
            allLineDefs.append(lineDef)

        # final point, final line, connects back to first point
        elif idx == len(polygon) - 1:
            lineDef.asLeaf(lineDefs[-1], lineDefs[0], polygon[idx][2], polygon[idx][3])
            lineDefs.append(lineDef)
            allLineDefs.append(lineDef)

solidBsp = SolidBSPNode(allLineDefs)
print(solidBsp.toText(), flush=True)

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
icon = pygame.image.load("textures/tim.png")
pygame.display.set_icon(icon)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

glEnable(GL_BLEND) # allows for alpha transparency on color
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

listener = EventListener()
camera = Camera(solidBsp)

# ? set base camera application for matrix
glMatrixMode(GL_MODELVIEW) # set us into the 3d matrix
camera.setPosition(72, 2.5, 104)
camera.setYaw(-math.pi/2)

# ? RENDER MODE OPTIONS
mode = 0
max_modes = 4
collisionDetection = True
fullscreen = False

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
    
    # ! doesn't feel like working, return to later
    # worldPosition = camera.findWorldPos()
    # print(worldPosition)

    # if camera.lockFlight == False:
        
    #     worldPosition[1] = 2.5
    #     camera.setPosition(worldPosition[0], worldPosition[1], worldPosition[2])
    
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
    #pygame.mouse.set_visible(not fullscreen)
    #pygame.event.set_grab(fullscreen)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    # reapply window matrix
    glLoadMatrixf(m)
    
# ? await fullscreen key
listener.onKeyUp(pygame.K_f, on_f)

# ? move controls
listener.onKeyHold(pygame.K_a, camera.strafeLeft)
listener.onKeyHold(pygame.K_d, camera.strafeRight)
listener.onKeyHold(pygame.K_w, camera.moveForward)
listener.onKeyHold(pygame.K_s, camera.moveBackward)
listener.onMouseMove(camera.applyMouseMove)

# ? controls and info
print("m (mouselook)")
print("x (noclip)")
print("f (fullscreen)")
print("up_arrow (map mode up)")
print("down_arrow (map mode down)")
print("wasd (movement)", flush=True)

# ! TEXTURES! (NEED A BETTER PLACE FOR THIS)

Texture1=Texture("textures/wall.png")
Texture2=Texture("textures/carpet.png")
Texture3=Texture("textures/ceiling.png")

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
def drawHud(offsetX, offsetY, width, height, mode, camera, allLineDefs, walls):
    # wall lines
    # walls are position in with start and in in the x and z coordinates
    if mode == 0:
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
    if mode == 1:
        solidBsp.drawSegs(drawLine, offsetX, offsetY)
    if mode == 2:
        solidBsp.drawFaces(drawLine, camera.worldPos[0], camera.worldPos[2], offsetX, offsetY)
    if mode == 3:
        for wall in walls:
            start = [wall.start[0] + offsetX, wall.start[1] + offsetY];
            end = [wall.end[0] + offsetX, wall.end[1] + offsetY];
            drawLine(start, end, 1, 0, .3, 1, 1)

    # camera
    angleLength = 10
    camOrigin = [camera.worldPos[0] + offsetX, camera.worldPos[2] + offsetY] # mapX is worldX, mapY is worldZ
    camNeedle = [camOrigin[0] + math.cos(camera.yaw - math.pi/2) * angleLength, camOrigin[1] + math.sin(camera.yaw - math.pi/2) * angleLength]
    # yaw at 0 is straight down the positive z, which is down mapY
    # ? draw player on mini map
    drawLine(camOrigin, camNeedle, 1, 1, .5, 1, 1)
    drawPoint(camOrigin, 2, 1, 1, 1, 1)

    # ? render crosshair
    
    drawPoint([displayWidth/2, displayHeight/2 - 8], 3, 1, 1, 1, 1)
    
    # ? CURRENT COORDS
    TextRendering.drawText(0, 0, worldPosition, font, yellow)
    
    # ? NOCLIP TOGGLE INDICATOR
    if camera.collisionDetection:
        TextRendering.drawText(0, 20, "NOCLIP: OFF", font, yellow)
    else:
        TextRendering.drawText(0, 20, "NOCLIP: ON", font, yellow)
        
# ? define which walls are drawn
def drawWalls(walls, camera):
    for i, wall in enumerate(walls):
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,Texture1.texID)
        
        glBegin(GL_QUADS)
        # c = wall.drawColor
        # glColor3f(c[0]/255, c[1]/255, c[2]/255)
        
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
        
# ? placeholder texture and associated 3 vertices for testing purposes
def drawFloor(textures, camera):
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D,Texture2.texID)
        
    glBegin(GL_QUADS)
    
    glTexCoord2f(0.0,1.0)
    glVertex3f(80, 0, 110)
    
    glTexCoord2f(1.0,1.0)
    glVertex3f(30, 0, 110)
    
    glTexCoord2f(1.0,0.0)
    glVertex3f(30, 0, 30)
    
    glTexCoord2f(0.0,0.0)
    glVertex3f(80, 0, 30)
    
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
def drawCeiling(textures, camera):
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D,Texture3.texID)
        
    glBegin(GL_QUADS)
    
    glTexCoord2f(0.0,1.0)
    glVertex3f(80, 9, 110)
    
    glTexCoord2f(1.0,1.0)
    glVertex3f(30, 9, 110)
    
    glTexCoord2f(1.0,0.0)
    glVertex3f(30, 9, 30)
    
    glTexCoord2f(0.0,0.0)
    glVertex3f(80, 9, 30)
    
    glEnd()
    glDisable(GL_TEXTURE_2D)

# ? catch all update functions into one
def update():
    listener.update()
    camera.update()

# ? define everything to be drawn in the game
def draw():
    
    # sort walls around camera x and z
    walls = []
    textures = []
    solidBsp.getWallsSorted(camera.worldPos[0], camera.worldPos[2], walls)
    solidBsp.getTexturesSorted(camera.worldPos[0], camera.worldPos[2], textures) 

    # RENDER 3D
    glPushMatrix() # copies matrix below stack (in this case, our base camera matrix transformation)

    # projection
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, displayWidth, displayHeight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (displayWidth/displayHeight), 0.00001, 5000)
    # models
    glMatrixMode(GL_MODELVIEW) # set us into the 3d matrix

    # Cube(20, 0, 20)
    # Cube(-3, 3, 5)
    # Cube(0, 0, 10)
    # Cube(3, -3, 15)
    # Cube(0,0,0)

    drawWalls(walls, camera)
    drawFloor(textures, camera)
    drawCeiling(textures, camera)
    
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

    drawHud(20, 20, 400, 300, mode, camera, allLineDefs, walls)
    
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
    
    # ? drawing of everything in the game
    draw()
    
    drawCounter += 1

    actualTime = newTime # ms
