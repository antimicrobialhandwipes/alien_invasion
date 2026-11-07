import pygame

class DebugButton:
    """A button that skips to the next round, for testing"""

    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.color = (200, 200, 200)
        self.font = pygame.font.SysFont("consolas, menlo, dejavusansmono", 20, 24)

        # Top-right corner
        self.rect = pygame.Rect(0, 0, 100, 30)
        self.rect.bottomright = (ai_settings.screen_width - 50, ai_settings.screen_height - 45)

    def draw_button(self):
        """Draw the button with its caption underneath"""
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

        label = self.font.render("Debug", True, self.color)
        self.screen.blit(label, label.get_rect(center=self.rect.center))

        caption = self.font.render("skip to next", True, self.color)
        self.screen.blit(caption, caption.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 4)))