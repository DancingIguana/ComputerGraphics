from typing import List
from OpenGL.GL import *
import numpy as np

class Mesh:
    def __init__(self, filename, shader_attribs):
        # x, y, z, s, t, nx, ny, nz
        vertices = self.loadMesh(filename)
        self.vertex_count = len(vertices) // 8
        vertices = np.array(vertices, dtype=np.float32)

        # Vertices
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        for attribute in shader_attribs:
            glEnableVertexAttribArray(shader_attribs[attribute]["index"])
            glVertexAttribPointer(
                shader_attribs[attribute]["index"],
                shader_attribs[attribute]["size"],
                shader_attribs[attribute]["type"],
                shader_attribs[attribute]["normalize"],
                shader_attribs[attribute]["stride"],
                shader_attribs[attribute]["pointer"]
            )

    def destroy(self):
        glDeleteBuffers(1, (self.vbo,))

    def loadMesh(self, filename: str) -> List[float]:

        v = []
        vt = []
        vn = []

        vertices = []

        with open(filename, "r") as file:

            line = file.readline()

            while line:

                words = line.split(" ")
                if words[0] == "v":
                    v.append(self.read_vertex_data(words))
                elif words[0] == "vt":
                    vt.append(self.read_texcoord_data(words))
                elif words[0] == "vn":
                    vn.append(self.read_normal_data(words))
                elif words[0] == "f":
                    self.read_face_data(words, v, vt, vn, vertices)
                line = file.readline()

        return vertices
    
    def read_vertex_data(self, words: List[str]) -> List[float]:

        return [
            float(words[1]),
            float(words[2]),
            float(words[3])
        ]
    
    def read_texcoord_data(self, words: List[str]) -> List[float]:

        return [
            float(words[1]),
            float(words[2])
        ]
    
    def read_normal_data(self, words: List[str]) -> List[float]:

        return [
            float(words[1]),
            float(words[2]),
            float(words[3])
        ]

    def read_face_data(
        self, words: List[str], 
        v: List[List[float]], vt: List[List[float]], 
        vn: List[List[float]], vertices: List[float]) -> None:

        triangleCount = len(words) - 3

        for i in range(triangleCount):

            self.make_corner(words[1], v, vt, vn, vertices)
            self.make_corner(words[2 + i], v, vt, vn, vertices)
            self.make_corner(words[3 + i], v, vt, vn, vertices)
    
    def make_corner(self, corner_description: str, 
        v: List[List[float]], vt: List[List[float]], 
        vn: List[List[float]], vertices: List[float]) -> None:

        v_vt_vn = corner_description.split("/")
        for element in v[int(v_vt_vn[0]) - 1]:
            vertices.append(element)
        for element in vt[int(v_vt_vn[1]) - 1]:
            vertices.append(element)
        for element in vn[int(v_vt_vn[2]) - 1]:
            vertices.append(element)
    
    def destroy(self):
        glDeleteBuffers(1, (self.vbo,))