import random
from dino_runner.components.obstacles.obstacle import Obstacle

class Bird(Obstacle):
    def __init__(self, image_list):
        self.type = random.randint(0,1)
        super().__init__(image_list, self.type)
        self.rect.y = random.randint(100,315)
        self.index = 0

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image_list[self.index//5], self.rect)
        self.index += 1