from math import cos, radians, sin, ceil
from typing import Tuple

from attributes.constants import *
from attributes.locations import FIRST_LOCATION_WIDTH, FIRST_LOCATION_HEIGHT
from utils.coordinates_helper import is_bullet_collide_collider, is_outside_screen, get_rect_coordinates, \
    segment_rect_intersection, find_nearest_point, find_distance_between_points
from utils.intersect_coordinator import get_segment_circle_intersection


class PygameView:
    # НАДО ПЕРЕДАТЬ screen ОТ Game К PygameView
    def __init__(self, game):
        super().__init__()
        self.game = game

    def notify(self):
        if self.game.level_index == 1:
            self.draw_level_1()
        elif self.game.level_index == 2:
            self.draw_level_2()
        elif self.game.level_index == 3:
            self.draw_level_3()

    def draw_level_1(self):
        self.game.player.update()
        self.game.camera.update(self.game.player)
        self.game.screen.blit(self.game.background, (-self.game.camera.rect.x, -self.game.camera.rect.y))
        for bullet in self.game.bullet_list:
            bullet.update()
            if is_bullet_collide_collider(bullet):
                BULLET_METAL_HIT_SOUND.play()
                self.game.bullet_list.remove(bullet)
            if is_outside_screen(bullet):
                self.game.bullet_list.remove(bullet)
        self.game.screen.blit(self.game.player.image, self.game.camera.apply(self.game.player))
        self.game.bullet_list.draw(self.game.screen)
        pygame.draw.line(self.game.screen, BLACK, self.game.camera.apply(self.game.player).center,
                         pygame.mouse.get_pos())
        pygame.display.update()

    def draw_level_2(self):
        self.game.player.update()
        self.game.camera.update(self.game.player)
        self.game.screen.fill(BLACK)
        radar = self.game.player.rect.center
        screen_rectangle = pygame.Rect(0, 0, FIRST_LOCATION_WIDTH, FIRST_LOCATION_HEIGHT)
        radar_intersection_points = self.get_radar_intersection_points(radar, screen_rectangle)
        # screen_rectangle = self.game.screen.get_rect()
        for i, point in enumerate(radar_intersection_points):
            next_point = radar_intersection_points[(i + 1) % len(radar_intersection_points)]
            point = self.game.camera.apply_point(point)
            radar = self.game.camera.apply_point(radar)
            next_point = self.game.camera.apply_point(next_point)
            pygame.draw.polygon(self.game.screen, WHITE, [point, radar, next_point], width=0)
        for collider in self.game.colliders_list:
            pygame.draw.rect(self.game.screen, BLACK, self.game.camera.apply_rect(collider.rect))
        self.game.screen.blit(self.game.player.image, self.game.camera.apply(self.game.player))
        pygame.display.update()

    def get_radar_intersection_points(self, radar, screen_rectangle):
        radar_intersection_points = []
        for i in range(0, 361, 10):
            x = radar[0] + cos(radians(i)) * RADAR_LENGTH
            y = radar[1] + sin(radians(i)) * RADAR_LENGTH
            line_point = (radar[0] + cos(radians(i)) * RADAR_LENGTH, radar[1] + sin(radians(i)) * RADAR_LENGTH)
            radar_line = (self.game.player.rect.center, line_point)
            colliders_intersection_points = set()
            for collider in self.game.colliders_list:
                current_intersection_points = segment_rect_intersection(radar_line,
                                                                        get_rect_coordinates(collider.rect))
                colliders_intersection_points.update(current_intersection_points)
            colliders_intersection_points.update(
                segment_rect_intersection(radar_line, get_rect_coordinates(screen_rectangle)))
            best_point = find_nearest_point(radar, colliders_intersection_points)
            best_point_vector = (best_point[0] - radar[0], best_point[1] - radar[1])
            best_point_length = find_distance_between_points(best_point, radar)
            best_point_vector = (best_point_vector[0] / best_point_length, best_point_vector[1] / best_point_length)
            best_point_vector = (best_point_vector[0] * 200, best_point_vector[1] * 200)
            circle_best_point = (radar[0] + best_point_vector[0], radar[1] + best_point_vector[1])
            circle_point_distance = find_distance_between_points(radar, circle_best_point)
            best_point_distance = find_distance_between_points(radar, best_point)
            if circle_point_distance < best_point_distance:
                radar_intersection_points.append(circle_best_point)
            else:
                radar_intersection_points.append(best_point)
            # if best_point is not None:
            #     ...
            #     # pygame.draw.line(self.game.screen, BLACK, radar, best_point)
            #     # pygame.draw.circle(self.game.screen, GREEN, best_point, 5)
            # else:
            #     print("Error")
            #     pygame.draw.line(self.game.screen, RED, radar, (x, y))
        return radar_intersection_points

    def draw_level_3(self):
        self.game.player.update()
        self.game.camera.update(self.game.player)
        # self.game.screen.fill(WHITE)
        self.game.screen.fill(WHITE, (0, 0, CAMERA_WIDTH, CAMERA_HEIGHT / 2))
        self.game.screen.fill(GREEN, (0, CAMERA_HEIGHT / 2, CAMERA_WIDTH, CAMERA_HEIGHT / 2))
        radar = self.game.player.rect.center
        screen_rectangle = self.game.screen.get_rect()
        radar_intersection_points_pairs, middle_point = self.get_radar_intersection_pairs(radar, screen_rectangle)
        radar_intersection_points = list(radar_intersection_points_pairs.keys())

        self.draw_visible_walls(radar, radar_intersection_points, radar_intersection_points_pairs, middle_point)
        # self.draw_visible_circle(radar, radar_intersection_points, middle_point)
        pygame.display.update()

    def draw_visible_walls(self, radar, radar_intersection_points, radar_intersection_points_pairs, middle_point):
        for angle in range(45, 135, 1):
            point_index = angle - 45
            current_point = radar_intersection_points[point_index]
            current_point_distance = radar_intersection_points_pairs[current_point]
            current_point_x = (CAMERA_WIDTH / 90) * point_index
            if abs(cos(radians(90 - angle))) != 0:
                # print(f"Abs: {abs(cos(radians(90 - angle)))}")
                current_point_distance = current_point_distance * abs(cos(radians(90 - angle)))
                current_line_height = (1 / current_point_distance) * 50000
            else:
                current_line_height = (1 / current_point_distance) * 50000
            # print(f"angle {angle} -> distance -> {current_point_distance}")
            # current_line_height = (1 / current_point_distance) * 50000
            current_point_y = CAMERA_HEIGHT / 2 + current_line_height / 2
            next_point = radar_intersection_points[(point_index + 1) % len(radar_intersection_points)]
            next_point_x = (CAMERA_WIDTH / 90) * ((point_index + 1) % len(radar_intersection_points))
            next_point_distance = radar_intersection_points_pairs[next_point]
            # pygame.draw.line(self.game.screen, BLACK, (current_point_x, current_point_y),
            #                  (current_point_x, current_point_y - current_line_height))
            current_wall_rect = pygame.Rect(current_point_x, int(current_point_y - current_line_height), int(next_point_x - current_point_x), int(current_line_height))
            pygame.draw.rect(self.game.screen, BLACK, current_wall_rect)
            pygame.draw.rect(self.game.screen, BLACK, current_wall_rect, 2)
        self.draw_player_hand()
        # exit(1)

    def draw_player_hand(self):
        cadr = self.game.player.cadr / 100
        bob_x = cos(cadr * 2) * 3 * 6
        bob_y = sin(cadr * 4) * 3 * 6
        # bob_x = 1
        # bob_y = 1
        left = CAMERA_WIDTH * 0.56 + bob_x
        top = CAMERA_HEIGHT * 0.65 + bob_y
        self.game.screen.blit(self.game.player.knife_image, (left, top))

    def draw_visible_circle(self, radar, radar_intersection_points, middle_point):
        for i, point in enumerate(radar_intersection_points):
            next_point = radar_intersection_points[(i + 1) % len(radar_intersection_points)]
            pygame.draw.polygon(self.game.screen, WHITE, [point, radar, next_point], width=0)
        for collider in self.game.colliders_list:
            pygame.draw.rect(self.game.screen, BLACK, collider.rect)
        pygame.draw.line(self.game.screen, BLACK, self.game.player.rect.center, middle_point)
        self.game.screen.blit(self.game.player.image, self.game.player)
        player_rect = self.game.player.rect
        arc_rect = pygame.Rect(player_rect.topleft[0] - 10, player_rect.topleft[1] - 10, 20 + player_rect.width, 20 + player_rect.height)
        arc_start_angle = self.game.first_person_mouse_angle
        arc_finish_angle = self.game.first_person_mouse_angle + 180
        pygame.draw.arc(self.game.screen, BLUE, arc_rect, -radians(arc_start_angle), -radians(arc_finish_angle), width=1)

    def get_radar_intersection_pairs(self, radar, screen_rectangle) -> Tuple[dict, Tuple[float, float]]:
        radar_intersection_pairs = {}
        angle_range = range(self.game.first_person_mouse_angle - 180, self.game.first_person_mouse_angle + 1)
        angle_range = range(self.game.first_person_mouse_angle - 180 + 45, self.game.first_person_mouse_angle - 45 + 1)
        for i in angle_range:
            line_point = (radar[0] + cos(radians(i)) * RADAR_LENGTH, radar[1] + sin(radians(i)) * RADAR_LENGTH)
            radar_line = (self.game.player.rect.center, line_point)
            colliders_intersection_points = set()
            for collider in self.game.colliders_list:
                current_intersection_points = segment_rect_intersection(radar_line,
                                                                        get_rect_coordinates(collider.rect))
                colliders_intersection_points.update(current_intersection_points)
            colliders_intersection_points.update(
                segment_rect_intersection(radar_line, get_rect_coordinates(screen_rectangle)))
            best_point = find_nearest_point(radar, colliders_intersection_points)
            # best_point_vector = (best_point[0] - radar[0], best_point[1] - radar[1])
            # best_point_length = find_distance_between_points(best_point, radar)
            # best_point_vector = (best_point_vector[0] / best_point_length, best_point_vector[1] / best_point_length)
            # best_point_vector = (best_point_vector[0] * 200, best_point_vector[1] * 200)
            # circle_best_point = (radar[0] + best_point_vector[0], radar[1] + best_point_vector[1])
            # circle_point_distance = find_distance_between_points(radar, circle_best_point)
            # best_point_distance = find_distance_between_points(radar, best_point)
            # if circle_point_distance < best_point_distance:
            #     radar_intersection_pairs.update({circle_best_point: circle_point_distance})
            # else:
            #     radar_intersection_pairs.update({best_point: best_point_distance})
            if i == self.game.first_person_mouse_angle - 90:
                middle_point = best_point
            best_point_distance = find_distance_between_points(radar, best_point)
            # if int(best_point_distance * cos(radians(i))) != 0:
            #     best_point_distance = int(best_point_distance * cos(radians(i)))
            radar_intersection_pairs.update({best_point: best_point_distance})
            # radar_intersection_pairs.update({best_point: best_point_distance})
        return radar_intersection_pairs, middle_point

