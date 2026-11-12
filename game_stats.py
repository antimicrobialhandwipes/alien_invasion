import json
from pathlib import Path

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.waves_cleared = 0
        self.boss_active = False
        self.ships_left = self.settings.ship_limit
        self.tokens = 0
        self.save_exists = False

        path = Path(self.settings.save_path)

        if path.exists():
            self.save_exists = True
            with open(path, "r") as f:
                data = json.load(f)
                self.settings.load_save(data)
                if "tokens" in data:
                    self.tokens = data.get("tokens")
