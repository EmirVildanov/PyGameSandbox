from attributes.constants import *
from objects.bullet import Bullet
from utils.intersect_coordinator import is_segment_intersect_rect


def rect_coordinates_from_wh(x, y, width, height):
    return [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]


def rect_coordinates(rect: pygame.Rect):
    return [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]


def is_outside_screen(object):
    if object.rect.x <= 0 or object.rect.x >= CAMERA_WIDTH or object.rect.y <= 0 or object.rect.y >= CAMERA_HEIGHT:
        return True
    return False


def is_collide_collider(rect: pygame.Rect, collider, x, y):
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


def line_intersection(line1, line2):
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


def line_rect_intersection(line, rect_coordinates):
    for i in range(4):
        current_intersection = line_intersection(line, (rect_coordinates[i], rect_coordinates[(i + 1) % 4]))
        if current_intersection is not None:
            return current_intersection
    return None
