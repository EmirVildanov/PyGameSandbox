import pygame


def is_movement_event_key(key):
    if key == pygame.K_LEFT or key == pygame.K_RIGHT or key == pygame.K_DOWN or key == pygame.K_UP:
        return True
    elif key == ord('a') or key == ord('d') or key == ord('s') or key == ord('w'):
        return True
    return False
