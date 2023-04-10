import pygame, pascalengine, math, os
from pascalengine.player import Camera
from OpenGL.GL import *

class Cube():
    
    def __init__(self):
        self.hit = False
        # CUBE DATA
        self.vertices= (
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, -1, 1),
            (-1, 1, 1)
        )
        # maps how to connected vertices
        self.edges = (
            (0,1),
            (0,3),
            (0,4),
            (2,1),
            (2,3),
            (2,7),
            (6,3),
            (6,4),
            (6,7),
            (5,1),
            (5,4),
            (5,7)
        )
        # rgb in float 0-1 values
        self.r = (
            (1,0,0), #r
            (0,0,0), #r
            (0,0,0), #r
            (1,0,0), #r
            (1,0,0.6), #r
            (1,0,0), #r
            (1,0,0), #r
            (1,0,0), #r
            (1,0,0), #r
            (1,0,0), #r
            (1,0,0), #r
        )
        self.g = (
            (0,1,0), #r
            (0,0,0), #r
            (0,0,0), #r
            (0,1,0), #r
            (0,1,0.6), #r
            (0,1,0), #r
            (0,1,0), #r
            (0,1,0), #r
            (0,1,0), #r
            (0,1,0), #r
            (0,1,0), #r
        )
        self.b = (
            (0,0,1), #r
            (0,0,0), #r
            (0,0,0), #r
            (0,0,1), #r
            (0,0.6,1), #r
            (0,0,1), #r
            (0,0,1), #r
            (0,0,1), #r
            (0,0,1), #r
            (0,0,1), #r
            (0,0,1), #r
        )

        self.w = (
            (1,1,1), #r
            (0,0,0), #r
            (0,0,0), #r
            (1,1,1), #r
            (1,1,1), #r
            (1,1,1), #r
            (1,1,1), #r
            (1,1,1), #r
            (0,0,0), #r
            (0,0,0), #r
            (0,0,0), #r
        )
        # surfaces are groups of vertices
        # indexes to the vertices list
        self.surfaces = (
            (0,1,2,3),
            (3,2,7,6),
            (6,7,5,4),
            (4,5,1,0),
            (1,5,7,2),
            (4,0,3,6)
        )

    def cubeDraw(self, x, y, z, colour):
        # render colored surfaces as quads
        glBegin(GL_QUADS)
        for surface in self.surfaces:
            i = 0
            for vertex in surface:
                i+=1
                v = self.vertices[vertex]

                if colour == 'r':
                    glColor3fv(self.r[i])

                elif colour == 'g':
                    glColor3fv(self.g[i])

                elif colour == 'b':
                    glColor3fv(self.b[i])
                    
                elif colour == 'w':
                    glColor3fv(self.w[i])
                    
                else:
                    print("incorrect colour")
                    
                if self.hit == True:
                    glColor3fv(self.g[i])
                    
                glVertex3f(v[0] + x, v[1] + y, v[2] + z)
        glEnd()

        # render lines between vertices
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                v = self.vertices[vertex]
                glVertex3f(v[0] + x, v[1] + y, v[2] + z)
        glEnd()