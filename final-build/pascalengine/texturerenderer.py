from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

class Texture():
    
    def __init__(self,fileName):
        
        self.texID=0
        self.loadTexture(fileName)
        
    def loadTexture(self,fileName): 
        
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
            