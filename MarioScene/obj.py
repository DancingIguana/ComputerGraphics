import numpy as np
class Obj:
    def __init__(self, position, eulers, scale = [1,1,1]):

        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
        self.scale = np.array(scale, dtype = np.float32)