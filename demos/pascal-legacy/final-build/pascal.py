import pygame, pascalengine, math, os, random, sys
from pascalengine.eventlistener import EventListener
from pascalengine.player import Camera
from pascalengine.spriterenderer import Text
from pascalengine.texturerenderer import Texture
from pascalengine.cube import Cube
from pascalengine.math import *
from maps.levels import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

mapReturnees = createBSP(map)
mapSolidBsp = mapReturnees[0]
mapAllLineDefs = mapReturnees[1]
mapAliveCubes = mapEnemies.copy()

# ! ------------------------------------------------------------------------------------------------------------------
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
debugFont = pygame.font.SysFont('comic sans ms', 16)
announcerFont = pygame.font.SysFont('georgia', 65)
introFont = pygame.font.SysFont('georgia', 200)
subtitleFont = pygame.font.SysFont('georgia', 28)
counterFont = pygame.font.SysFont('jeff', 65)

# * colours!
yellow = (255, 255, 66, 255)
red = (255, 0, 0, 255)
green = (0, 255, 0, 255)
purpleish = (218, 112, 214)
white = (255, 255, 255, 255)
grey = (200, 200, 200, 255)

displayWidth = targetWidth
displayHeight = targetHeight

# ? PYGAME & OPENGL SETUPS

os.environ['SDL_VIDEO_CENTERED'] = '1' # center window on screen

screen = pygame.display.set_mode((displayWidth, displayHeight), DOUBLEBUF|OPENGL) # build window with opengl
pygame.display.set_caption("Pascal")
icon = pygame.image.load("assets/textures/tim.png")
pygame.display.set_icon(icon)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

glEnable(GL_BLEND) # allows for alpha transparency on color
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

listener = EventListener()
camera = Camera(mapSolidBsp)
cubeclass = Cube()

# ? set base camera application for matrix
glMatrixMode(GL_MODELVIEW) # set us into the 3d matrix
camera.setPosition(75, 2, 60)

camera.setYaw(-math.pi/2)

# ? RENDER MODE OPTIONS
mode = 0
max_modes = 4
collisionDetection = True
fullscreen = False

# ! ------------------------------------------------------------------------------------------------------------------

# ? KEY OPERATIONS

# * define what happens when the v key is clicked (turns on noclip)
def on_v():
    global camera
    camera.collisionDetection = not camera.collisionDetection
    camera.lockFlight = not camera.lockFlight
    
# ? await v key
listener.onKeyUp(pygame.K_v, on_v)

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

listener.onKeyDown(pygame.K_SPACE, on_space)

def on_r():
    global restart
    if ableToRestart:
        restart = True
    
listener.onKeyDown(pygame.K_r, on_r)
    
def on_c():
    global debug
    if not debug:
        debug = True
    else:
        debug = False

listener.onKeyDown(pygame.K_c, on_c)

def on_x():
    global fpsTog
    fpsTog = not fpsTog

listener.onKeyDown(pygame.K_x, on_x)

def on_k():
    global sammich
    if introSequence:
        sammich = True
        
listener.onKeyDown(pygame.K_k, on_k)

# ? move controls
listener.onKeyHold(pygame.K_a, camera.strafeLeft)
listener.onKeyHold(pygame.K_d, camera.strafeRight)
listener.onKeyHold(pygame.K_w, camera.moveForward)
listener.onKeyHold(pygame.K_s, camera.moveBackward)
listener.onMouseMove(camera.applyMouseMove)

# ! ------------------------------------------------------------------------------------------------------------------

# ! textures and sounds

texturePath = "assets/textures/"
soundPath = "assets/sound/"

Texture1=Texture(texturePath + "bones.png")
Texture2=Texture(texturePath + "voidwalls.png")
Texture3=Texture(texturePath + "sandwich.png")

