import pygame, math, numpy
from pascalengine.math import *
from pascalengine.eventlistener import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Cmd:
    
    forwardMove = None
    rightMove = None
    upMove = None

class Camera(object):

    def __init__(self, solidBsp):
        self.solidBsp = solidBsp
        self.collisionDetection = True
        self.gravity = 20.0
        self.friction = 6
        # move
        self.moveSpeed = .7
        self.moveDir = [0, 0] # x,y or strafe/fwd
        self.worldPos = [0, 0, 0] # x, y, z
        self.runAcceleration = 14.0
        self.runDeacceleration = 10.0
        self.airAcceleration = 2.0
        self.airDeacceleration = 2.0
        self.airControl = 0.3
        self.sideStrafeAcceleration = 50.0
        self.sideStrafeSpeed = 1.0
        self.jumpSpeed = 8.0
        self.holdJumpToBhop = True
        self.playerFriction = 0.0
        # look
        self.lookSpeed = .2
        self.pitch = 0
        self.pitchMax = math.pi/2 - .05 # maximum rotation negative and positive for pitch
        self.pitchDelta = 0
        self.yaw = 0
        self.yawDelta = 0
        self.moveDirectionNorm = [0, 0, 0]
        self.playerVelocity = [0, 0, 0]
        self.playerTopVelocity = 0.0
        # locks
        self.lockFlight = True
        self.wishJump = False

    def moveForward(self):
        self.moveDir[1] = 1

    def moveBackward(self):
        self.moveDir[1] = -1

    def strafeLeft(self):
        self.moveDir[0] = 1

    def strafeRight(self):
        self.moveDir[0] = -1

    def applyMouseMove(self, deltaX, deltaY, screenX, screenY):
        self.yawDelta += deltaX
        self.pitchDelta += deltaY
    
    def setPosition(self, x, y, z):
        # camera translates in the inverse of the world?
        glTranslate(-x, -y, -z)
        
    def toPosition(self, x, z):
        rX = x - self.worldPos[0]
        rZ = z - self.worldPos[2]
        glTranslate(-rX, 0, -rZ)
        
    
    def setYaw(self, yawRadians):
        self.yawDelta = rad2deg(yawRadians) / self.lookSpeed

    def checkMove(self):
        wp = self.findWorldPos()
        if not self.collisionDetection or self.solidBsp.inEmpty([wp[0], wp[2]]):
            return True
        return False

    def findWorldPos(self):
        M = glGetDoublev(GL_MODELVIEW_MATRIX)
        C = (numpy.mat(M[:3,:3]) * numpy.mat(M[3,:3]).T).reshape(3,1).tolist()
        return [-C[0][0], -C[1][0], -C[2][0]]

    def update(self):

        # normalize move vector so strafe + fwd is not faster
        self.moveDir = normalize(self.moveDir[0], self.moveDir[1])
        
        if self.moveDir[0] != 0:
            strafe = self.moveDir[0] * self.moveSpeed
            m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
            glTranslate(strafe * m[0], strafe * m[4], strafe * m[8])
            # test if it is valid
            if not self.checkMove():
                # move us back
                glTranslate(-strafe * m[0], -strafe * m[4], -strafe * m[8])
            self.moveDir[0] = 0
            
        if self.moveDir[1] != 0:
            fwd = self.moveDir[1] * self.moveSpeed
            # move us there
            m = glGetDoublev(GL_MODELVIEW_MATRIX).flatten()
            glTranslate(fwd * m[2], 0 if self.lockFlight else fwd * m[6], fwd * m[10])
            # test if it is valid
            if not self.checkMove():
                # move us back
                glTranslate(-fwd * m[2], 0 if self.lockFlight else -fwd * m[6], -fwd * m[10])
            self.moveDir[1] = 0
            
        # look
        if self.yawDelta != 0 or self.pitchDelta != 0:
            yawDeltaDegrees = self.yawDelta * self.lookSpeed
            yawDeltaRadians = deg2rad(yawDeltaDegrees)
            pitchDeltaDegrees = self.pitchDelta * self.lookSpeed
            pitchDeltaRadians = deg2rad(pitchDeltaDegrees)

            M = glGetDoublev(GL_MODELVIEW_MATRIX)
            c = (numpy.mat(M[:3,:3]) * numpy.mat(M[3,:3]).T).reshape(3,1)
            # c is camera center in absolute coordinates (world pos)
            # we need to move it back to (0,0,0)
            # before rotating the camera
            glTranslate(-c[0], -c[1], -c[2])
            m = M.flatten()
            # yaw in y axis unlimited
            glRotate(yawDeltaDegrees, m[1], m[5], m[9])
            self.yaw += yawDeltaRadians

            # pitch in x axis should be limited to -90 and +90 degrees
            # newPitch = self.pitch + pitchDeltaRadians
            # if newPitch < self.pitchMax and newPitch > -self.pitchMax:
            #     self.pitch = newPitch
            #     glRotate(pitchDeltaDegrees, m[0], m[4], m[8])

            # compensate roll (not sure what this does yet)
            # glRotated(-math.atan2(-m[4],m[5]) * 57.295779513082320876798154814105, m[2], m[6], m[10])
            # reset translation back to where we were
            glTranslate(c[0], c[1], c[2])

            self.yawDelta = 0
            # self.pitchDelta = 0

        # get and set world position
        self.worldPos = self.findWorldPos()

