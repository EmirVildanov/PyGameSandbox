import numpy as np

from src.raycasting.material import Material


class Figure:
    def __init__(self, material: Material):
        self.material = material


class Sphere(Figure):
    def __init__(self, center: np.array, radius: float, material: Material):
        super().__init__(material)
        self.center = center
        self.radius = radius