hit01Sound = pygame.mixer.Sound(soundPath + "hit01.wav")
hit02Sound = pygame.mixer.Sound(soundPath + "hit02.wav")
hit03Sound = pygame.mixer.Sound(soundPath + "hit03.wav")
impactSound = pygame.mixer.Sound(soundPath + "impact.wav")

ambienceSound = pygame.mixer.Sound(soundPath + "ambience.wav")
mainSound = pygame.mixer.Sound(soundPath + "main.wav")

def impact():
    pygame.mixer.Sound.play(impactSound)

defaultInfo = [displayWidth, displayHeight, debugFont, green, screen]

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
    
    if debug:
        for wall in walls:
            start = [wall.start[0] + offsetX, wall.start[1] + offsetY];
            end = [wall.end[0] + offsetX, wall.end[1] + offsetY];
            drawLine(start, end, 1.5, 0, 1, 0.2, 1)


        # camera
        angleLength = 10
        camOrigin = [camera.worldPos[0] + offsetX, camera.worldPos[2] + offsetY] # mapX is worldX, mapY is worldZ
        camNeedle = [camOrigin[0] + math.cos(camera.yaw - math.pi/2) * angleLength, camOrigin[1] + math.sin(camera.yaw - math.pi/2) * angleLength]
        # yaw at 0 is straight down the positive z, which is down mapY
        # ? draw player on mini map
        drawLine(camOrigin, camNeedle, 1, 1, .5, 1, 1)
        drawPoint(camOrigin, 2, 1, 1, 1, 1)
    
    if crosshairCheck:
    
        # ? render crosshair
        drawLine([displayWidth/2, displayHeight/2-8], [displayWidth/2, displayHeight/2-2], 3, 0, 0, 0, 1)
        drawLine([displayWidth/2, displayHeight/2+2], [displayWidth/2, displayHeight/2+8], 3, 0, 0, 0, 1)
        drawLine([displayWidth/2-8, displayHeight/2], [displayWidth/2-2, displayHeight/2], 3, 0, 0, 0, 1)
        drawLine([displayWidth/2+2, displayHeight/2], [displayWidth/2+8, displayHeight/2], 3, 0, 0, 0, 1)

        drawLine([displayWidth/2, displayHeight/2-8], [displayWidth/2, displayHeight/2-2], 2, .3, 1, .3, 1)
        drawLine([displayWidth/2, displayHeight/2+2], [displayWidth/2, displayHeight/2+8], 2, .3, 1, .3, 1)
        drawLine([displayWidth/2-8, displayHeight/2], [displayWidth/2-2, displayHeight/2], 2, .3, 1, .3, 1)
        drawLine([displayWidth/2+2, displayHeight/2], [displayWidth/2+8, displayHeight/2], 2, .3, 1, .3, 1)

    if debug:
        # ? CURRENT COORDS
        Text.drawText(0, 0, worldPosition, debugFont, green)
        
        # ? NOCLIP TOGGLE INDICATOR
        if camera.collisionDetection:
            Text.drawText(0, 20, "NOCLIP: OFF", debugFont, green)
        else:
            Text.drawText(0, 20, "NOCLIP: ON", debugFont, green)
            
        Text.drawText(0, 40, f"FPS: {currentFPS}", debugFont, green)

        # ! drawing enemies, taken out because it caused crazy fps drops
        for i, v in enumerate(enemies):
            
            drawPoint((enemies[i][0] + offsetX, enemies[i][1] + offsetY), 2, 1, 0, 0, 1)
            
    else:
        if fpsTog:
            Text.drawText(0, 0, f"FPS: {currentFPS}", debugFont, green)
        
        
