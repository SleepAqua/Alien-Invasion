import pygame
from pygame.sprite import Sprite
from ship import Ship


class Alien(Sprite):
    def __init__(self, screen, ai_settings):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        self.image = pygame.image.load("images\\alien.jpg")
        ship = Ship(screen, ai_settings)
        # self.image = pygame.transform.scale(self.image,(45, 50))
        self.rect = self.image.get_rect()

        self.rect.x = ship.rect.width
        self.rect.y = ship.rect.height

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def draw(self, screen):
        pygame.draw.rect(self.screen, self.rect)

    def update(self):
        self.x = float(self.rect.x)
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        

    def reach_edge(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        else:
            return False