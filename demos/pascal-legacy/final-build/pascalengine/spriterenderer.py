import array
import pygame
from OpenGL.GL import *


class Text(object):
    
    def __init__(self) -> None:
        pass
    
    def drawText(x, y, text, font, colour):                                                
        textSurface = font.render(text, True, colour).convert_alpha()
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x, y)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
        
    def drawImage(path, infoArray):
        imageSurface = pygame.image.load(path)
        imageData = pygame.image.tostring(imageSurface, "RGBA", True)
        glWindowPos2d(infoArray[0]/2-100, 0)
        glDrawPixels(imageSurface.get_width(), imageSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, imageData)
        
    def dialogue(id, message, infoArray):
        
        box = pygame.image.load('final-build/assets/sprites/dialoguebox.png')
        imageData = pygame.image.tostring(box, "RGBA", True)
        glWindowPos2d(infoArray[0]/2-600, infoArray[1]/2-8-280)
        glDrawPixels(box.get_width(), box.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, imageData)
        
        # ? id will be used for displaying a character portrait, and other features(colour change maybe)
        
        messageArray = message.split()
        splits = len(messageArray) // 8 + 1
        messageY = [0]
        toAppend = []
        splitArray = []
        
        for i in range(splits):
            
            toAppend = ' '.join(messageArray[0:8])
            splitArray.append(toAppend)
            del messageArray[0:8]

        for i in range(len(splitArray)):
            
            value = messageY[0]; messageY.clear(); messageY.append(value + 20)
            Text.drawText(infoArray[0]/2-570, infoArray[1]/2-8-messageY[0]-45, splitArray[i], infoArray[2], infoArray[3])
        
# ? EXAMPLE: drawText(140, 120, "cube")
# ? COLOUR EXAMPLE (255, 255, 66, 255)