# ? define which walls are drawn
def drawWalls(walls):
    for i, wall in enumerate(walls):
        
        glEnable(GL_TEXTURE_2D)
    
        glBegin(GL_QUADS)

        c = wall.drawColor
        # glColor3f(255, 255, 255)
        glColor3f(c[0]/(scoreStreak*1.25), c[1]/255, c[2]/(scoreStreak*1.25))
        
        if scoreStreak < 20 or scoreStreak > 40:
            glTexCoord2f(1, 0)
        glVertex3f(wall.start[0],   0,              wall.start[1]) # low lef
        
        if scoreStreak < 40 or scoreStreak > 80:
            glTexCoord2f(1, 1)
        glVertex3f(wall.start[0],   wall.height,    wall.start[1]) # up lef
        
        if scoreStreak < 40 or scoreStreak > 80:
            glTexCoord2f(0, 1)
        glVertex3f(wall.end[0],     wall.height,    wall.end[1]) # up rig
        
        if scoreStreak < 80:
            glTexCoord2f(0, 0)
        glVertex3f(wall.end[0],     0,              wall.end[1]) # up lef
        
        glEnd()
        glDisable(GL_TEXTURE_2D)
        
def drawEnemies(enemies):
    for i, enemy in enumerate(enemies):
        cubeclass.cubeDraw(enemies[i][0], 1.4, enemies[i][1], enemies[i][2])
        
# ? catch all update functions into one
def update():
    listener.update()
    camera.update()

# ? define everything to be drawn in the game
def draw():
    
    # sort walls around camera x and z
    walls = []
    mapSolidBsp.getWallsSorted(camera.worldPos[0], camera.worldPos[2], walls)

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
    drawEnemies(mapAliveCubes)

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

    drawHud(20, 20, 400, 300, mode, camera, mapAllLineDefs, walls, mapAliveCubes)
    
    # ? titles:

    if againCheck:
        Text.drawText(displayWidth/2-98, displayHeight/2+100, "AGAIN", announcerFont, white)
    if not restartToolTipDone:
        if restartToolTipCheck:
            Text.drawText(displayWidth/2-65, displayHeight/2+60, "R to Restart", subtitleFont, grey)
    
    if acclimateAnnouncerCheck:
        Text.drawText(displayWidth/2-182, displayHeight/2+100, "ACCLIMATE", announcerFont, white)
    if acclimateSubtitleCheck:
        Text.drawText(displayWidth/2-87, displayHeight/2+60, "WASD to Move", subtitleFont, grey)
        Text.drawText(displayWidth/2-82, displayHeight/2+177, "Mouse to Look", subtitleFont, grey)
        
    if assimilateAnnouncerCheck:
        Text.drawText(displayWidth/2-182, displayHeight/2+100, "ASSIMILATE", announcerFont, white)
    if assimilateSubtitleCheck:
        Text.drawText(displayWidth/2-158, displayHeight/2+60, "Space to Dash while Moving", subtitleFont, grey)
        
    if repeatAnnouncerCheck:
        if sammich:
            Text.drawText(displayWidth/2-55, displayHeight/2+100, "EAT", announcerFont, white)
        else:
            Text.drawText(displayWidth/2-120, displayHeight/2+100, "REPEAT", announcerFont, white)
            
    if repeatSubtitleCheck:
        Text.drawText(displayWidth/2-95, displayHeight/2+60, "Destroy them all", subtitleFont, grey)
        
    if levelTimer:
        Text.drawText(displayWidth/2-17, displayHeight/2+295, str(levelTime), counterFont, purpleish)
        
    if scoreShow:
        Text.drawText(0, displayHeight-50, str(score), counterFont, green)
    if streakShow:
        Text.drawText(displayWidth-50, displayHeight-50, str(scoreStreak-1), counterFont, red)
        
    if pascalTitleCheck:
        Text.drawText(displayWidth/2-373, displayHeight/2-100, "PASCAL", introFont, purpleish)
        Text.drawText(displayWidth/2-50, displayHeight/2-180, str(score), counterFont, green) 
        Text.drawText(displayWidth/2, displayHeight/2-225, str(scoreStreak-1), counterFont, red) 
        
    if resetTitleCheck:
        Text.drawText(displayWidth/2-310, displayHeight/2-100, "RESET", introFont, purpleish)
        Text.drawText(displayWidth/2-36, displayHeight/2-180, str(score), counterFont, green) 
        Text.drawText(displayWidth/2, displayHeight/2-225, str(scoreStreak-1), counterFont, red) 
        
    if decimateAnnouncerCheck:
        Text.drawText(displayWidth/2-160, displayHeight/2+100, titles[randTitle], announcerFont, white)
    
    glPopMatrix()
    # END 2D

    # update display
    pygame.display.flip() # buffer swap

