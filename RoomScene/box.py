import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from collections import defaultdict
face_names = ["front", "left", "right", "back", "top", "bottom"]

class Cube:
    def __init__(
            self, 
            origin_pos,
            size = [1,1,1],
            visible_faces = face_names,
            material_ambient = [0.2, 0.2, 0.2, 1.0],
            material_diffuse = [0.8,0.8,0.8,1.0],
            material_specular = [1,1,1,1.0],
            material_shininess = 10.,
            textures = defaultdict(None,{}),
            texture_coords = defaultdict(None,{})
        ):
        print(textures)
        print(texture_coords)
        self.origin_pos = origin_pos
        self.rotation_vector = [0,0,0]
        self.visible_faces = visible_faces
        self.vertices = [
            (size[0]*1,size[1]*1,size[2]*1),
            (size[0]*-1,size[1]*1,size[2]*1),
            (size[0]*-1,size[1]*-1,size[2]*1),
            (size[0]*1,size[1]*-1,size[2]*1),
            (size[0]*1,size[1]*-1,size[2]*-1),
            (size[0]*1,size[1]*1,size[2]*-1),
            (size[0]*-1,size[1]*1,size[2]*-1),
            (size[0]*-1,size[1]*-1,size[2]*-1)
        ]
        
        default_texture_coords = [(0,0), (0,1), (1,1), (1,0)]
        textures_complete_dict  = {}
        texture_coords_complete_dict = {}
        for face in face_names:
            if face in textures:
                textures_complete_dict[face] = textures[face]
            else:
                textures_complete_dict[face] = None
            
            if face in texture_coords:
                texture_coords_complete_dict[face] = texture_coords[face]
            else:
                texture_coords_complete_dict[face] = default_texture_coords

        self.face_data = {
            "front": {
                "indexes": (3,0,1,2),
                "normals": (0,0,1),
                "texture": textures_complete_dict["front"],
                "texture_coords": texture_coords_complete_dict["front"]
            },
            "left": {
                "indexes": (2,1,6,7),
                "normals": (-1,0,0),
                "texture": textures_complete_dict["left"],
                "texture_coords": texture_coords_complete_dict["left"]
            },
            "right": {
                "indexes": (4,5,0,3),
                "normals": (1,0,0),
                "texture": textures_complete_dict["right"],
                "texture_coords": texture_coords_complete_dict["right"]
            },
            "back": {
                "indexes": (7,6,5,4),
                "normals": (0,0,-1),
                "texture": textures_complete_dict["back"],
                "texture_coords": texture_coords_complete_dict["back"]
            },
            "top": {
                "indexes": (0,5,6,1),
                "normals": (0,1,0),
                "texture": textures_complete_dict["top"],
                "texture_coords": texture_coords_complete_dict["top"]
            }, 
            "bottom": {
                "indexes":(2,7,4,3),
                "normals": (0,-1,0),
                "texture": textures_complete_dict["bottom"],
                "texture_coords": texture_coords_complete_dict["bottom"]
            } 
        }
        
        self.colors = [
            (1, 0, 0), # Red
            (0, 1, 0), # Green
            (0, 0, 1), # Blue
            (1, 1, 0), # Yellow
            (1, 0, 1), # Magenta
            (0, 1, 1)  # Cyan
        ]
        
        self.angle = 0
        self.orbit_angle = 0
        self.orbit_point = [0,0,0]
        self.in_orbit = False

        # Light components
        self.material_ambient = material_ambient
        self.material_diffuse = material_diffuse
        self.material_specular = material_specular
        self.material_shininess = material_shininess

    def draw(self):
        glPushMatrix()
        glTranslate(self.origin_pos[0],self.origin_pos[1],self.origin_pos[2])
        glRotatef(self.angle,self.rotation_vector[0],self.rotation_vector[1],self.rotation_vector[2])
        if self.in_orbit:
            glTranslatef(self.orbit_point[0],self.orbit_point[1],self.orbit_point[2])
            glRotatef(self.orbit_angle,self.orbit_rotation_vector[0],self.orbit_rotation_vector[1],self.orbit_rotation_vector[2])
            glTranslatef(-self.orbit_point[0],-self.orbit_point[1],-self.orbit_point[2])
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.material_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.material_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.material_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, self.material_shininess)

        glEnable(GL_TEXTURE_2D)
        for face_idx, face in enumerate(self.visible_faces):
            if self.face_data[face]["texture"]:#self.textures is not None:
                glBindTexture(GL_TEXTURE_2D, self.face_data[face]["texture"])#self.textures[face_idx])
            glBegin(GL_QUADS)
            glNormal3fv(self.face_data[face]["normals"])#self.normals[face_idx])
            for i,vertex in enumerate(self.face_data[face]["indexes"]):
                if self.face_data[face]["texture"]:#self.textures:
                    glTexCoord2fv(self.face_data[face]["texture_coords"][i])#self.texture_coords[face_idx][i])
                glVertex3fv(self.vertices[vertex])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()


    def rotate(self,angle,x,y,z):
        self.angle+=angle
        self.rotation_vector = [x,y,z]

    def orbit(self, angle, x, y, z, cx, cy, cz):
        self.orbit_angle += angle
        self.orbit_rotation_vector = x,y,z
        self.orbit_point = cx,cy,cz
        self.in_orbit = True

    def move_from_axis(self,x,y,z):
        self.vertices = [[v[0] + x, v[1] + y, v[2] + z] for v in self.vertices]
