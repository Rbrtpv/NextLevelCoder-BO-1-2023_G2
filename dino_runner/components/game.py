import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.text_utils import TextUtils
from dino_runner.components.player_hearts.player_heart_manager import PlayerHeartManager
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import BG, CLOUD, COLORS, DINO_DEAD, DINO_START, END_SCREEN, ICON, MENU, RESET, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.multiple_of_100 = False
        self.playing = False
        self.game_running = True

        self.death_count = 0
        self.game_speed = 20
        self.points = 0
        self.best_score = 0

        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.player = Dinosaur()
        self.text_utils = TextUtils()
        self.player_heart_manager = PlayerHeartManager()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

        pygame.mixer.music.load("Running-About.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        self.points_sound = pygame.mixer.Sound("point.wav")
        self.points_sound.set_volume(0.5)

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.points = 0
        self.create_comment()
        self.player_heart_manager.reset_hearts()
        self.power_up_manager.reset_power_ups(self.points)
        self.obstacle_manager.reset_obstacles()
        
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        self.player.update(pygame.key.get_pressed())
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.player)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill(COLORS["white"])
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.player_heart_manager.draw(self.screen)
        self.score()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(CLOUD,(image_width + self.x_pos_bg, 125))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.screen.blit(CLOUD,(image_width + self.x_pos_bg, 125))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
    def create_comment(self):
        self.power_up_manager.reset_power_ups(self.points)

    def score(self):
        self.points += 0.5

        if self.points % 100 == 0 and self.points >= 0 and not self.multiple_of_100:
            self.points_sound.play()
            self.game_speed += 1
            self.multiple_of_100 = True

        elif int(self.points) % 100 != 0:
            self.multiple_of_100 = False

        score, score_rect = self.text_utils.get_score(int(self.points))
        self.screen.blit(score, score_rect)

        self.player.check_invincibility(self.screen)

    def show_menu(self, death_count = 0):
        self.game_running = True
        self.screen.fill(COLORS["white"])

        self.print_menu_elements(self.death_count if death_count == 0 else death_count)

        pygame.display.update()
        self.handle_key_events()

    def print_menu_elements(self, death_count = 0):
        half_screen_height = SCREEN_HEIGHT //2
        half_screen_width = SCREEN_WIDTH //2

        if self.death_count == 0:
            self.screen.blit(MENU,(0,0))
            text, text_rect = self.text_utils.get_centered_message("Press any Key to start",height = half_screen_height + 20)
            self.screen.blit(text, text_rect)
            self.screen.blit(DINO_START[0], (half_screen_width-300, half_screen_height-50))

        elif self.death_count >= 1:
            self.screen.blit(END_SCREEN,(0,0))
            self.update_best_score()
            text, text_rect = self.text_utils.get_centered_message("Press any Key to Restart")
            score, score_rect = self.text_utils.get_centered_message(f"Your Current Score: {str(int(self.points))}", height=half_screen_height + 50)
            best_score, best_score_rect = self.text_utils.get_centered_message(f"Your Best Score: {str(int(self.best_score))}", height=half_screen_height + 75)
            death, death_rect = self.text_utils.get_centered_message(f"Your Death Count: {str(int(self.death_count))}", height=half_screen_height + 100)
            self.screen.blit(text, text_rect)
            self.screen.blit(score, score_rect)
            self.screen.blit(death, death_rect)
            self.screen.blit(best_score, best_score_rect)

            self.screen.blit(DINO_DEAD[0], (half_screen_width-150, half_screen_height-120))
            self.screen.blit(RESET[0], (half_screen_width-30, half_screen_height-100))

    def handle_key_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                self.points = 0
                self.run()

    def reset_game(self):
        self.game_speed=20

    def update_best_score(self):
        if self.points > self.best_score:
            self.best_score = self.points