import random
import pygame
import game_functions as gf

from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from ship import Ship
from debug_button import DebugButton

def run_game():
    # Initialize game and create a screen object

    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    clock = pygame.time.Clock()

    pygame.display.set_caption("Alien Invasion")

    # Create an instance to store game statistics
    stats = GameStats(ai_settings)

    # Make a debug button
    debug_button = DebugButton(ai_settings, screen)

    # Make a ship
    ship = Ship(ai_settings, screen)
    # Make a group to store bullets in
    bullets = Group()

    # Make a fleet of aliens to be stored in
    aliens = Group()
    # Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    """
        Reference | Citation (YouTube Shorts):
        Sparkling stars background using pygame in Python (2024) YouTube. 
        Available at: https://www.youtube.com/shorts/rBcW3HtCiN8 (Accessed: 04 November 2026)
    """

    # 100 Sparkles:
    # Formatted [x_position, y_position, radius (1-3)]
    sparkles = [[random.randint(0, ai_settings.screen_width),
                 random.randint(0, ai_settings.screen_height),
                 random.randint(1, 3)] for _ in range(ai_settings.sparkle_count)]

    # Start the main loop for the game
    while True:
        gf.check_events(ai_settings, screen, stats, ship, aliens, bullets, debug_button)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, ship, aliens, sparkles, bullets, debug_button)
        clock.tick(ai_settings.fps)

run_game()