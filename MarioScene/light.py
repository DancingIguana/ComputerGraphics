import numpy as np
class Light:
    def __init__(self, position, color, strength):

        self.position = np.array(position, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)
        self.strength = strength
        self.on = True