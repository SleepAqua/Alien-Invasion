import pygame.font
from pygame.sprite import Group
from ship import Ship


class ScoreBorad:
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.txt_color = (30, 30, 30)
        self.font = pygame.font.SysFont('arial', 28)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        score_msg = "Current: {:,}".format(int(round(self.stats.score, -1)))
        self.score_img = self.font.render(score_msg, True, self.txt_color, self.ai_settings.bg_color)
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def draw_score(self):
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        high_score = "Highest: {:,}".format(int(round(self.stats.high_score, -1)))
        self.high_score_img = self.font.render(high_score, True, self.txt_color, self.ai_settings.bg_color)
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def prep_level(self):
        level_msg = str("Level: {}".format(self.stats.level))
        self.level_image = self.font.render(level_msg, True, self.txt_color, self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = 10 + self.score_rect.bottom

    def prep_ships(self):
        self.ships = Group()
        for ship_num in range(self.stats.ships_left):
            ship = Ship(self.screen, self.ai_settings)
            ship.rect.x = 10 + ship_num*ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
