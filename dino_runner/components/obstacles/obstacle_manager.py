import pygame
import random
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD

class ObstacleManager:

    def __init__(self):
        self.obstacles = []
        self.death_sound = pygame.mixer.Sound("death_sound.wav")

    def update(self, game):
        if len(self.obstacles) == 0:
            obstacle_option = random.randint(0,2)
            if (obstacle_option == 0):
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif (obstacle_option == 1):
                self.obstacles.append(Cactus(LARGE_CACTUS))
            elif (obstacle_option == 2):
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(70)
                self.death_sound.play()

                if not game.player.shield:
                    self.obstacles = []
                    game.player_heart_manager.reduce_heart()

                    if game.player_heart_manager.heart_count > 0:
                        game.player.shield = True
                        game.player.show_text = False

                    else:
                        pygame.time.delay(1000)
                        game.playing = False
                        game.death_count += 1
                        break
                else:
                    self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []