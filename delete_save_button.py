from button import Button

class DeleteSaveButton(Button):
    """A button that deletes your save file so your upgrades reset on the next instance"""

    def __init__(self, ai_game):
        super().__init__(ai_game,
            width = 200, height = 30,
            position = (ai_game.settings.screen_width - 10, 35),
            label = "Delete Save"
        )
