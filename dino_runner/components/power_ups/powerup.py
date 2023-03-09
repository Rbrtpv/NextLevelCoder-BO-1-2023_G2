import random
from pygame.sprite import Sprite
from dino_runner.utils.constants import SCREEN_WIDTH

class PowerUp(Sprite):
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(100, 300)

    def update(self, game_speed, powerups_list):
        self.rect.x -= game_speed

        if self.rect.x <= 0:
            powerups_list.pop()

    def draw(self, screen):
        screen.blit(self.image, self.rect)