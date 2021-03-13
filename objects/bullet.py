from attributes.constants import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.move_x = 0
        self.move_y = 0
        image = PLAYER_IMAGE.convert()
        image = pygame.transform.scale(image, (10, 10))
        image.convert_alpha()  # optimise alpha
        image.set_colorkey(ALPHA_WHITE)  # set alpha
        self.image = image
        self.rect = self.image.get_rect()

    def control(self, x, y):
        self.move_x = x
        self.move_y = y

    def update(self):
        self.rect.x = self.rect.x + self.move_x
        self.rect.y = self.rect.y + self.move_y