"""Main functions of the game"""

import sys
from time import sleep
from random import randint

import pygame
from bullet import ShipBullet
from alien import *


def check_events(game):
    """Game event loop"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, game)


def check_keydown_events(event, game):
    """Actions for pressed keys"""
    if event.key == pygame.K_RIGHT and game.stats.game_active:
        game.ship.moving_right = True
    if event.key == pygame.K_LEFT and game.stats.game_active:
        game.ship.moving_left = True
    if event.key == pygame.K_SPACE and game.stats.game_active:
        fire_bullets(game)
    if event.key == pygame.K_p and not game.stats.game_active:
        start_game(game)
    if event.key == pygame.K_ESCAPE and game.stats.game_active:
        game.stats.game_not_paused = not game.stats.game_not_paused
    if event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, game):
    """Actions for released keys"""
    if event.key == pygame.K_RIGHT:
        game.ship.moving_right = False
    if event.key == pygame.K_LEFT:
        game.ship.moving_left = False


def update_screen(game):
    """Actions required to screen refresh"""
    game.screen.fill(game.settings.bg_color)

    if game.stats.game_active:
        if game.stats.level <= game.settings.alien_changes[-1]:

            for bullet in game.bullets.sprites():
                bullet.draw_bullet()

            for abullet in game.alien_bullets.sprites():
                abullet.draw_bullet()

            game.ship.blitme()
            game.aliens.draw(game.screen)
            game.scoreboard.show_score()

        else:
            game.stats.game_active = False
            pygame.mouse.set_visible(True)
            game.scoreboard.prep_end_screen()
            game.scoreboard.show_score()

    if not game.stats.game_active:
        if game.stats.game_played:
            game.scoreboard.prep_end_screen()
            game.scoreboard.show_score()

        game.play_button.draw_button()

    pygame.display.flip()


def update_bullets(game):
    """Update bullets positions and check collission with aliens"""
    game.bullets.update()

    for bullet in game.bullets.copy():
        if bullet.rect.bottom <= 0:
            game.bullets.remove(bullet)

    check_bullet_alien_collisions(game)

    if game.alien_bullets:
        game.alien_bullets.update()
        for abullet in game.alien_bullets.copy():
            if abullet.rect.top >= game.settings.screen_height:
                game.alien_bullets.remove(abullet)

        check_alien_bullets_ship_collision(game)


def fire_bullets(game):
    """Create new bullets when needed"""
    if len(game.bullets) < game.settings.bullets_allowed:
        new_bullet = ShipBullet(game.settings, game.screen, game.ship)
        game.bullets.add(new_bullet)
        game.stats.bullets_fired += 1


def create_fleet(game):
    """Create full fleet of aliens"""

    if game.stats.level == game.settings.alien_changes[-1]:
        create_alien(game, 1, 0, 1)
    elif game.stats.level > game.settings.alien_changes[-1]:
        pass

    else:
        alien = globals()[game.settings.alien_types[game.settings.current_alien]](
            game.settings, game.screen, game.alien_bullets
        )

        number_aliens_x = get_number_aliens_x(game.settings, alien.rect.width)
        number_rows = get_number_rows(
            game.settings, game.ship.rect.height, alien.rect.height
        )

        if game.stats.level < game.settings.alien_changes[3]:
            for row_number in range(number_rows):
                for alien_number in range(number_aliens_x):
                    create_alien(game, alien_number, row_number, number_aliens_x)
        else:
            for alien_number in range(game.stats.level):
                create_alien(game, alien_number, 0, number_aliens_x)


def get_number_aliens_x(settings, alien_width):
    """Get number of aliens possible to fit in x dimension"""
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = available_space_x // (2 * alien_width)
    return number_aliens_x


def create_alien(game, alien_number, row_number, number_aliens_x):
    """Create alien and add it to the fleet"""
    alien = globals()[game.settings.alien_types[game.settings.current_alien]](
        game.settings, game.screen, game.alien_bullets
    )

    if game.settings.current_alien == 0:  # AlienUFO
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
    elif game.settings.current_alien == 1:  # AlienTentacle
        y = (
            2 * alien.rect.height
            - alien.rect.height
            * abs(alien_number - number_aliens_x // 2)
            // number_aliens_x
        )

        alien.rect.y = y + alien.rect.height * row_number
        alien_width = alien.rect.width
        alien.x = (
            alien_width + (game.settings.screen_width // number_aliens_x) * alien_number
        )
        alien.rect.x = alien.x
    elif game.settings.current_alien == 2:  # AlienShoot
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
    elif game.settings.current_alien == 3:  # AlienTeleport
        alien.rect.x = randint(0, game.settings.screen_width - alien.rect.width)
        alien.rect.y = randint(0, game.settings.screen_height - 3 * alien.rect.height)
    elif game.settings.current_alien == 4:  # AlienBoss1
        alien.rect.centerx = game.settings.screen_width // 2
        alien.rect.centery = game.settings.screen_height // 2

    game.aliens.add(alien)


def get_number_rows(settings, ship_height, alien_height):
    """Get number of rows of aliens"""
    availables_space_y = settings.screen_height - (3 * alien_height) - ship_height
    number_rows = availables_space_y // (2 * alien_height)
    return number_rows


def update_aliens(game):
    """Check screen edges and update position of every alien in the group"""
    check_fleet_edges(game.settings, game.stats, game.aliens)
    game.aliens.update()

    if pygame.sprite.spritecollideany(game.ship, game.aliens):
        ship_hit(game)

    check_aliens_bottom(game)


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


def check_bullet_alien_collisions(game):
    """Reaction to the collision between bullet and alien"""
    collisions = pygame.sprite.groupcollide(
        game.bullets,
        game.aliens,
        True,  # CHANGED
        game.stats.level < game.settings.alien_changes[-1],
    )

    if collisions:
        if game.stats.level >= game.settings.alien_changes[-1]:
            game.settings.alien_boss_life = max(
                0, game.settings.alien_boss_life - len(collisions)
            )
            game.stats.score += game.settings.alien_boss_points * len(collisions)
            game.stats.hits[game.stats.level] += len(collisions)

            game.scoreboard.prep_boss_health()
        else:
            for aliens in collisions.values():
                game.stats.score += game.settings.alien_points * len(aliens)
                game.stats.hits[game.stats.level] += len(aliens)

        game.scoreboard.prep_score()
        check_high_score(game.stats, game.scoreboard)

    if game.settings.alien_boss_life <= 0:
        game.stats.game_won = True
        game.aliens.empty()

    if not game.aliens:
        game.bullets.empty()
        game.settings.increase_speed()

        game.stats.level += 1

        if game.stats.level in game.settings.alien_changes:
            game.settings.current_alien += 1
            game.stats.ships_left += 1

        game.scoreboard.prep_level()

        create_fleet(game)


def ship_hit(game):
    """Reaction in case of collision of ship and alien"""
    if game.stats.ships_left > 0:
        game.stats.ships_left -= 1

        reset_screen(game)

        sleep(0.5)
    else:
        game.stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(game):
    """Reaction to any alien reacheing bottom of the screen."""
    screen_rect = game.screen.get_rect()
    for alien in game.aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(game)
            break


def check_play_button(game, mouse_x, mouse_y):
    """Reaction to button click"""
    button_clicked = game.play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not game.stats.game_active:
        start_game(game)


def start_game(game):
    """Prepare and start the game"""
    game.settings.initialize_dynamic_settings()

    pygame.mouse.set_visible(False)
    game.stats.reset_stats()
    game.stats.game_active = True
    game.stats.game_played = True

    game.scoreboard.prep_score()
    game.scoreboard.prep_high_score()
    game.scoreboard.prep_level()
    game.scoreboard.prep_boss_health()

    reset_screen(game)


def check_high_score(stats, scoreboard):
    """Check if there is a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()


def check_alien_bullets_ship_collision(game):
    """Check if the ship has been shot down"""
    if pygame.sprite.spritecollideany(game.ship, game.alien_bullets):
        ship_hit(game)


def reset_screen(game):
    """Set default game and screen elements to default state"""
    game.scoreboard.prep_ships()

    if game.stats.level == game.settings.alien_changes[-1]:
        game.scoreboard.prep_boss_health()

    game.aliens.empty()
    game.bullets.empty()
    game.alien_bullets.empty()

    create_fleet(game)
    game.ship.center_ship()
