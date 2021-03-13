from math import sqrt
from typing import Tuple, Optional, List, Set

from attributes.constants import *
from objects.bullet import Bullet
from utils.intersect_coordinator import is_segment_intersect_rect, get_segment_intersection


def find_distance_between_points(point1: Tuple[float, float], point2: Tuple[float, float]):
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def rect_coordinates_from_wh(x, y, width, height):
    return [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]


def get_rect_coordinates(rect: pygame.Rect):
    return [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]


def is_outside_screen(object):
    if object.rect.x <= 0 or object.rect.x >= CAMERA_WIDTH or object.rect.y <= 0 or object.rect.y >= CAMERA_HEIGHT:
        return True
    return False


def is_collide_rect_with_xy(rect: pygame.Rect, collider, x, y):
    with_move_coordinates_player_rect_x = rect.x + x
    with_move_coordinates_player_rect_y = rect.y + y
    with_move_rect = pygame.rect.Rect(with_move_coordinates_player_rect_x,
                                      with_move_coordinates_player_rect_y,
                                      rect.width,
                                      rect.height)
    return collider.rect.colliderect(with_move_rect)


def is_bullet_collide_collider(bullet: Bullet) -> bool:
    for collider in bullet.colliders:
        if is_segment_intersect_rect(bullet.rect.topleft, (
        bullet.rect.x + bullet.move_x, bullet.rect.y + bullet.move_y), collider.rect):
            return True
    return False


def line_intersection(line1, line2) -> Optional[Tuple[float, float]]:
    """
    :param line1: line1 coordinates Tuple
    :param line2: line2 coordinates Tuple
    :return: the point Tuple of intersection of None
    """
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def line_rect_intersection(line, rect_coordinates: Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float], Tuple[float, float]]):
    for i in range(4):
        current_intersection = line_intersection(line, (rect_coordinates[i], rect_coordinates[(i + 1) % 4]))
        if current_intersection is not None:
            return current_intersection
    return None


def segment_rect_intersection(segment, rect_coordinates) -> List[Tuple[float, float]]:
    intersection_points = []
    for i in range(4):
        current_intersection = get_segment_intersection(segment[0], segment[1], rect_coordinates[i], rect_coordinates[(i + 1) % 4])
        if current_intersection is not None:
            intersection_points.append(current_intersection)
    return intersection_points


def find_nearest_point(start_point: Tuple[float, float], points: Set[Tuple[float, float]]) -> Tuple[float, float]:
    min_distance = None
    best_point = None
    for point in points:
        current_distance = find_distance_between_points(start_point, point)
        if min_distance is None or current_distance < min_distance:
            min_distance = current_distance
            best_point = point
    return best_point
