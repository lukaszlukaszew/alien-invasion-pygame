"""All functions of the game"""

import sys
from time import sleep
from random import randint

import pygame
from bullet import ShipBullet
from explosion import Boom
from alien import AlienUFO, AlienTentacle, AlienTeleport, AlienShoot, AlienBoss
from bonus import Bonus00, Bonus01, Bonus02, Bonus03, Bonus04, Bonus05


def check_events(game):
    """Game event loop"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, game)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game, mouse_x, mouse_y)


def check_keydown_events(event, game):
    """Actions for pressed keys"""
    if game.stats.game_active:
        if event.key == pygame.K_ESCAPE:
            game.stats.game_not_paused = not game.stats.game_not_paused
        if game.stats.game_not_paused:
            if event.key == pygame.K_RIGHT:
                game.ship.moving_right = True
            if event.key == pygame.K_LEFT:
                game.ship.moving_left = True
            if event.key == pygame.K_SPACE:
                fire_bullets(game)
    else:
        if event.key == pygame.K_p:
            start_game(game)
    if event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, game):
    """Actions for released keys"""
    if event.key == pygame.K_RIGHT:
        game.ship.moving_right = False
    if event.key == pygame.K_LEFT:
        game.ship.moving_left = False


def check_play_button(game, mouse_x, mouse_y):
    """Reaction to button click"""
    button_clicked = game.play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not game.stats.game_active:
        game.sounds.play_sound("menu_button_play")
        game.sounds.play_sound("alien_alien_background", -1)
        game.sounds.fade_out("menu_start")
        game.sounds.fade_out("menu_end_screen")
        game.sounds.fade_out("alien_boss_background")
        start_game(game)


def start_game(game):
    """Prepare dynamic parameters and start the game"""
    game.settings.initialize_dynamic_settings()
    game.stats.reset_stats()

    pygame.mouse.set_visible(False)
    game.stats.game_active = True
    game.stats.game_played = True

    game.scoreboard.prep_score()
    game.scoreboard.prep_high_score()
    game.scoreboard.prep_level()

    game.prepare_background_image("background")

    reset_screen(game)


def reset_screen(game):
    """Set game and screen elements to default state"""
    game.scoreboard.prep_ships()

    if game.stats.level == game.settings.alien_changes[-1]:
        game.scoreboard.prep_boss_health()

    game.ship.center_ship()

    game.aliens.empty()
    game.bullets.empty()
    game.alien_bullets.empty()

    for bonus in game.active_bonuses.keys():
        bonus.reverse_effect()

    game.bonuses.empty()
    game.active_bonuses = {}

    game.explosions.empty()

    create_fleet(game)


def update_screen(game):
    """Actions required to screen refresh"""
    game.screen.fill(game.settings.bg_color)

    if game.stats.game_active:
        game.background_image_blitme()
        if game.stats.level <= game.settings.alien_changes[-1]:

            for bullet in game.bullets.sprites():
                bullet.draw_bullet()

            for abullet in game.alien_bullets.sprites():
                abullet.draw_bullet()

            for bonus in game.bonuses.sprites():
                bonus.blitme()

            game.ship.blitme()
            game.aliens.draw(game.screen)
            game.scoreboard.show_score()
        else:
            game.stats.game_active = False
            pygame.mouse.set_visible(True)
            game.ship.moving_left = False
            game.ship.moving_right = False

    if not game.stats.game_active:
        if game.stats.game_played:
            game.scoreboard.prep_end_screen()
            game.scoreboard.show_score()
        else:
            game.background_image_blitme()

        game.play_button.draw_button()

    for boom in game.explosions.sprites():
        boom.blitme()

    pygame.display.flip()


def update_bullets(game):
    """Update bullets positions and check collission with another objects"""
    game.bullets.update()
    game.alien_bullets.update()

    for bullet in game.bullets.copy():
        if bullet.rect.bottom <= 0:
            game.bullets.remove(bullet)

    check_bullet_alien_collisions(game)

    for alien_bullet in game.alien_bullets.copy():
        if alien_bullet.rect.top >= game.settings.screen_height:
            game.alien_bullets.remove(alien_bullet)

    check_alien_bullets_ship_collision(game)


def fire_bullets(game):
    """Create new bullet when players shoots"""
    if len(game.bullets) < game.settings.bullets_allowed:
        new_bullet = ShipBullet(game, game.ship.rect.centerx, game.ship.rect.top)
        game.bullets.add(new_bullet)
        game.stats.bullets_fired += 1
        game.sounds.play_sound("ship_shoot")


def create_fleet(game):
    """Create full fleet of aliens"""
    if game.stats.level == game.settings.alien_changes[-1]:
        create_boss(game)
    else:
        alien = globals()[game.settings.alien_types[game.settings.current_alien]](game)

        number_aliens_x = get_number_aliens_x(game.settings, alien.rect.width)
        number_rows = get_number_rows(
            game.settings, game.ship.rect.height, alien.rect.height
        )

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                create_alien(game, alien_number, row_number, number_aliens_x)


def create_boss(game):
    """Create one instance of AlienBoss object"""
    create_alien(game, 1, 0, 1)
    game.sounds.fade_out("alien_alien_background")
    game.sounds.play_sound("alien_boss_background")


def get_number_aliens_x(settings, alien_width):
    """Get number of aliens possible to fit in x dimension"""
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = available_space_x // (2 * alien_width)
    return number_aliens_x


def get_number_rows(settings, ship_height, alien_height):
    """Get number of aliens possible to fit in y dimension"""
    availables_space_y = settings.screen_height - (3 * alien_height) - ship_height
    number_rows = availables_space_y // (2 * alien_height)
    return number_rows


def create_alien(game, alien_number, row_number, number_aliens_x):
    """Create proper type of alien and add it to the fleet"""
    alien = globals()[game.settings.alien_types[game.settings.current_alien]](game)

    if game.settings.current_alien == 0:  # AlienUFO
        alien.pos_x = alien.rect.width + 2 * alien.rect.width * alien_number
        alien.rect.x = alien.pos_x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    elif game.settings.current_alien == 1:  # AlienTentacle
        alien.pos_x = (
            alien.rect.width
            + (game.settings.screen_width // number_aliens_x) * alien_number
        )
        alien.rect.x = alien.pos_x
        alien.rect.y = (
            alien.rect.height
            * (2 - abs(alien_number - number_aliens_x // 2))
            // number_aliens_x
            + alien.rect.height * row_number
        )
    elif game.settings.current_alien == 2:  # AlienTeleport
        alien.rect.x = randint(0, game.settings.screen_width - alien.rect.width)
        alien.rect.y = randint(0, game.settings.screen_height - 3 * alien.rect.height)
    elif game.settings.current_alien == 3:  # AlienShoot
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        alien.rect.x = alien.rect.width + 2 * alien.rect.width * alien_number
    elif game.settings.current_alien == 4:  # AlienBoss
        alien.rect.centerx = game.settings.screen_width // 2
        alien.rect.centery = game.settings.screen_height // 2

    game.aliens.add(alien)


def update_aliens(game):
    """Check screen edges and update position of every alien in the group"""
    check_fleet_edges(game.settings, game.stats, game.aliens)
    check_aliens_bottom(game)
    game.aliens.update()

    if pygame.sprite.spritecollideany(game.ship, game.aliens):
        ship_hit(game)


def check_fleet_edges(settings, stats, aliens):
    """Reaction for alien reaching the edge of the screen"""
    if stats.level < settings.alien_changes[1]:
        for alien in aliens.sprites():
            if alien.check_edges():
                change_fleet_direction(settings, aliens)
                break


def check_aliens_bottom(game):
    """Reaction to any alien reacheing the bottom of the screen"""
    screen_rect = game.screen.get_rect()
    for alien in game.aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(game)
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
        True,
        game.stats.level < game.settings.alien_changes[-1],
    )

    if collisions:
        if game.stats.level >= game.settings.alien_changes[-1]:
            boss_hit(game, collisions)
        else:
            for aliens in collisions.values():
                game.stats.score += game.settings.alien_points * len(aliens)
                game.stats.hits[game.stats.level] += len(aliens)

                for alien in aliens:
                    if randint(0, 10000) >= game.settings.bonus_drop_rate:
                        drop_bonus(game, alien.rect.centerx, alien.rect.centery)
                    game.explosions.add(
                        Boom(game, alien.rect.centerx, alien.rect.centery)
                    )

    game.scoreboard.prep_score()
    check_high_score(game.stats, game.scoreboard)

    if game.settings.alien_boss_life <= 0:
        game.stats.game_won = True
        game.aliens.empty()

    if not game.aliens:
        level_finished(game)


def level_finished(game):
    """Actions required when all aliens at current level are down"""
    game.bullets.empty()
    game.settings.increase_speed()
    game.stats.level += 1

    if game.stats.level in game.settings.alien_changes:
        game.settings.current_alien += 1
        game.stats.ships_left += 1
        game.scoreboard.prep_ships()

    game.scoreboard.prep_level()

    create_fleet(game)


def boss_hit(game, collisions):
    """Reaction for the boss taking a hit"""
    for bullet, aliens in collisions.items():
        for alien in aliens:
            game.explosions.add(Boom(game, bullet.rect.centerx, alien.rect.bottom))
            for _ in range(
                (game.settings.starting_alien_boss_life - game.settings.alien_boss_life)
                // 10
            ):
                game.explosions.add(
                    Boom(
                        game,
                        randint(alien.rect.left, alien.rect.right),
                        randint(alien.rect.top, alien.rect.bottom),
                    )
                )
    game.settings.alien_boss_life = max(
        0, game.settings.alien_boss_life - len(collisions)
    )
    game.stats.score += game.settings.alien_boss_points * len(collisions)
    game.stats.hits[game.stats.level] += len(collisions)

    game.scoreboard.prep_boss_health()


def ship_hit(game):
    """Reaction in case of collision of ship and alien or alien reaching bottom"""

    if game.stats.ships_left:
        game.stats.ships_left -= 1
        game.sounds.play_sound("ship_hit_reset")
        reset_screen(game)
        sleep(0.5)
    else:
        game.stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, scoreboard):
    """Check if there is a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()


