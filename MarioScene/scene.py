from obj import Obj
from light import Light
from camera import Camera
import numpy as np

class Scene:
    def __init__(self):

        self.assets = [
            ("cube", "./objects/cube/cube.obj", "mesh"),
            ("box", "./objects/box/box.obj", "mesh"),
            ("floor", "./objects/floor/floor.obj", "mesh"),
            ("square", "./objects/square/square.obj", "mesh"),
            ("mystery", "./textures/mystery.png", "material"),
            ("floor_block", "./textures/floor.png", "material"),
            ("sky", "./textures/sky.png", "material"),
            ("brick", "./textures/brick.png", "material"),
            ("mario_sprites", "./textures/mario/idle.png", "material"),
            ("cloud", "./textures/cloud.png", "material"),
            ("bush","./textures/bush.png", "material"),
            ("goomba", "./textures/goomba.png", "material"),
            ("mushroom", "./textures/mushroom.png", "material")
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
                "floor",
                "floor_block",
                Obj(position=[5,0,-1.5],eulers = [0,0,0])
            ),
            (
                "cube", # key of the object mesh
                "mystery", # key of the object texture
                Obj(position = [5,0,0], eulers = [0,0,0])
            ),
            (
                "cube",
                "brick",
                Obj(position = [5,-1.5,0], eulers = [0,0,0])
            ),
            (
                "cube", # key of the object mesh
                "mystery", # key of the object texture
                Obj(position = [5,-2,0], eulers = [0,0,0])
            ),
            (
                "cube", # key of the object mesh
                "brick", # key of the object texture
                Obj(position = [5,-2.5,0], eulers = [0,0,0])
            ),
            (
                "cube", # key of the object mesh
                "mystery", # key of the object texture
                Obj(position = [5,-3,0], eulers = [0,0,0])
            ),
            (
                "cube", # key of the object mesh
                "brick", # key of the object texture
                Obj(position = [5,-3.5,0], eulers = [0,0,0])
            ),
            (
                "cube", # key of the object mesh
                "mystery", # key of the object texture
                Obj(position = [5,-2.5,1.5], eulers = [0,0,0])
            ),
            (
                "square",
                "bush",
                Obj(position=[5.5,4,-1], eulers=[0,0,0],scale=[1,2,1])
            ),
            (
                "square",
                "bush",
                Obj(position=[5.5,2,-1], eulers=[0,0,0],scale=[1,2,1])
            ),
            (
                "square",
                "bush",
                Obj(position=[5.5,-3,-1], eulers=[0,0,0],scale=[1,2,1])
            ),
            (
                "square",
                "cloud",
                Obj(position=[5.5,3,1], eulers=[0,0,0],scale=[1,1.5,1])
            ),
            (
                "square",
                "cloud",
                Obj(position=[5.5,1,1.5], eulers=[0,0,0],scale=[1,2,1])
            ),
            (
                "square",
                "cloud",
                Obj(position=[5.5,-3.5,1.2], eulers=[0,0,0],scale=[1,2,1])
            ),
            (
                "square",
                "cloud",
                Obj(position=[5.5,-7.5,2], eulers=[0,0,0],scale=[1,2,1])
            ),
            (
                "square",
                "mushroom",
                Obj(position=[5,5,-1.1],eulers = [0,0,0], scale = [0.75,0.75,0.75])
            ),
            (
                "square",
                "goomba",
                Obj(position=[5,-5.5,-1.1],eulers = [0,0,0], scale =[0.75,0.75,0.75])
            ),
            
            #(
            #   "mario",
            #    "mario_sprites",
            #    Obj(position = [5.5,0,-1], eulers = [0,0,0])
            #)
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
                    4.5,
                    5,
                    0
                ],
                color = [
                    1,
                    1,
                    1
                ],
                strength = 5
            ),
            Light(
            position = [
                3,
                5,
                0
            ],
            color = [
                1,
                1,
                1
            ],
            strength = 100
            ),
            Light(
            position = [
                3,
                -5,
                0
            ],
            color = [
                1,
                1,
                1
            ],
            strength = 100,
            ),

        ]

        self.camera = Camera(
            position = [0,5,0]
        )

        self.camera_mode = "follow"
        self.goomba_dir_multiplier = 1
        self.mushroom_dir_multiplier = -1
    def update(self,mario):
        if self.camera_mode == "follow":
            self.camera.position = [0,mario.obj.position[1], 0]
        else:
            self.camera.position = [-5,0,0]

        if self.objs[-1][2].position[1] >= 7: 
            self.goomba_dir_multiplier *= -1
        if self.objs[-1][2].position[1] <= -7:
            self.goomba_dir_multiplier *= -1
            
        if self.objs[-2][2].position[1] >= 7:
            self.mushroom_dir_multiplier *= -1
        if self.objs[-2][2].position[1] <= -7: 
            self.mushroom_dir_multiplier *=-1

        self.objs[-1][2].position[1] += self.goomba_dir_multiplier*0.02
        self.objs[-2][2].position[1] += self.mushroom_dir_multiplier*0.02


        #self.objs[-1][2].position[1] += 0.02
        self.lights[0].position[1] = mario.obj.position[1]
        #for i in range(len(self.objs)):
        #    self.objs[i][2].eulers[1] += 0.25 * 1
        #    if self.objs[i][2].eulers[1] > 360:
        #        self.objs[i][2].eulers[1] -= 360
        return