from obj import Obj
from light import Light
from camera import Camera
import numpy as np

class Scene:
    def __init__(self):

        self.assets = [
            ("cube", "./objects/cube/cube.obj", "mesh"),
            ("box", "./objects/box/box.obj", "mesh"),
            ("sky", "./textures/sky.png", "material"),
            ("brick", "./textures/mystery.png", "material"),

        ]
        #self.shaders = [
        #    ("blinn_phong", "./shaders/")
        #]
        self.objs = [
            (
                "box",           
                "sky",
                Obj(position = [5,0,0], eulers = [0,0,0])
            ),
            (
                "cube", # key of the object mesh
                "brick", # key of the object texture
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
                    4,
                    0,
                    0
                ],
                color = [
                    1,
                    1,
                    1
                ],
                strength = 3
            )
        ]

        self.camera = Camera(
            position = [0,0,0]
        )

    def update(self,):
        for i in range(len(self.objs)):
            self.objs[i][2].eulers[1] += 0.25 * 1
            if self.objs[i][2].eulers[1] > 360:
                self.objs[i][2].eulers[1] -= 360
        return