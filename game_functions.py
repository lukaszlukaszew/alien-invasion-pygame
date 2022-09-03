"""Main functions of the game"""

import sys
from time import sleep
from random import randint
import pygame
from bullet import Bullet
from alien import AlienUFO, AlienTentacle, AlienShoot, AlienTeleport


def check_events(
    settings, screen, stats, scoreboard, play_button, ship, aliens, bullets, alien_bullets
):
    """Event loop"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                settings,
                screen,
                stats,
                scoreboard,
                play_button,
                ship,
                aliens,
                bullets,
                mouse_x,
                mouse_y,
                alien_bullets
            )
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(
                event, settings, screen, stats, scoreboard, ship, aliens, bullets, alien_bullets
            )
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(
    event, settings, screen, stats, scoreboard, ship, aliens, bullets, alien_bullets
):
    """Actions for pressed keys"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_SPACE:
        fire_bullets(settings, screen, ship, bullets)
    if event.key == pygame.K_p:
        start_game(settings, screen, stats, scoreboard, ship, aliens, bullets, alien_bullets)
    if event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Actions for released keys"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(
    settings, screen, stats, scoreboard, ship, aliens, bullets, play_button, alien_bullets
):
    """Actions required to screen refresh"""
    screen.fill(settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for abullet in alien_bullets.sprites():
        abullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    scoreboard.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def update_bullets(
    settings, screen, stats, scoreboard, ship, aliens, bullets, alien_bullets
):
    """Update bullets positions and check collission with aliens"""
    bullets.update()  # here for every item in group method update() is launched

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(
        settings, screen, stats, scoreboard, ship, aliens, bullets, alien_bullets
    )

    if alien_bullets:
        alien_bullets.update()
        for abullet in alien_bullets.copy():
            if abullet.rect.top >= settings.screen_height:
                alien_bullets.remove(abullet)

        check_alien_bullets_ship_collision(settings, stats, scoreboard, screen, ship, aliens, bullets, alien_bullets)


def fire_bullets(settings, screen, ship, bullets):
    """Create new bullets when needed"""
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(settings, screen, stats, ship, aliens, alien_bullets):
    """Create full fleet of aliens"""
    if stats.level < settings.alien_changes[0]:
        alien = AlienUFO(settings, screen)
    elif stats.level < settings.alien_changes[1]:
        alien = AlienTentacle(settings, screen)
    elif stats.level < settings.alien_changes[3]:
        alien = AlienShoot(settings, screen, alien_bullets)
    elif stats.level < settings.alien_changes[4]:
        alien = AlienTeleport(settings, screen, alien_bullets)

    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)

    if stats.level < settings.alien_changes[3]:
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                create_alien(
                    settings,
                    screen,
                    aliens,
                    alien_number,
                    row_number,
                    stats.level,
                    number_aliens_x,
                    alien_bullets,
                )
    else:
        for alien_number in range(stats.level):
            create_alien(
                settings,
                screen,
                aliens,
                alien_number,
                0,
                stats.level,
                number_aliens_x,
                alien_bullets,
            )


def get_number_aliens_x(settings, alien_width):
    """Get number of aliens possible to fit in x dimension"""
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = available_space_x // (2 * alien_width)
    return number_aliens_x


def create_alien(
    settings,
    screen,
    aliens,
    alien_number,
    row_number,
    level,
    number_aliens_x,
    alien_bullets,
):
    """Create alien and add it to the fleet"""
    if level < settings.alien_changes[0]:
        alien = AlienUFO(settings, screen)
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
    elif level < settings.alien_changes[1]:
        alien = AlienTentacle(settings, screen)
        y = (
            alien.rect.height
            + alien.rect.height
            - alien.rect.height
            * abs(alien_number - number_aliens_x // 2)
            // number_aliens_x
        )
        alien.rect.y = y + alien.rect.height * row_number
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
    elif level < settings.alien_changes[3]:
        alien = AlienShoot(settings, screen, alien_bullets)
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
    elif level < settings.alien_changes[4]:
        alien = AlienTeleport(settings, screen, alien_bullets)
        alien.rect.x = randint(0, settings.screen_width - alien.rect.width)
        alien.rect.y = randint(0, settings.screen_height - 3 * alien.rect.height)

    aliens.add(alien)


def get_number_rows(settings, ship_height, alien_height):
    """Get number of rows of aliens"""
    availables_space_y = settings.screen_height - (3 * alien_height) - ship_height
    number_rows = availables_space_y // (2 * alien_height)
    return number_rows


def update_aliens(settings, stats, scoreboard, screen, ship, aliens, bullets, alien_bullets):
    """Check screen edges and update position of every alien in the group"""
    check_fleet_edges(settings, stats, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, scoreboard, screen, ship, aliens, bullets, alien_bullets)

    check_aliens_bottom(settings, stats, scoreboard, screen, ship, aliens, bullets, alien_bullets)


def check_fleet_edges(settings, stats, aliens):
    """Reactiion for alien reaching the edge of the screen"""
    if stats.level < settings.alien_changes[1]:
        for alien in aliens.sprites():
            if alien.check_edges():
                change_fleet_direction(settings, aliens)
                break


def change_fleet_direction(settings, aliens):
    """Move down and change direction of horizontal movement"""
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def check_bullet_alien_collisions(
    settings, screen, stats, scoreboard, ship, aliens, bullets, alien_bullets
):
    """Reaction to the collision between bullet and alien"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)

    if not aliens:
        bullets.empty()
        settings.increase_speed()

        stats.level += 1
        scoreboard.prep_level()

        create_fleet(settings, screen, stats, ship, aliens, alien_bullets)


def ship_hit(
    settings, stats, scoreboard, screen, ship, aliens, bullets, alien_bullets
):
    """Reaction in case of collision of ship and alien"""
    if stats.ships_left > 0:
        stats.ships_left -= 1

        scoreboard.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(settings, screen, stats, ship, aliens, alien_bullets)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(
    settings, stats, scoreboard, screen, ship, aliens, bullets, alien_bullets
):
    """Reaction to any alien reacheing bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(
                settings,
                stats,
                scoreboard,
                screen,
                ship,
                aliens,
                bullets,
                alien_bullets,
            )
            break


def check_play_button(
    settings,
    screen,
    stats,
    scoreboard,
    play_button,
    ship,
    aliens,
    bullets,
    mouse_x,
    mouse_y,
    alien_bullets
):
    """Reaction to button click"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(settings, screen, stats, scoreboard, ship, aliens, bullets, alien_bullets)


def start_game(
    settings, screen, stats, scoreboard, ship, aliens, bullets, alien_bullets
):
    """Prepare and start the game"""
    settings.initialize_dynamic_settings()

    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True

    scoreboard.prep_score()
    scoreboard.prep_high_score()
    scoreboard.prep_level()
    scoreboard.prep_ships()

    aliens.empty()
    bullets.empty()
    alien_bullets.empty()

    create_fleet(settings, screen, stats, ship, aliens, alien_bullets)
    ship.center_ship()


def check_high_score(stats, scoreboard):
    """Check if there is a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()


def check_alien_bullets_ship_collision(settings, stats, scoreboard, screen, ship, aliens, bullets, alien_bullets):
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        ship_hit(settings, stats, scoreboard, screen, ship, aliens, bullets, alien_bullets)