# ? game checks
debug = False
fpsTog = False
musicPlayedCheck = False
ambiencePlayedCheck = False
scoreShow = False
streakShow = False

restart = False
againCheck = False
restartToolTipCheck = False
restartToolTipDone = False
ableToRestart = False

introSequence = True
sammich = False
acclimateAnnouncerCheck = False
acclimateSubtitleCheck = False
assimilateAnnouncerCheck = False
assimilateSubtitleCheck = False
introSequenceComplete = False
repeatAnnouncerCheck = False
crosshairCheck = False

introLevel = False
levelTimer = False
repeatSubtitleCheck = False
introLevelComplete = False
pascalTitleCheck = False
introLevelSequenceComplete = False

secondLevel = False
secondLevelTimer = False
decimateAnnouncerCheck = False
secondLevelComplete = False
resetTitleCheck = False
secondLevelSequenceComplete = False

# ? -----------------------

glBindTexture(GL_TEXTURE_2D, Texture2.texID)

# ? -----------------------

titles = [
    "DECIMATE",
    "DESTROY",
    "ASSIMILATE",
    "ANNIHILIATE",
    "FOREVER",
    "DESOLATE",
    "DEVESTATE",
    "PULVERIZE",
    "VAPORIZE"
]

currentMoveSpeed = 0

score = 0
scoreStreak = 1
scoreMultiplier = 1
scorePunisher = 0
timer = 0
counter = 0
againCounter = 0
timeToTeleport = 0
timeToTeleportCheck = False

levelTime = 7

introCounter = 0
introLevelCounter = 0
introLevelCounter2 = 0

secondLevelCounter = 0
secondLevelCounter2 = 0

marginCount = 0
actualTime = pygame.time.get_ticks() # ms
FPS = 60
dt = int(1 / FPS * 1000) # 60 fps in ms
updateCounter = 0
drawCounter = 0

