import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import (
    RUNNING,
    DUCKING,
    JUMPING,
    DEFAULT_TYPE,
    SHIELD_TYPE,
    RUNNING_SHIELD,
    DUCKING_SHIELD,
    JUMPING_SHIELD
)

class Dinosaur(Sprite):
    POS_X = 80
    POS_Y = 310
    POS_Y_DUCKING = 345
    JUMP_VEL = 8.5

    def __init__(self):
      self.run_img = {
            DEFAULT_TYPE: RUNNING,
            SHIELD_TYPE: RUNNING_SHIELD
        }
      self.duck_img = {
            DEFAULT_TYPE: DUCKING,
            SHIELD_TYPE: DUCKING_SHIELD
        }
      self.jump_img = {
            DEFAULT_TYPE: JUMPING,
            SHIELD_TYPE: JUMPING_SHIELD
        }
      self.type = DEFAULT_TYPE

      self.image = self.run_img[self.type][0]
      self.dino_rect = self.image.get_rect()
      self.dino_rect.x = self.POS_X
      self.dino_rect.y = self.POS_Y
      self.step_index = 0
      self.dino_running = True
      self.dino_ducking = False
      self.dino_jumping = False
      self.jump_vel = self.JUMP_VEL
      self.jump_sound = pygame.mixer.Sound("jump.wav")

      self.setup_state_booleans()

    def setup_state_booleans(self):
        self.has_powerup = False
        self.shield = False
        self.show_text = False
        self.shield_time_up = 0

    def update(self, user_input):
      if self.dino_running:
        self.run()
      elif self.dino_jumping:
        self.jump()
      elif self.dino_ducking:
        self.duck()

      if user_input[pygame.K_DOWN] and not self.dino_jumping:
        self.dino_running = False
        self.dino_jumping = False
        self.dino_ducking = True

      elif user_input[pygame.K_UP] and not self.dino_jumping:
        self.jump_sound.play()
        self.dino_running = False
        self.dino_jumping = True
        self.dino_ducking = False

      elif not self.dino_jumping:
        self.dino_running = True
        self.dino_jumping = False
        self.dino_ducking = False

      if self.step_index >= 10:
        self.step_index = 0

    def draw(self, screen):
      screen.blit(self.image, self.dino_rect)

    def run(self):
      self.image = self.run_img[self.type][self.step_index//5]
      self.dino_rect = self.image.get_rect()
      self.dino_rect.x = self.POS_X
      self.dino_rect.y = self.POS_Y
      self.step_index += 1

    def jump(self):
      self.image = self.jump_img[self.type]
      if self.dino_jumping:
        self.dino_rect.y -= self.jump_vel * 4
        self.jump_vel -= 0.8
      if self.jump_vel < -self.JUMP_VEL:
        self.dino_rect.y = self.POS_Y
        self.dino_jumping = False
        self.jump_vel = self.JUMP_VEL

    def duck(self):
      self.image = self.duck_img[self.type][self.step_index//5]
      self.dino_rect = self.image.get_rect()
      self.dino_rect.x = self.POS_X
      self.dino_rect.y = self.POS_Y_DUCKING
      self.step_index += 1

    def check_invincibility(self):
        if self.shield:
            time_to_show = round((self.shield_time_up - pygame.time.get_ticks())/1000, 2)
            if time_to_show >= 0:
                #show remaining time
                pass
            else:
                self.shield = False
                self.update_to_default(SHIELD_TYPE)

    def update_to_default(self, current_type):
        if self.type == current_type:
            self.type = DEFAULT_TYPE