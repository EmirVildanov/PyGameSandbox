import pygame
import yaml
from yaml import load, dump

from objects.collider import Collider

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def read_yaml_file(file_path):
    stream = open(file_path, 'r')
    elements = load(stream, Loader=Loader)
    return elements


def save_yaml_file(file_name, data_list):
    with open(f'{file_name}.yaml', 'w') as f:
        yaml.dump(data_list, f)


def initialize_colliders():
    colliders_list = []
    for block_element in read_yaml_file(f"levels/level1.yaml"):
        for k, v in block_element.items():
            colliders_list.append(Collider(v["x"], v["y"], v["width"], v["height"]))
    return colliders_list
