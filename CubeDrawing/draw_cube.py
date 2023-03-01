import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


class Cube:
    def __init__(self, origin_pos = [0,0,0]):
        self.vertices = [(-1,-1,-1), ( 1,-1,-1), ( 1, 1,-1), (-1, 1,-1), (-1,-1, 1), ( 1,-1, 1), ( 1, 1, 1), (-1, 1, 1)]
        self.faces = (
            (0,1,2), (0,2,3), (5,4,7), (5,7,6), (4,0,3), (4,3,7), 
            (1,5,6), (1,6,2), (4,5,1), (4,1,0), (3,2,6), (3,6,7)
        )

        self.colors = [(1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1), (1, 0, 1)]

        self.origin_pos = origin_pos
        self.angle = 0
        self.rotation_vector = [0,0,0]
        self.draw()

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslate(self.origin_pos[0],self.origin_pos[1],self.origin_pos[2])
        glRotate(self.angle,self.rotation_vector[0],self.rotation_vector[1],self.rotation_vector[2])
        glBegin(GL_TRIANGLES)
        for face_idx, face in enumerate(self.faces):
            glColor3fv(self.colors[face_idx // 2])
            for vertex in face:
                glVertex3fv(self.vertices[vertex])
        glEnd()
        glPopMatrix()

    def move_from_axis(self,x,y,z):
        self.vertices = [[v[0] + x, v[1] + y, v[2] + z] for v in self.vertices]

    def rotate(self,angle,x,y,z):
        self.angle+=angle
        self.rotation_vector = [x,y,z]

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 1000.0)
    glEnable(GL_DEPTH_TEST)
    glTranslatef(0.0,0.0, -15)

    cube1 = Cube([-5,0,0])
    cube2 = Cube([0,0,0])
    cube3 = Cube([5,0,0])
    cube4 = Cube([0,5,0])
    cube5 = Cube([0,-5,0])
    cube6 = Cube([0,0,0])
    cube6.move_from_axis(-5,5,0)
    cube7 = Cube([0,0,0])
    cube7.move_from_axis(5,5,0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        cube1.rotate(0.90,0,1,0)
        cube2.rotate(0.90,1,1,1)
        cube3.rotate(0.90,0,-1,0)
        cube4.rotate(0.90,1,0,0)
        cube5.rotate(0.90,-1,0,0)
        cube6.rotate(0.90,1,1,0)
        cube7.rotate(0.90,-1,1,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cube1.draw()
        cube2.draw()
        cube3.draw()
        cube4.draw()
        cube5.draw()
        cube6.draw()
        cube7.draw()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()