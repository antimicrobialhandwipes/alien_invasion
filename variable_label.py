import pygame

class VariableLabel:
    """Creates a label that will have the format 'label: value' to track variables"""

    def __init__(self, ai_game, position, label):
        self.screen = ai_game.screen
        self.color = (200, 200, 200)
        self.label = label
        self.position = position
        self.font = pygame.font.SysFont("consolas", 20)

    def draw_label(self, value):
        """Render and draw the text"""
        text = f"{self.label}: {value}"
        surface = self.font.render(text, True, self.color)
        self.screen.blit(surface, self.position)
