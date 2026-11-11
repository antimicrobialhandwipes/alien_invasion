import pygame

"""
    Reference | Citation (GeeksforGeeks):
    GeeksforGeeks. (2020, April 23). How to create buttons in a game using PyGame? GeeksforGeeks. 
    Available at: https://www.geeksforgeeks.org/python/how-to-create-buttons-in-a-game-using-pygame/ (Accessed: 06 November 2026)
"""

class DebugButton:
    """A button that skips a level; for debugging"""

    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.color = (200, 200, 200)
        self.font = pygame.font.SysFont("consolas", 20, 24) #console font

        # Bottom-right corner
        self.rect = pygame.Rect(0, 0, 100, 30)
        self.rect.bottomright = (ai_settings.screen_width - 50, ai_settings.screen_height - 45)

    def draw_button(self):
        """Draw the button with its caption underneath"""
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

        label = self.font.render("Debug", True, self.color)
        self.screen.blit(label, label.get_rect(center=self.rect.center))

        caption = self.font.render("skip to next", True, self.color)
        self.screen.blit(caption, caption.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 4)))