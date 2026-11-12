from button import Button

class DebugButton(Button):
    """A button that skips a level; for debugging"""

    def __init__(self, ai_game):
        super().__init__(ai_game,
            width = 100, height = 30,
            position = (ai_game.settings.screen_width - 40, ai_game.settings.screen_height - 30),
            label = "Skip"
        )
