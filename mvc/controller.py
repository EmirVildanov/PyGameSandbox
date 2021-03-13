import pygame

from attributes.constants import *
from mvc.view import PygameView
from mvc.event import EventManager, Event, TickEvent, QuitEvent


class Controller:
    """this is a superclass for any controllers that might subscribe on Event updates"""

    def __init__(self):
        self.name = "Generic Controller"


class KeyboardController(Controller):
    def __init__(self, game, event_manager: EventManager):
        super().__init__()
        self.game = game
        self.event_manager = event_manager
        self.pressed_movement_buttons_list = []

    def notify(self, event: Event):
        if isinstance(event, TickEvent):
            event_type = event.pygame_event.type
            if event_type == pygame.KEYDOWN:
                self.handle_key_down_event(event.pygame_event)
            elif event_type == pygame.KEYUP:
                self.handle_key_up_event(event.pygame_event)

    @staticmethod
    def is_movement_event_key(key):
        if key == pygame.K_LEFT or key == pygame.K_RIGHT or key == pygame.K_DOWN or key == pygame.K_UP:
            return True
        elif key == ord('a') or key == ord('d') or key == ord('s') or key == ord('w'):
            return True
        return False

    def handle_key_down_event(self, event: pygame.event.Event):
        if event.key == pygame.K_ESCAPE:
            self.event_manager.post(QuitEvent())
        elif self.is_movement_event_key(event.key):
            if len(self.pressed_movement_buttons_list) == 0:
                SNOW_WALK_SOUND.play()
            key = event.key
            if key == pygame.K_LEFT or key == ord('a'):
                wanted_movement = (-ONE_STEP_IN_PX, 0)
            elif key == pygame.K_RIGHT or key == ord('d'):
                wanted_movement = (ONE_STEP_IN_PX, 0)
            elif key == pygame.K_UP or key == ord('w'):
                wanted_movement = (0, -ONE_STEP_IN_PX)
            else:
                wanted_movement = (0, ONE_STEP_IN_PX)
            self.pressed_movement_buttons_list.append(key)
            self.game.control_player(wanted_movement)

    def handle_key_up_event(self, event: pygame.event.Event):
        if self.is_movement_event_key(event.key):
            key = event.key
            if key in self.pressed_movement_buttons_list:
                if key == pygame.K_LEFT or key == ord('a'):
                    wanted_movement = (ONE_STEP_IN_PX, 0)
                elif key == pygame.K_RIGHT or key == ord('d'):
                    wanted_movement = (-ONE_STEP_IN_PX, 0)
                elif key == pygame.K_UP or key == ord('w'):
                    wanted_movement = (0, ONE_STEP_IN_PX)
                else:
                    wanted_movement = (0, -ONE_STEP_IN_PX)
                self.pressed_movement_buttons_list.remove(key)
                if len(self.pressed_movement_buttons_list) == 0:
                    SNOW_WALK_SOUND.stop()
                self.game.control_player(wanted_movement)


class MouseController(Controller):
    def __init__(self, game: 'Game', event_manager: EventManager):
        super().__init__()
        self.game = game
        self.event_manager = event_manager

    def notify(self, event: Event):
        if isinstance(event, TickEvent):
            pygame_event = event.pygame_event
            pygame_event_type = pygame_event.type
            if pygame_event_type == pygame.MOUSEMOTION:
                self.handle_mouse_motion_event(event)
            elif pygame_event_type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down_event()

    def handle_mouse_motion_event(self, event: Event):
        pygame_event = event.pygame_event
        print(f"FPAngle :{self.game.first_person_mouse_angle}")
        if self.game.level_index == 3:
            sensivity = 4
            if pygame_event.rel[0] < 0:
                x_diff = -sensivity
            else:
                x_diff = +sensivity
            current_position = (self.game.first_person_mouse_angle + x_diff) % 360
            self.game.first_person_mouse_angle = current_position

    def handle_mouse_down_event(self):
        if self.game.level_index == 1:
            self.game.shot_bullet()


class CPUSpinnerController(Controller):
    def __init__(self, game, pygame_view: PygameView, event_manager: EventManager):
        super().__init__()
        self.keepGoing: bool = True
        self.clock = pygame.time.Clock()
        self.view = pygame_view
        self.game = game
        self.event_manager = event_manager

    def run(self):
        while self.keepGoing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.event_manager.post(QuitEvent())
                self.game.check_collisions()
                self.event_manager.post(TickEvent(event))
            self.view.notify()
            self.clock.tick(FPS)

    def notify(self, event: Event):
        if isinstance(event, QuitEvent):
            self.keepGoing = False