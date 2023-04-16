import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    def __init__(self, position, angle):
        self.position = list(position)
        self.angle = list(angle)

    def set(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotate(self.angle[0], 1, 0, 0)
        glRotate(self.angle[1], 0, 1, 0)
        glRotate(self.angle[2], 0, 0, 1)
        glTranslate(self.position[0], self.position[1], self.position[2])

    def update_position(self, position):
        self.position = position

    def update_angle(self, angle):
        self.angle = angle
