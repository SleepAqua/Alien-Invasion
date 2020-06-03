import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_events(ai_settings, screen, aliens, ship, bullets, play_button, stats, score, sound):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sound)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not stats.game_active:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, aliens, bullets, ship, play_button, mouse_x, mouse_y, score, sound)
            else:
                check_mouse_events(event, bullets, screen, ai_settings, ship, sound)

def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sound):
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        if stats.game_active:
            fire_bullets(bullets, screen, ai_settings, ship, sound)
    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        with open("data\\history_highest.json", "w+") as f:
            f.write(str(stats.high_score))
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = False
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.moving_down = False

def check_play_button(ai_settings, screen, stats, aliens, bullets, ship, play_button, mouse_x, mouse_y, score, sound):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        sound.confirm_sound.play()
        reset_game(ai_settings, screen, stats, aliens, bullets, ship, score)
        pygame.mouse.set_visible(False)
        
def reset_game(ai_settings, screen, stats, aliens, bullets, ship, score):
    stats.reset_stats()
    stats.game_active = True

    score.prep_level()
    score.prep_high_score()
    score.prep_score()
    score.prep_ships()

    aliens.empty()
    bullets.empty()
    ai_settings.initialize_dynamic_settings()

    create_fleet(ai_settings, screen, aliens, ship)
    ship.center_ship()
    sleep(0.5)

def check_mouse_events(event, bullets, screen, ai_settings, ship, sound):
    fire_bullets(bullets, screen, ai_settings, ship, sound)

def fire_bullets(bullets, screen, ai_settings, ship, sound):
    if len(bullets) <= ai_settings.bullet_allowed:
        sound.shoot_sound.play()
        new_bullet = Bullet(screen, ai_settings, ship)
        bullets.add(new_bullet)


def update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, score):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    aliens.draw(screen)
    score.draw_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()
    sleep(0.005)


def update_bullets(bullets, ai_settings, screen, aliens, ship, stats, score, sound):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_collisons(bullets, ai_settings, screen, aliens, ship, stats, score, sound)

def check_collisons(bullets, ai_settings, screen, aliens, ship, stats, score, sound):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens_ in collisions.values():
            sound.alien_sound.play()
            stats.score += ai_settings.alien_score * len(aliens_)
            score.prep_score()
        check_high_score(stats, score)
    if len(aliens) == 0:
        bullets.empty()
        start_new_level(ai_settings, stats, score, screen, aliens, ship)
        sound.lvlup_sound.play()
        sleep(1.5)

def start_new_level(ai_settings, stats, score, screen, aliens, ship):
    ai_settings.increase_speed()
    stats.level += 1
    score.prep_level()
    create_fleet(ai_settings, screen, aliens, ship)

def check_high_score(stats, score):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score.prep_high_score()

def update_aliens(ai_settings, stats, screen, aliens, ship, bullets, score, sound):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, aliens, ship, bullets, score, sound)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, score, sound)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, score, sound):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, aliens, ship, bullets, score, sound)
            break

def ship_hit(ai_settings, stats, screen, aliens, ship, bullets, score, sound):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        score.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        sound.ship_sound.play()
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        sound.gg_sound.play()
        pygame.mixer.music.stop()


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.reach_edge():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def get_num_alien(ai_settings, alien_width):
    available_x = (ai_settings.screen_width - 2 * alien_width)
    res = int(available_x / 2 / alien_width)
    return res

def create_alien(screen, ai_settings, accu_num, aliens, row_num):
    new_alien = Alien(screen, ai_settings)
    alien_width = new_alien.rect.width; alien_height = new_alien.rect.height
    new_alien.rect.x = 2*accu_num*alien_width + alien_width
    new_alien.rect.y = 35+2*alien_height*row_num + alien_height
    aliens.add(new_alien)

def get_num_rows(ai_settings, alien_width, ship_width):
    available_y = ai_settings.screen_height - 3 * alien_width - ship_width
    res = int(available_y / 2 / alien_width)
    return res

def create_fleet(ai_settings, screen, aliens, ship):
    alien = Alien(screen, ai_settings)
    num_alien = get_num_alien(ai_settings, alien.rect.width)
    num_rows = get_num_rows(ai_settings, alien.rect.width, ship.rect.width)
    for row_num in range(num_rows):
        for accu_num in range(num_alien):
            create_alien(screen, ai_settings, accu_num, aliens, row_num)