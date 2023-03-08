from pygame.sprite import Sprite
from dino_runner.utils.constants import SCREEN_WIDTH

class Obstacle(Sprite):

    def __init__(self, image_list, type):
        self.image_list = image_list
        self.type = type
        self.rect = image_list[type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if self.rect.x <= 0:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image_list[self.type], self.rect)