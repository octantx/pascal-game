import pygame, pascalengine, math, os
from OpenGL.GL import *

# CUBE DATA
vertices= (
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
edges = (
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
red = (
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

green = (
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

blue = (
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


# surfaces are groups of vertices
# indexes to the vertices list
surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
)

def Cube(x, y, z, colour):
    # render colored surfaces as quads
    glBegin(GL_QUADS)
    for surface in surfaces:
        i = 0
        for vertex in surface:
            i+=1
            v = vertices[vertex]
            if colour == red:
                glColor3fv(red[i])
            elif colour == green:
                glColor3fv(green[i])
            elif colour == blue:
                glColor3fv(blue[i])
            else:
                print("incorrect colour")
            glVertex3f(v[0] + x, v[1] + y, v[2] + z)
    glEnd()

    # render lines between vertices
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            v = vertices[vertex]
            glVertex3f(v[0] + x, v[1] + y, v[2] + z)
    glEnd()