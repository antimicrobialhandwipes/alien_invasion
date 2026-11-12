import random

import pygame

from alien import Alien


class BossAlien(Alien):
    """A class to represent the boss alien"""

    def __init__(self, ai_game):
        """Initialize the boss and set its starting position"""
        super().__init__(ai_game)

        # Load a random boss image and set its rect attribute
        self.image = pygame.image.load(random.choice(self.settings.boss_images))
        self.rect = self.image.get_rect()

        # Start the boss at the top center of the screen
        screen_rect = self.screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.y = 20

        # Store the boss's exact position
        self.x = float(self.rect.x)

        self.hp = self.settings.boss_hp

        # Strafe direction: 1 is right, -1 is left
        self.direction = random.choice([-1, 1])
        self.timer = 0

    """
        Reference | Citation (Pygame Documentation):
        Pygame Community (no date) pygame.time.
        Available at: https://www.pygame.org/docs/ref/time.html (Accessed: 08 November 2026)
    """

    def update(self):
        """Strafe left and right, and drop down when at an edge"""
        # Pick a new random direction every third of a second
        self.timer += 1
        if self.timer >= self.settings.boss_strafe_delay:
            self.direction = random.choice([-1, 1])
            self.timer = 0

        self.x += self.settings.boss_speed_factor * self.direction
        self.rect.x = self.x

        # Drops down if an edge is touched
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            self.direction = -1
            self.rect.y += self.settings.boss_drop_speed
        elif self.rect.left <= 0:
            self.direction = 1
            self.rect.y += self.settings.boss_drop_speed

    """
      Reference | Citation (Stack Overflow):
      Ogilvie, M. (2021) How to put a health bar over the sprite in pygame, Stack Overflow.
      Available at: https://stackoverflow.com/questions/64867475/how-to-put-a-health-bar-over-the-sprite-in-pygame (Accessed: 08 November 2026)
    """

    def draw_hp_bar(self):
        """Draw a green hp bar under the boss"""
        bar_width = self.rect.width * self.hp / self.settings.boss_hp
        back_bar = pygame.Rect(self.rect.x, self.rect.bottom + 5, self.rect.width, 8)
        hp_bar = pygame.Rect(self.rect.x, self.rect.bottom + 5, bar_width, 8)
        pygame.draw.rect(self.screen, self.settings.boss_bar_back, back_bar)
        pygame.draw.rect(self.screen, self.settings.boss_bar_color, hp_bar)