dashSpeedCount = 0
dashLengthCount = 0
dashSpeedLength = 4.5
dashLength = 8
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
    
    # ? speed 
    currentSpeed = str(camera.moveSpeed)
    
    # ? dash:
    referencePos = camera.worldPos.copy()
    referencePos.pop(1)
    total = len(referencePos)

    for idx, v, in enumerate(mapAliveCubes):
        for i in range(total):
            if abs(referencePos[i] - mapAliveCubes[idx][i]) > 2:
                marginCount += 1
                
        if total > 0:
            margin = marginCount / total
            marginCount = 0
        else:
            margin = 1.0
            marginCount = 0
            
        if round(referencePos[0]) == mapAliveCubes[idx][0] and round(referencePos[1]) == mapAliveCubes[idx][1] or margin < .30:
            if isDashing:
                mapAliveCubes.pop(idx)
                score += round(100 * scoreMultiplier + (scoreStreak * 5))
                scoreStreak += 1
                
                whichHit = random.randint(0,2)
                
                if whichHit == 0:
                    pygame.mixer.Sound.play(hit01Sound)
                if whichHit == 1:
                    pygame.mixer.Sound.play(hit02Sound)
                if whichHit == 2:
                    pygame.mixer.Sound.play(hit03Sound)
                    
            elif introSequence:
                pass
            else:
                restart = True
                score -= (50 + scorePunisher)
                scoreStreak = 1

    if isDashing:
        
        dashSpeedCount += 1
        dashLengthCount += 1
        while dashSpeedCount < dashSpeedLength:
            camera.moveSpeed = 2 + currentMoveSpeed
            break
        if dashSpeedCount > dashSpeedLength:
            camera.moveSpeed = .7 + currentMoveSpeed
        if dashLengthCount > dashLength:
            
                
            dashSpeedCount = 0
            dashLengthCount = 0
            isDashing = False 

    # ? time it took to complete level and time remaining in the level
    if introSequence:
        introCounter += 1
        
        if ambiencePlayedCheck == False:
            pygame.mixer.Sound.play(ambienceSound)
            ambiencePlayedCheck = True

        if introCounter == toFps(2):
            acclimateAnnouncerCheck = True
            impact()

        if introCounter == toFps(3):
            acclimateSubtitleCheck = True
        
        if introCounter == toFps(7):
            acclimateAnnouncerCheck = False
            acclimateSubtitleCheck = False
            
        if introCounter == toFps(9):
            assimilateAnnouncerCheck = True
            impact()
        
        if introCounter == toFps(10):
            assimilateSubtitleCheck = True
            mapAliveCubes[0][2] = 'r'
            crosshairCheck = True

        if mapAliveCubes[0][3] != 0:
            mapEnemies.pop(0)
            pygame.mixer.Sound.stop(ambienceSound)
            assimilateAnnouncerCheck = False
            assimilateSubtitleCheck = False
            acclimateAnnouncerCheck = False
            acclimateSubtitleCheck = False
            introSequenceComplete = True
            repeatAnnouncerCheck = True
            impact()
            crosshairCheck = True
            introLevel = True
            scoreShow = True
            streakShow = True
            intLevelPosChange = True
            introSequence = False
            
    if introLevel:
        
        if musicPlayedCheck == False:
            pygame.mixer.Sound.play(mainSound)
            musicPlayedCheck = True
        
        ableToRestart = True
        
        if sammich:
            glBindTexture(GL_TEXTURE_2D, Texture3.texID)
        else:
            glBindTexture(GL_TEXTURE_2D, Texture1.texID)
        
        introLevelCounter += 1
        
        if intLevelPosChange:
            map.pop(0)
            camera.toPosition(125.6, 197)
            camera.setYaw(math.pi/2)
            intLevelPosChange = False
        
        # ? restart logic, intro level
        
        if introLevelCounter == toFps(1):
            
            repeatSubtitleCheck = True
            
        if introLevelCounter == toFps(3):
            
            repeatAnnouncerCheck = False
            repeatSubtitleCheck = False

        if not introLevelComplete:
            if not levelTimer:
                levelTimer = True
        
        endCubeCheck = []
        for i, v in enumerate(mapAliveCubes):
            if mapAliveCubes[i][3] != 5:
                endCubeCheck.append(False)
            else:
                endCubeCheck.append(True)
        
        if True not in endCubeCheck:
            introLevelComplete = True
            endCubeCheck.clear()
            
        if introLevelComplete and not introLevelSequenceComplete:
            
            scoreShow = False
            streakShow = False
            decimateAnnouncerCheck = False
            pascalTitleCheck = True
            impact()
            camera.toPosition(900, 900000)
            crosshairCheck = False
            levelTimer = False
            repeatAnnouncerCheck = False
            repeatSubtitleCheck = False
            againCheck = False
            restartToolTipCheck = False
            timeToTeleportCheck = True
            introLevelSequenceComplete = True
            
        if timeToTeleportCheck:
            timeToTeleport += 1
        
        if timeToTeleport == toFps(2) and introLevelComplete:
            camera.toPosition(202, 107)
            
            if random.randint(1, 500) == 500:
                sammich == True
                
            timeToTeleportCheck = False
            timeToTeleport = 0
            score += levelTime * 100
            pascalTitleCheck = False
            secondLevel = True
            secondLevelSequenceComplete = False
            secondLevelComplete = False
            introLevel = False
            
            levelTime = 5
            levelTimer = True
            scoreShow = True
            streakShow = True

            randTitle = random.randint(0,8)
            decimateAnnouncerCheck = True
            crosshairCheck = True
            
        if levelTimer:
            introLevelCounter2 += 1
            if introLevelCounter2 == toFps(1):
                if levelTime != 0:
                    levelTime -= 1
                else:
                    restart = True
                introLevelCounter2 = 0
        
        if restart:
            camera.toPosition(125.6, 197)
            mapAliveCubes = mapEnemies.copy()
            levelTime = 7

            againCheck = True
            repeatAnnouncerCheck = False
            repeatSubtitleCheck = False
            restart = False
            
        if againCheck:
            
            repeatSubtitleCheck = False
            decimateAnnouncerCheck = False
            
            againCounter += 1
            if againCounter == toFps(1):
                restartToolTipCheck = True
            if againCounter == toFps(3):
                restartToolTipDone = True
                restartToolTipCheck = False
                againCheck = False
                againCounter = 0
                
    if secondLevel:
        
        if sammich:
            glBindTexture(GL_TEXTURE_2D, Texture3.texID)
        else:
            glBindTexture(GL_TEXTURE_2D, Texture1.texID)
        
        secondLevelCounter += 1
        
        if secondLevelCounter == toFps(2):
            decimateAnnouncerCheck = False
        
        endCubeCheck = []
        for i, v in enumerate(mapAliveCubes):
            if mapAliveCubes[i][3] != 11:
                endCubeCheck.append(False)
            else:
                endCubeCheck.append(True)
        
        if True not in endCubeCheck:
            secondLevelComplete = True
            endCubeCheck.clear()
            
        if secondLevelComplete and not secondLevelSequenceComplete:
            
            resetTitleCheck = True
            decimateAnnouncerCheck = False

            impact()
            camera.toPosition(900, 900000)
            crosshairCheck = False
            levelTimer = False
            scoreShow = False
            streakShow = False
            decimateAnnouncerCheck = False
            againCheck = False
            restartToolTipCheck = False
            timeToTeleportCheck = True
            secondLevelSequenceComplete = True
            
        if timeToTeleportCheck:
            timeToTeleport += 1
        
        if timeToTeleport == toFps(2) and secondLevelComplete:
            camera.toPosition(125.6, 197)
            currentMoveSpeed += .025
            scoreMultiplier += .25
            scorePunisher += 100
            
            if random.randint(1, 500) == 500:
                sammich == True
                
            camera.setYaw(math.pi)
            mapAliveCubes = mapEnemies.copy()
                
            timeToTeleportCheck = False
            timeToTeleport = 0
            resetTitleCheck = False # * replace
            introLevel = True
            introLevelComplete = False
            introLevelSequenceComplete = False
            secondLevel = False
            randTitle = random.randint(0,8)
            decimateAnnouncerCheck = True
            
            levelTime = 7
            levelTimer = True
            scoreShow = True
            streakShow = True

            crosshairCheck = True
        
        if levelTimer:
            secondLevelCounter2 += 1
            if secondLevelCounter2 == toFps(1):
                if levelTime != 0:
                    levelTime -= 1
                else:
                    restart = True
                secondLevelCounter2 = 0
        
        if restart:
            camera.toPosition(202, 107)
            mapAliveCubes = mapEnemies.copy()
            levelTime = 5
            
            decimateAnnouncerCheck = False

            againCheck = True
            restart = False
            
        if againCheck:
            
            repeatSubtitleCheck = False
            decimateAnnouncerCheck = False
            
            againCounter += 1
            if againCounter == toFps(1):
                restartToolTipCheck = True
            if againCounter == toFps(3):
                restartToolTipDone = True
                restartToolTipCheck = False
                againCheck = False
                againCounter = 0
        
    # ? drawing of everything in the game
    draw()
    
    drawCounter += 1

    actualTime = newTime # ms
