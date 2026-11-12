import json
from pathlib import Path

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = "#120e24"
        self.fps = 60

        # Sparkle settings
        self.sparkle_count = 100
        self.sparkle_color = 255, 255, 255

        # Savefile
        self.save_path = "save.json"

        # Ship settings.
        self.ship_speed = 4
        self.ship_limit = 2

        # Bullet settings
        self.bullet_speed = 8
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = "#e33941"
        self.bullets_allowed = 5

        # Alien settings.
        self.alien_speed = 1
        self.fleet_drop_speed = 2
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Boss alien settings
        self.waves_before_boss = 3
        self.boss_images = ["images/alien_boss_1.png", "images/alien_boss_2.png", "images/alien_boss_3.png"]
        self.boss_speed_factor = 8
        self.boss_hp = 30
        self.boss_strafe_delay = 20  # Strafes every third of a second (1 sec = 60 fps)
        self.boss_drop_speed = 20
        self.boss_bar_color = "#2ecc40"
        self.boss_bar_back = "#5c1a1a"

        # Tokens + upgrades settings
        self.ship_speed_inc = 1
        self.bullet_speed_inc = 2
        self.tokens_gained_boss = 2
        self.tokens_gained_normal = 1

    def load_save(self, data):
        if not ("ship_speed" in data and "bullet_speed" in data):
            print("Invalid save file; couldn't load and sticking with defaults")
            return

        self.ship_speed = data.get("ship_speed")
        self.bullet_speed = data.get("bullet_speed")

    def write_save(self, stats):
        data = {
            "tokens": stats.tokens,
            "ship_speed": self.ship_speed,
            "bullet_speed": self.bullet_speed,
        }

        path = Path(self.save_path)

        with open(path, "w") as f:
            json.dump(data, f)

        stats.save_exists = True

    def delete_save(self, stats):
        path = Path(self.save_path)
        path.unlink()
        stats.save_exists = False


