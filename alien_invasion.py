try:
    import pygame
except:
    import os
    os.system("pip install pygame")    
from pygame.sprite import Group

import game_functions as gf
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from button import Button
from score_board import ScoreBorad
from sound import Sound


def run_game():
    pygame.init()
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=521)
    ai_settings = Settings()

    pygame.mixer.music.load("sound\\BGM.mp3")
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    icon = pygame.image.load("images\\icons\\alien.ico").convert_alpha()
    pygame.display.set_icon(icon)

    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    score = ScoreBorad(ai_settings, screen, stats)
    sound = Sound(pygame.mixer)

    ship = Ship(screen, ai_settings)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens, ship)


    while True:
        if stats.game_active and pygame.mixer.music.get_busy()==False:
            pygame.mixer.music.play()
        gf.check_events(ai_settings, screen, aliens, ship, bullets, play_button, stats, score, sound)
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, score)
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, ai_settings, screen, aliens, ship, stats, score, sound)
            gf.update_aliens(ai_settings, stats, screen, aliens, ship, bullets, score, sound)

if __name__ == "__main__":
    run_game()