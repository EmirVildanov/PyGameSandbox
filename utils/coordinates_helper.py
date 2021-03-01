from attributes.constants import *
from objects.bullet import Bullet
from src.intersect_coordinator import is_segment_intersect_rect


def get_rectangle_coordinates(x, y, width, height):
    return [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]


def find_button_coordinates(button_x, buttons_y, button_width, button_height):
    p1 = (button_x, buttons_y)
    p2 = (button_x + button_width, buttons_y)
    p3 = (button_x + button_width, buttons_y + button_height)
    p4 = (button_x, buttons_y + button_height)
    return [p1, p2, p3, p4]


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
