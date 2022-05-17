from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

class Texture():
# simple texture class
# designed for 32 bit png images (with alpha channel)
    def __init__(self,fileName):
        self.texID=0
        self.LoadTexture(fileName)
    def LoadTexture(self,fileName): 
        try:
            textureSurface = pygame.image.load(fileName)
            textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
            
            self.texID=glGenTextures(1)
            
            glBindTexture(GL_TEXTURE_2D, self.texID)
            glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA,
                        textureSurface.get_width(), textureSurface.get_height(),
                        0, GL_RGBA, GL_UNSIGNED_BYTE, textureData )
            glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        except:
            pass
            # print "can't open the texture: %s"%(fileName)
    def __del__(self):
        glDeleteTextures(self.texID)

class Main():
    def resize(self, width, height):
        if height==0:
            height=1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #gluOrtho2D(-8.0, 8.0, -6.0, 6.0)
        glFrustum(-2,2,-2,2,1,8)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def init(self):
        #set some basic OpenGL settings and control variables
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        #glEnable(GL_BLEND)
        
        self.tutorial_texture=Texture("textures/tim.png") # ! argument?
        
        self.demandedFps=30.0
        self.done=False
        
        self.x,self.y,self.z=0.0 , 0.0, -4.0
        self.rX,self.rZ=0,0
        
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glPushMatrix()
        
        glTranslatef(self.x, self.y, self.z)

        glRotate(-self.rZ/3,0,0,1)
        glRotate(-self.rX/3,1,0,0)

        glColor4f(1.0, 1.0, 1.0,1.0)
        
        glBindTexture(GL_TEXTURE_2D,self.tutorial_texture.texID)
        
        glBegin(GL_QUADS)
        
        # ! ALL NECESSARY (HOW TEXTURES ARE MAPPED TO 3D SHIT)
        
        glTexCoord2f(0.0,1.0)
        glVertex3f(-1.0, 1.0,0.0)
        
        glTexCoord2f(1.0,1.0)
        glVertex3f(1.0, 1.0,-1.0)
        
        glTexCoord2f(1.0,0.0)
        glVertex3f(1.0, -1.0,0.0)
        
        glTexCoord2f(0.0,0.0)
        glVertex3f(-1.0, -1.0,1.0)
        
        glEnd()
        glBegin(GL_LINES)
        glColor(1,17,0)
        glVertex(0,0,0)
        glVertex(3,0,0)
        glColor(1,0,1)
        glVertex(0,0,0)
        glVertex(0,3,0)
        glColor(0,1,1)
        glVertex(0,0,0)
        glVertex(0,0,3)
        glEnd()
        glPopMatrix()
        
    def __init__(self):
        glOrtho(0, 800, 0, 600, 0.0, 100.0)
        video_flags = OPENGL|DOUBLEBUF|RESIZABLE
        
        pygame.init()
        pygame.display.set_mode((800,800), video_flags)
        
        pygame.display.set_caption("jason BALLS")
        
        self.resize(800,800)
        self.init()

        fl=0
        clock = pygame.time.Clock()
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT or self.done:
                    pygame.quit () 
                    break
                if event.type==MOUSEBUTTONDOWN:
                    if event.button==4: self.z+=0.1
                    if event.button==5: self.z-=0.1
                    if event.button==2: fl=1
                if event.type==MOUSEBUTTONUP:
                    if event.button==2: fl=0
                if event.type==VIDEORESIZE: self.resize((event.w,event.h))
            # self.Input(fl)
            self.draw()
            
            pygame.display.flip()
            
            #limit fps
            clock.tick(self.demandedFps)

if __name__ == '__main__': Main()