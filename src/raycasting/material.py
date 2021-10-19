import numpy as np


class Material:
    def __init__(self, ambient: np.array, diffuse: np.array, specular: np.array, shininess: int, reflection: float):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflection = reflection
