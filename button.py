import pygame

"""
    Reference | Citation (GeeksforGeeks):
    GeeksforGeeks. (2020, April 23). How to create buttons in a game using PyGame? GeeksforGeeks.
    Available at: https://www.geeksforgeeks.org/python/how-to-create-buttons-in-a-game-using-pygame/ (Accessed: 06 November 2026)
"""

class Button:
    """Creates a button given a size, position, and label"""

    def __init__(self, ai_game, width, height, position, label):
        self.screen = ai_game.screen
        self.color = (200, 200, 200)
        self.label = label
        self.font = pygame.font.SysFont("consolas", 20)

        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.bottomright = position

    def draw_button(self):
        """Draw the button"""
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

        label = self.font.render(self.label, True, self.color)
        self.screen.blit(label, label.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
