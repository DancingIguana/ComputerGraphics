import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from pywavefront import Wavefront, visualization

# initialize Pygame
pygame.init()
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF|OPENGL)

# initialize PyOpenGL
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, width/height, 0.1, 1000.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glEnable(GL_DEPTH_TEST)

# load .obj file using PyWavefront
obj = Wavefront('./my_object/dio/wry.obj',)#create_materials=True)

angle = 0
# render the object
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    angle+=1
    if angle == 720: angle = 0
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    # draw the object
    glPushMatrix()
    glTranslatef(0,-50,-150)
    glRotatef(angle,0,0.9,0)
    glScalef(0.5, 0.5, 0.5) 
    visualization.draw(obj)
    glPopMatrix()
    pygame.display.flip()
    pygame.time.wait(10)
