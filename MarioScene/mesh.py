from typing import List
from OpenGL.GL import *
import numpy as np

class Mesh:
    def __init__(self, filename, shader_indexes):
        # x, y, z, s, t, nx, ny, nz
        vertices = self.loadMesh(filename)
        self.vertex_count = len(vertices) // 8
        vertices = np.array(vertices, dtype=np.float32)

        # Vertices
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        # Position
        #position = glGetAttribLocation(shader_indexes["vertexPos"], "vertexPos")
        #print(position)
        glEnableVertexAttribArray(shader_indexes["vertexPos"])
        glVertexAttribPointer(shader_indexes["vertexPos"], 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        # Texture
        #texCoord = glGetAttribLocation(shader_indexes["vertexTexCoord"], "vertexTexCoord")
        #print(texCoord)
        glEnableVertexAttribArray(shader_indexes["vertexTexCoord"])
        glVertexAttribPointer(shader_indexes["vertexTexCoord"], 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        # Normal
        #normal = glGetAttribLocation(shader_indexes["vertexNormal"], "vertexNormal")
        glEnableVertexAttribArray(shader_indexes["vertexNormal"])
        glVertexAttribPointer(shader_indexes["vertexNormal"], 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))

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