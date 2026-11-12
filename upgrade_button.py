from button import Button

class UpgradeButton(Button):
    """A button that's used to upgrade the ship"""

    def __init__(self, ai_game, position):
        super().__init__(ai_game,
            width = 30, height = 30,
            position = position,
            label = "+",
        )

