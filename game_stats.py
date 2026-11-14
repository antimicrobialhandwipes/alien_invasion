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
        self.save_exists = False

        self.xp = 0
        self.level = 1
        self.skill_points = 0

        path = Path(self.settings.save_path)

        if path.exists():
            self.save_exists = True
            with open(path, "r") as f:
                data = json.load(f)
                self.settings.load_save(data)
                self.xp = data.get("xp", 0)
                self.level = data.get("level", 1)
                self.skill_points = data.get("skill_points", 0)
                self.waves_cleared = data.get("waves_cleared", 0)

    def xp_to_next_level(self):
        """XP needed to level up"""
        return self.settings.xp_per_level

    def add_xp(self, amount):
        """Adding XP and levelling up."""
        self.xp += amount

        while self.xp >= self.xp_to_next_level():
            self.xp -= self.xp_to_next_level()
            self.level += 1
            self.skill_points += self.settings.skill_points_per_level
