import pygame
import pygame.freetype

from attributes.constants import *
from attributes.locations import *
from level_editor.editor_option import EditorOption
from objects.collider import Collider
from utils.yaml_worker import save_yaml_file, initialize_colliders


class Editor:

    def __init__(self, screen: pygame.Surface, level_index: int):
        self.level_index = level_index
        self.level_name = f"level{self.level_index}"
        self.screen = screen
        self.running = True
        self.chosen_first_rect_button_pos = None
        self.state = EditorOption.RECT_DRAWING
        self.colliders = initialize_colliders()
        print(self.colliders)
        print(self.colliders[0].rect)

    def start(self):
        while self.running:
            self.screen.blit(FIRST_LOCATION_BACKGROUND, (0, 0))
            for event in pygame.event.get():
                self.handle_event(event)
            if self.chosen_first_rect_button_pos is not None:
                pygame.draw.rect(self.screen, GREEN, self.get_drawn_rectangle())
            for collider in self.colliders:
                pygame.draw.rect(self.screen, BLUE, collider.rect)
            pygame.display.update()
        self.save_result_to_file()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            self.handle_key_down_event(event)
        elif event.type == pygame.KEYUP:
            self.handle_key_up_event(event)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion_event()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down_event()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up_event()

    def handle_key_down_event(self, event: pygame.event.Event):
        if event.key == pygame.K_ESCAPE:
            self.running = False
        if event.key == ord('c'):
            print("DRAWING RECTANGLES")
            self.state = EditorOption.RECT_DRAWING

    def handle_key_up_event(self, event: pygame.event.Event):
        print(f"Key: {event.key} up")

    def handle_mouse_motion_event(self):
        return 1

    def handle_mouse_down_event(self):
        if self.state == EditorOption.RECT_DRAWING:
            self.chosen_first_rect_button_pos = pygame.mouse.get_pos()

    def handle_mouse_up_event(self):
        if self.chosen_first_rect_button_pos is not None:
            self.colliders.append(Collider.from_rect(self.get_drawn_rectangle()))
            self.chosen_first_rect_button_pos = None

    def get_drawn_rectangle(self) -> pygame.Rect:
        x = min(self.chosen_first_rect_button_pos[0], pygame.mouse.get_pos()[0])
        y = min(self.chosen_first_rect_button_pos[1], pygame.mouse.get_pos()[1])
        width = abs(pygame.mouse.get_pos()[0] - x)
        height = abs(pygame.mouse.get_pos()[1] - y)
        return pygame.Rect(x, y, width, height)

    def save_result_to_file(self):
        colliders = []
        for collider in self.colliders:
            current_collider_rect = collider.rect
            colliders.append({"collider": {"x": current_collider_rect.x, "y": current_collider_rect.y,
                                               "width": current_collider_rect.width,
                                               "height": current_collider_rect.height}})
        save_yaml_file(f"levels/{self.level_name}", colliders)
