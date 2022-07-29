from pascalengine.camera import *
from pascalengine.eventlistener import *
from pascalengine.mathdef import *
import math

class Cmd:
    
    forwardMove = None
    rightMove = None
    upMove = None
    
class Player:
    
    global playerViewYOffset; playerViewYOffset = 0.6
    global xMouseSensitivity; xMouseSensitivity = 30.0
    global yMouseSensitivity; yMouseSensitivity = 30.0
    
    # frame occuring factors
    
    global gravity; gravity = 20.0
    global friction; friction = 6 # Ground friction
    
    # "movement stuff"
    
    global moveSpeed; moveSpeed = 7.0 # Ground move speed
    global runAcceleration; runAcceleration = 14.0 # Ground accel
    global runDeacceleration; runDeacceleration = 10.0 # Deacceleration that occurs when running on the ground
    global airAcceleration; airAcceleration = 2.0 # Air acceleration
    global airDeacceleration; airDeacceleration = 2.0 # Deacceleration experienced when opposite strafing
    global airControl; airControl = 0.3 # How precise air control is
    global sideStrafeAcceleration; sideStrafeAcceleration = 50.0 # How fast acceleration occurs to get up to sideStrafeSpeed
    global sideStrafeSpeed; sideStrafeSpeed = 1.0 # The max speed to generate when side strafing
    global jumpSpeed; jumpSpeed = 8.0  # The speed at which the character's up axis gains when hitting the jump button
    global holdJumpToBhop; holdJumpToBhop = False # When enabled allows the player to hold jump button to bhop perfectly. Beware: who gives a shit
    
    # frames per second stuff
    
    fpsDisplayRate = 4.0
    frameCount = 0
    global fps; fps = 60.0
    global dt; dt = 0
    
    # Camera rotations
    
    rotX = 0.0
    rotY = 0.0
    
    global moveDirectionNorm; moveDirectionNorm = [0, 0, 0]
    global playerVelocity; playerVelocity = [0, 0, 0]
    playerTopVelocity = 0.0
    
    # the ability to queue a jump before hitting the ground
    global wishJump; wishJump = False
    
    # used to display real time friction values
    global playerFriction; playerFriction = 0.0
    
    # ! "Start()" not needed, so removed (handled already)
    
    # ! unsure what parts of "Update()" are needed, skipped for now

    # sets the movement direction based on the player's input
    global SetMovementDir
    def SetMovementDir():
        
        Cmd.forwardMove = Camera.moveDir[1]
        Cmd.rightMove = Camera.moveDir[0]
        
    global Accelerate
    def Accelerate(wishDir, wishSpeed, accel):
        
        currentSpeed = dot(playerVelocity, wishDir)
        addSpeed = wishSpeed - currentSpeed
        
        if addSpeed <= 0:
            return
        accelSpeed = accel * dt * wishSpeed
        if accelSpeed > addSpeed:
            accelSpeed = addSpeed
            
        playerVelocity[0] += accelSpeed * wishDir[0]
        playerVelocity[2] += accelSpeed * wishDir[2]
        
    global ApplyFriction
    def ApplyFriction(t):
        
        vec = playerVelocity
        speed = None
        newSpeed = None
        control = None
        drop = None
        
        vec[1] = 0.0
        speed = magnitude(vec)
        drop = 0.0
        
        if Camera.isGrounded():
            
            # ! how the hell do we do this
            # control = speed < runDeacceleration ? runDeacceleration
            pass
            
        newSpeed = speed - drop
        playerFriction = newSpeed
        if newSpeed < 0:
            newSpeed = 0
        if speed > 0:
            newSpeed /= speed
        
        playerVelocity[0] *= newSpeed
        playerVelocity[2] *= newSpeed
        
    # queues the next jump just like Q3
    def QueueJump():
        
        if holdJumpToBhop:
            
            wishJump = EventListener.onKeyHold(pygame.K_SPACE)
            return wishJump
        
        jumpKeyPressed = EventListener.onKeyDown(pygame.K_SPACE)
        jumpKeyReleased = EventListener.onKeyUp(pygame.K_SPACE)
        
        if jumpKeyPressed and not wishJump:
            
            wishJump = True
        
        if jumpKeyReleased:
            
            wishJump = False
            
    # executes when player is in the air
    
    def AirMove():
        
        wishvel = airAcceleration
        accel = None
        
        SetMovementDir()
        
        wishDir = [Cmd.rightMove, 0, Cmd.forwardMove]
        
        wishSpeed = magnitude(wishDir)
        wishSpeed *= moveSpeed
        
        wishDir = normalizeVector(wishDir)
        moveDirectionNorm = wishDir
        
        wishSpeed2 = wishSpeed
        if dot(playerVelocity, wishDir) < 0:
            accel = airDeacceleration
        else:
            accel = airAcceleration
        
        if Cmd.forwardMove == 0 and Cmd.rightMove != 0:
            
            if wishSpeed > sideStrafeSpeed:
                wishSpeed = sideStrafeSpeed
            accel = sideStrafeAcceleration
            
        Accelerate(wishDir, wishSpeed, accel)
        
        if airControl > 0:
            AirControl(wishDir, wishSpeed2)
            
        # ! CPM: Aircontrol
        
        playerVelocity[1] -= gravity * deltaTime(60)
        
    global AirControl
    def AirControl(wishDir, wishSpeed):
        
        zspeed = None
        speed = None
        dotVar = None
        k = None
        
        if abs(Cmd.forwardMove) < 0.001 or abs(wishSpeed) < 0.001:
            return
        zspeed = playerVelocity[1]
        playerVelocity[1] = 0 # ! this could cause a bug
        
        speed = magnitude(playerVelocity)
        playerVelocity = normalizeVector(playerVelocity)
        
        dotVar = dot(playerVelocity, wishDir)
        k = 32
        k *= airControl * dotVar * dotVar * deltaTime(60)
        
        if dotVar > 0:
            
            playerVelocity[0] = playerVelocity[0] * speed + wishDir[0] * k
            playerVelocity[1] = playerVelocity[1] * speed + wishDir[1] * k
            playerVelocity[2] = playerVelocity[2] * speed + wishDir[2] * k
            
            playerVelocity = normalizeVector(playerVelocity)
            moveDirectionNorm = playerVelocity
        
        playerVelocity[0] *= speed
        playerVelocity[1] = zspeed
        playerVelocity[2] *= speed
        
    def GroundMove():
        
        wishDir = [0, 0, 0]
        
        if not wishJump:
            ApplyFriction(1.0)
        else: 
            ApplyFriction(0)
            
        SetMovementDir()
        
        wishDir = [Cmd.rightMove, 0, Cmd.forwardMove]
        
        wishDir = normalizeVector(wishDir)
        moveDirectionNorm = wishDir
        
        wishSpeed = magnitude(wishDir)
        wishSpeed *= moveSpeed
        
        Accelerate(wishDir, wishSpeed, runAcceleration)
        
        playerVelocity[1] = -gravity * deltaTime(60)
        
        if wishJump:
            
            playerVelocity[1] = jumpSpeed
            wishJump = False