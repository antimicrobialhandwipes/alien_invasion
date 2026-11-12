import sys
import random
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from boss_alien import BossAlien
from debug_button import DebugButton
from delete_save_button import DeleteSaveButton
from variable_label import VariableLabel
from upgrade_button import UpgradeButton

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        # Initialize game and create a screen object
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        # Make a debug button
        self.debug_button = DebugButton(self)

        # Make the ships left label
        self.ships_left_label = VariableLabel(self, (20, self.settings.screen_height - 50), "Backup Ships Remaining")

        # Make the tokens label
        self.tokens_label = VariableLabel(self, (20, 10), "Tokens")

        # Make the upgrade buttons
        self.ship_speed_label = VariableLabel(self, (200, 10), "Ship Speed")
        self.ship_speed_button = UpgradeButton(self, (410, 35))

        self.bullet_speed_label = VariableLabel(self, (460, 10), "Bullet Speed")
        self.bullet_speed_button = UpgradeButton(self, (700, 35))

        # Delete Save button
        self.delete_save_button = DeleteSaveButton(self)

        # Make a ship
        self.ship = Ship(self)
        # Make a group to store bullets in
        self.bullets = pygame.sprite.Group()

        # Make a fleet of aliens to be stored in
        self.aliens = pygame.sprite.Group()

        # Create the fleet of aliens
        self._create_fleet()

        """
            Reference | Citation (YouTube Shorts):
            Sparkling stars background using pygame in Python (2024) YouTube. 
            Available at: https://www.youtube.com/shorts/rBcW3HtCiN8 (Accessed: 04 November 2026)
        """

        # 100 Sparkles:
        # Formatted [x_position, y_position, radius (1-3)]
        self.sparkles = [[random.randint(0, self.settings.screen_width),
                          random.randint(0, self.settings.screen_height),
                          random.randint(1, 3)] for _ in range(self.settings.sparkle_count)]

        # Start Alien Invasion in an active state.
        self.game_active = True

    def run_game(self):
        """Start the main loop for the game."""
        # Start the main loop for the game
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_active:
                    if self.debug_button.is_clicked(event.pos):
                        self.aliens.empty()  # the normal "wave cleared" logic builds the next fleet

                    elif self.ship_speed_button.is_clicked(event.pos):
                        if self.stats.tokens > 0:
                            self.stats.tokens -= 1
                            self.settings.ship_speed += self.settings.ship_speed_inc
                            self.settings.write_save(self.stats)

                    elif self.bullet_speed_button.is_clicked(event.pos):
                        if self.stats.tokens > 0:
                            self.stats.tokens -= 1
                            self.settings.bullet_speed += self.settings.bullet_speed_inc
                            self.settings.write_save(self.stats)

                    elif self.delete_save_button.is_clicked(event.pos):
                        self.settings.delete_save(self.stats)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            # Move the ship to the left
            self.ship.moving_left = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            # Move the ship up
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            # Move the ship down
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            # Ship stops moving to the right
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            # Ship stops moving to the left
            self.ship.moving_left = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            # Ship stops moving up
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            # Ship stops moving down
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            # Create a new bullet and add it to the bullets group
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        if self.stats.boss_active:
            # Remove the bullets only, the boss loses 1 hp for each bullet that hit
            collisions = pygame.sprite.groupcollide(
                    self.bullets, self.aliens, True, False)
            for boss in self.aliens.sprites():
                boss.hp -= len(collisions)
                if boss.hp <= 0:
                    self.aliens.remove(boss)
        else:
            # Remove any bullets and aliens that have collided.
            collisions = pygame.sprite.groupcollide(
                    self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and move on to the next wave
            self.bullets.empty()
            # boss defeated
            if self.stats.boss_active:
                self.stats.boss_active = False
                self.stats.waves_cleared = 0
                self.stats.tokens += self.settings.tokens_gained_boss
            else:
                self.stats.waves_cleared += 1
                self.stats.tokens += self.settings.tokens_gained_normal
                if self.stats.waves_cleared == self.settings.waves_before_boss:
                    self.stats.boss_active = True
            self._spawn_wave()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new wave and center the ship
            self._spawn_wave()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height + 20
        while current_y < (self.settings.screen_height - 5 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _create_boss(self):
        """Create the boss alien"""
        boss = BossAlien(self)
        self.aliens.add(boss)

    def _spawn_wave(self):
        """Create the boss if it's boss time, otherwise a normal fleet"""
        if self.stats.boss_active:
            self._create_boss()
        else:
            self._create_fleet()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)

        # Loops through all 100 sparkles
        for s in self.sparkles:
            pygame.draw.circle(self.screen, self.settings.sparkle_color,
                               (s[0], s[1]), s[2])

            s[0] = s[0] + random.choice([-1, 0, 1]) # x-pos
            s[1] = s[1] + random.choice([-1, 0, 1]) # y-pos
            s[2] = random.randint(1, 3)       # radius

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        if self.stats.boss_active:
            for boss in self.aliens.sprites():
                boss.draw_hp_bar()

        self.ships_left_label.draw_label(self.stats.ships_left) 

        self.debug_button.draw_button()

        if self.stats.save_exists:
            self.delete_save_button.draw_button()

        self.tokens_label.draw_label(self.stats.tokens) 

        self.ship_speed_label.draw_label(self.settings.ship_speed)
        self.ship_speed_button.draw_button()

        self.bullet_speed_label.draw_label(self.settings.bullet_speed)
        self.bullet_speed_button.draw_button()

        # Make the most recent drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
