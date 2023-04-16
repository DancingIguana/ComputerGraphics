import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront

def load_obj(filename):
    obj = pywavefront.Wavefront(filename)
    glNewList(1, GL_COMPILE)
    glBegin(GL_TRIANGLES)
    for mesh in obj.mesh_list:
        for face in mesh.faces:
            for vertex_i in face:
                glVertex3f(*obj.vertices[vertex_i])
    glEnd()
    glEndList()


def load_texture(filename):
    surface = pygame.image.load(filename)
    data = pygame.image.tostring(surface, "RGB", 1)
    width = surface.get_width()
    height = surface.get_height()
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    return texture