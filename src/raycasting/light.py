import numpy as np


class Light:
    def __init__(self, position: np.array, ambient: np.array, diffuse: np.array, specular: np.array):
        self.position = position
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
