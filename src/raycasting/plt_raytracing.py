from typing import Optional, Tuple, List

import numpy as np
from math import cos, radians, sin
import matplotlib.pyplot as plt
from pygame import gfxdraw

from src.raycasting.constants import *
from src.raycasting.geometry import Sphere, Figure
from src.raycasting.light import Light
from src.raycasting.material import Material

Vector = np.array


def remap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def convert_norm_to_rgb(color: np.array) -> List[int]:
    color = list(color)
    return [i * 255 for i in color]


def normalize(vector) -> Vector:
    """
    Function to normalize vector
    :param vector:
    :return:
    """
    return vector / np.linalg.norm(vector)


def reflected(vector, axis) -> Vector:
    """
    Function that returns reflected vector from (sphere)
    :param vector:
    :param axis:
    :return:
    """
    return vector - 2 * np.dot(vector, axis) * axis


def sphere_intersect(center, radius, ray_origin, ray_direction) -> Optional[float]:
    """
    :param center:
    :param radius:
    :param ray_origin: point
    :param ray_direction: vector
    :return: None if line do not intersect with sphere and nearest point of intersection otherwise
    """
    b = 2 * np.dot(ray_direction, ray_origin - center)
    c = np.linalg.norm(ray_origin - center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None


def nearest_intersected_object(objects, ray_origin, ray_direction) -> Tuple[Optional[Figure], float]:
    """
    Function that return nearest object that intersects with casted ray
    :param objects: (spheres)
    :param ray_origin:
    :param ray_direction:
    :return: object and distance (may be None)
    """
    distances = [sphere_intersect(obj.center, obj.radius, ray_origin, ray_direction) for obj in objects]
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = objects[index]
    return nearest_object, min_distance


def get_image(width, height, max_depth) -> np.array:
    # let's consider screen is located 1 unit from camera
    # and camera always look parallel to horizon
    distance_from_camera_to_screen = 1
    camera_angle = 45

    camera = np.array([0, 1, 0])
    camera_direction_vector = np.array([0, -distance_from_camera_to_screen, 0])
    screen_center = camera + camera_direction_vector
    ratio = float(width) / height
    screen = (
        (screen_center - distance_from_camera_to_screen)[0], distance_from_camera_to_screen / ratio,
        (screen_center + distance_from_camera_to_screen)[0],
        -(distance_from_camera_to_screen / ratio))  # left, top, right, bottom

    light = Light(np.array([-5, 5, 5]), WHITE, WHITE, WHITE)

    objects = [
        Sphere(np.array([-1, -1.5, -0.3]), 0.7, Material(RED, LIGHT_RED, WHITE, 100, 0.5)),
        Sphere(np.array([0.1, 0.3, 0]), 0.1, Material(PURPLE, LIGHT_PURPLE, WHITE, 100, 0.5)),
        Sphere(np.array([0.3, 0, 0]), 0.15, Material(GREEN, LIGHT_GREEN, WHITE, 100, 0.5)),
        Sphere(np.array([0, 0, -9000]), 9000 - 0.7, Material(GREY, LIGHT_GREY, WHITE, 100, 0.5)),
    ]

    image = np.zeros((height, width, 3))
    for i, z in enumerate(np.linspace(screen[1], screen[3], height)):
        for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
            pixel = np.array([x, 0, z])
            origin = camera
            direction_vector = normalize(pixel - origin)

            color = np.zeros(3)
            reflection = 1

            for k in range(max_depth):
                # check for intersections
                nearest_object, min_distance = nearest_intersected_object(objects, origin, direction_vector)
                if nearest_object is None:
                    break

                intersection = origin + min_distance * direction_vector
                normal_to_surface = normalize(intersection - nearest_object.center)
                shifted_point = intersection + 1e-5 * normal_to_surface
                intersection_to_light_vector = normalize(light.position - shifted_point)

                _, min_distance = nearest_intersected_object(objects, shifted_point, intersection_to_light_vector)
                intersection_to_light_distance = np.linalg.norm(light.position - intersection)
                is_shadowed = min_distance < intersection_to_light_distance

                if is_shadowed:
                    break

                illumination = np.zeros((3))

                # Blinn-Phong model calculation:

                # ambient
                illumination += nearest_object.material.ambient * light.ambient

                # diffuse
                illumination += nearest_object.material.diffuse * light.diffuse * np.dot(
                    intersection_to_light_vector,
                    normal_to_surface)

                # specular
                intersection_to_camera_vector = normalize(camera - intersection)
                vectors_sum = normalize(intersection_to_light_vector + intersection_to_camera_vector)
                illumination += nearest_object.material.specular * light.specular * np.dot(normal_to_surface,
                                                                                           vectors_sum) ** (
                                        nearest_object.material.shininess / 4)

                # reflection
                color += reflection * illumination
                reflection *= nearest_object.material.reflection

                origin = shifted_point
                direction_vector = reflected(direction_vector, normal_to_surface)
                image[i, j] = np.clip(color, 0, 1)
        print("progress: %d/%d" % (i + 1, height))
    return image


def draw_image(pygame_screen, angle, width, height):
    max_depth = 3
    distance_from_camera_to_screen = 1
    camera_angle = 45

    camera = np.array([0, 1, 0])
    x = distance_from_camera_to_screen * cos(radians(angle))
    y = distance_from_camera_to_screen * sin(radians(angle))
    camera_direction_vector = np.array([x, y, 0])
    screen_center = camera + camera_direction_vector
    ratio = float(width) / height
    screen = (
        (screen_center - distance_from_camera_to_screen)[0], distance_from_camera_to_screen / ratio,
        (screen_center + distance_from_camera_to_screen)[0],
        -(distance_from_camera_to_screen / ratio))  # left, top, right, bottom

    light = Light(np.array([-5, 5, 5]), WHITE, WHITE, WHITE)

    objects = [
        Sphere(np.array([-1, -1.5, -0.3]), 0.7, Material(RED, LIGHT_RED, WHITE, 100, 0.5)),
        Sphere(np.array([0.1, 0.3, 0]), 0.1, Material(PURPLE, LIGHT_PURPLE, WHITE, 100, 0.5)),
        Sphere(np.array([0.3, 0, 0]), 0.15, Material(GREEN, LIGHT_GREEN, WHITE, 100, 0.5)),
        Sphere(np.array([0, 0, -9000]), 9000 - 0.7, Material(GREY, LIGHT_GREY, WHITE, 100, 0.5)),
    ]

    image = np.zeros((height, width, 3))
    for i, z in enumerate(np.linspace(screen[1], screen[3], height)):
        for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
            pixel = np.array([x, 0, z])
            origin = camera
            direction_vector = normalize(pixel - origin)

            color = np.zeros(3)
            reflection = 1

            for k in range(max_depth):
                # check for intersections
                nearest_object, min_distance = nearest_intersected_object(objects, origin, direction_vector)
                if nearest_object is None:
                    break

                intersection = origin + min_distance * direction_vector
                normal_to_surface = normalize(intersection - nearest_object.center)
                shifted_point = intersection + 1e-5 * normal_to_surface
                intersection_to_light_vector = normalize(light.position - shifted_point)

                _, min_distance = nearest_intersected_object(objects, shifted_point, intersection_to_light_vector)
                intersection_to_light_distance = np.linalg.norm(light.position - intersection)
                is_shadowed = min_distance < intersection_to_light_distance

                if is_shadowed:
                    break

                illumination = np.zeros((3))

                # Blinn-Phong model calculation:

                # ambient
                illumination += nearest_object.material.ambient * light.ambient

                # diffuse
                illumination += nearest_object.material.diffuse * light.diffuse * np.dot(
                    intersection_to_light_vector,
                    normal_to_surface)

                # specular
                intersection_to_camera_vector = normalize(camera - intersection)
                vectors_sum = normalize(intersection_to_light_vector + intersection_to_camera_vector)
                illumination += nearest_object.material.specular * light.specular * np.dot(normal_to_surface,
                                                                                           vectors_sum) ** (
                                        nearest_object.material.shininess / 4)

                # reflection
                color += reflection * illumination
                reflection *= nearest_object.material.reflection

                origin = shifted_point
                direction_vector = reflected(direction_vector, normal_to_surface)
                image[i, j] = np.clip(color, 0, 1)
                converted_color = convert_norm_to_rgb(color)
                print(list(converted_color))
                gfxdraw.pixel(pygame_screen, i, j, list(converted_color))


if __name__ == "__main__":
    width = 50
    height = 50
    max_depth = 3
    image = get_image(width, height, max_depth)
    plt.imsave('image.png', image)
