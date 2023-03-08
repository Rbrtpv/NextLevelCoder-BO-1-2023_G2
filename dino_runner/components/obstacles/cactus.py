import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import LARGE_CACTUS, SMALL_CACTUS

class Cactus(Obstacle):
    large_cactus_y = 305
    small_cactus_y = 330

    def __init__(self, image_list):
        self.type = random.randint(0, 2)
        super().__init__(image_list, self.type)
        if image_list == LARGE_CACTUS:
            self.rect.y = self.large_cactus_y
        elif image_list == SMALL_CACTUS:
            self.rect.y = self.small_cactus_y