import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

class Cube:
    def __init__(self, origin_pos,texture_path):
        self.origin_pos = origin_pos
        self.vertices = [
            (1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1),
            (1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,-1)
        ]

        self.faces = [
            (1,2,3,0), # Front
            (6,7,2,1), # Left
            (0,3,4,5), # Right
            (5,4,7,6), # Back
            (0,1,6,5), # Top
            (2,3,4,7)  # Bottom
        ]

        self.normals = [
            (0,0,1),
            (-1,0,0),
            (1,0,0),
            (0,0,-1),
            (0,1,0),
            (0,-1,0)
        ]

        self.colors = [
            (1, 0, 0), # Red
            (0, 1, 0), # Green
            (0, 0, 1), # Blue
            (1, 1, 0), # Yellow
            (1, 0, 1), # Magenta
            (0, 1, 1)  # Cyan
        ]
        self.texture_path = texture_path
        self.image  = pygame.image.load(self.texture_path)
        self.datas = pygame.image.tostring(self.image, 'RGBA')

        self.texture_coordinates = [
            (0,0), (0,1), (1,1), (1,0)
        ]
        self.angle = 0
        self.material_ambient = [0.2, 0.2, 0.2, 1.0]
        self.material_diffuse = [0.8,0.8,0.8,1.0]
        self.material_specular = [1,1,1,1.0]
        self.material_shininess = 10.0

    def draw(self):
        glPushMatrix()
        texID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texID)
       # glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.image.get_width(), self.image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, self.datas)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glEnable(GL_TEXTURE_2D)

        glTranslate(self.origin_pos[0],self.origin_pos[1],self.origin_pos[2])
        glRotatef(self.angle,self.rotation_vector[0],self.rotation_vector[1],self.rotation_vector[2])
        #glEnable(GL_COLOR_MATERIAL)
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.material_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.material_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.material_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, self.material_shininess)
        glBegin(GL_QUADS)

        for face_idx, face in enumerate(self.faces):
            #glColor3fv(self.colors[face_idx])
            glNormal3fv(self.normals[face_idx])
            for i,vertex in enumerate(face):
                glTexCoord2fv(self.texture_coordinates[i])
                glVertex3fv(self.vertices[vertex])
        glEnd()
        #glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
    
    def rotate(self,angle,x,y,z):
        self.angle+=angle
        self.rotation_vector = [x,y,z]

    def move_from_axis(self,x,y,z):
        self.vertices = [[v[0] + x, v[1] + y, v[2] + z] for v in self.vertices]


class Light:
    def __init__(self, light_pos, ambient, diffuse, specular):
        self.light_pos = light_pos
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular

    def draw(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_pos)
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.specular)

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glTranslatef(0.0,0.0, -15)
    light_pos = [2, 2, 2, 1]
    ambient = [0.2, 0.2, 0.2, 1.0]
    diffuse = [0.8, 0.8, 0.8, 1.0]
    specular = [1, 1, 1, 1.0]
    my_light = Light(light_pos, ambient, diffuse, specular)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    
    cube1 = Cube([-5,0,0],"bricks.jpeg")
    cube2 = Cube([0,0,0], "cobblestone.jpeg")
    cube3 = Cube([5,0,0],"dirt.jpeg")
    cube4 = Cube([0,5,0], "sand.jpeg")
    cube5 = Cube([0,-5,0],"planks.png")
    cube6 = Cube([0,0,0], "stone.png")
    cube6.move_from_axis(-5,5,0)
    cube7 = Cube([0,0,0],"diamond.jpeg")
    cube7.move_from_axis(5,5,0)

    
    my_light.draw()
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