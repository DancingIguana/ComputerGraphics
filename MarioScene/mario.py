from mesh import Mesh
from material import Material
from obj import Obj


class Mario:
    def __init__(self, position, shader_indexes):
        self.sprites = {
            "idle": {
                "file": "./textures/mario/idle.png",
                "material": None
            },
            "walking1": {
                "file": "./textures/mario/walking/1.png",
                "material": None
            },
            "walking2": {
                "file": "./textures/mario/walking/2.png",
                "material": None
            },
            "walking3": {
                "file": "./textures/mario/walking/3.png",
                "material": None
            }
        }
        self.mesh_file = "./objects/square/square.obj"
        self.mesh = Mesh(self.mesh_file, shader_indexes)

        self.obj = Obj(position=position,eulers=[0,0,0])
        for sprite in self.sprites:
            self.sprites[sprite]["material"] = Material(self.sprites[sprite]["file"])

        self.current_texture = self.sprites["idle"]["material"]
        self.animations = {
            "idle": ["idle"],
            "walking": ["walking1", "walking2", "walking3", "walking2"]
        }
        
    def right(self):
        self.obj.position[1] -= 0.03
        self.obj.eulers = [0,0,0]

    def left(self):
        self.obj.position[1] += 0.03
        self.obj.eulers = [0,180,0]



