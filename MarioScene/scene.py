from obj import Obj
from light import Light
from camera import Camera
import numpy as np
from OpenGL.GL import *
import ctypes
class Scene:
    def __init__(self):

        self.meshes = [
            (
                "cube",
                "./objects/cube/cube.obj",
                "V3_T2_N3"
            ),
            (
                "box",
                "./objects/box/box.obj",
                "V3_T2_N3"
            )
        ]

        self.textures = [
            (
                "sky",
                "./textures/sky.png",
            ),
            (
                "mystery",
                "./textures/mystery.png"
            )
        ]


        self.global_shader_attributes = {
            "V3_T2_N3": {
                "vertexPos": {
                    "index": 0,
                    "size": 3,
                    "type": GL_FLOAT,
                    "normalize": GL_FALSE,
                    "stride": 32,
                    "pointer": ctypes.c_void_p(0)
                },
                "vertexTexCoord": {
                    "index": 1,
                    "size": 2,
                    "type": GL_FLOAT,
                    "normalize": GL_FALSE,
                    "stride": 32,
                    "pointer": ctypes.c_void_p(12)
                },
                "vertexNormal": {
                    "index": 2,
                    "size": 3,
                    "type": GL_FLOAT,
                    "normalize": GL_FALSE,
                    "stride": 32,
                    "pointer": ctypes.c_void_p(20)
                },
            }
        }
        
        self.shaders = [
            {
                "key": "blinn_phong_shader", 
                "vertex":"./shaders/blinn_phong_vertex.txt",
                "fragment":"./shaders/blinn_phong_fragment.txt",
                "attributes_key": "V3_T2_N3"
            }
        ]

        self.objs = [
            (
                "box",           
                "sky",
                "blinn_phong_shader",
                Obj(position = [0,0,0], eulers = [0,0,0])
            ),
            (
                "cube", # key of the object mesh
                "brick", # key of the object texture
                "blinn_phong_shader", # key of the shader
                Obj(position = [6,0,0], eulers = [0,0,0])
            ),
            #(
            #    "cube",
            #    "brick",
            #    Obj(position = [6,2,0], eulers = [0,0,0])
            #),
        ]
        #self.cubes = [
        #    Cube(
        #        position = [0,0,0],
        #        eulers = [0,0,0]
        #    )
        #]

        self.lights = [
            
            Light(
                position = [
                    -0.5,
                    0,
                    0
                ],
                color = [
                    1,
                    1,
                    1
                ],
                strength = 0.5
            )
        ]

        self.camera = Camera(
            position = [-1,0,0]
        )

    def update(self,):
        #for i in range(len(self.objs)):
        #    self.objs[i][2].eulers[1] += 0.25 * 1
        #    if self.objs[i][2].eulers[1] > 360:
        #        self.objs[i][2].eulers[1] -= 360
        return