def check_alien_bullets_ship_collision(game):
    """Check if the ship has been shot down"""
    if pygame.sprite.spritecollideany(game.ship, game.alien_bullets):
        ship_hit(game)


def drop_bonus(game, pos_x, pos_y):
    """Select and create bonus object which will be dropped by killed alien"""
    choosen_bonus = randint(2, 2)

    if choosen_bonus == 0:  # extra ship
        bonus = Bonus00(game, pos_x, pos_y, "bonus_add")
    elif choosen_bonus == 1:  # continuous fire
        bonus = Bonus01(game, pos_x, pos_y, "bonus_weapon")
    elif choosen_bonus == 2:  # all kill
        bonus = Bonus02(game, pos_x, pos_y, "bonus_alien")
    elif choosen_bonus == 3:  # additional points
        bonus = Bonus03(game, pos_x, pos_y, "bonus_add")
    elif choosen_bonus == 4:  # alien movement freeze
        bonus = Bonus04(game, pos_x, pos_y, "bonus_alien")
    elif choosen_bonus == 5:  # alien speed decrease
        bonus = Bonus05(game, pos_x, pos_y, "bonus_alien")

    game.bonuses.add(bonus)


def bonus_check_catch(game):
    """Check if bonus was catched by the player and start additional effects"""
    collisions = pygame.sprite.spritecollide(game.ship, game.bonuses, True)

    if collisions:
        for bonus in collisions:
            bonus.apply_effect()
            game.active_bonuses[bonus] = 0
            game.stats.bonuses_used += 1
            game.sounds.play_sound("ship_bonus_catch")


def bonus_check_bottom(game):
    """Delete bonuses which are out of the screen borders"""
    for bonus in game.bonuses.copy():
        if bonus.rect.top >= game.settings.screen_height:
            game.bonuses.remove(bonus)


def update_bonuses(game):
    """Update position of dropped bonuses and remaining time of applied effects."""
    bonus_check_catch(game)
    bonus_check_bottom(game)
    game.bonuses.update()

    if game.stats.game_not_paused:
        for bonus in game.active_bonuses.copy().keys():
            game.active_bonuses[bonus] += 1
            if game.active_bonuses[bonus] > game.settings.bonus_active_time:
                bonus.reverse_effect()
                game.active_bonuses.pop(bonus)


def update_explosions(game):
    """Update explostion animation and remove ones that are finished"""
    game.explosions.update()
    for boom in game.explosions.copy():
        if not boom.frame:
            game.explosions.remove(boom)


def check_ship_movement(game):
    """Play sound of moving ship only when it's in fact moving"""
    if game.ship.moving_left or game.ship.moving_right:
        if not game.sounds.channels["ship_move"].get_busy():
            game.sounds.play_sound("ship_move")
    else:
        if game.sounds.channels["ship_move"].get_busy():
            game.sounds.channels["ship_move"].stop()
