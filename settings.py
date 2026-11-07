class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = "#120e24"
        self.fps = 60

        # Sparkle settings
        self.sparkle_count = 100
        self.sparkle_color = 255, 255, 255

        # Ship settings
        self.ship_speed_factor = 5.5
        self.ship_limit = 3 # 4 lives

        # Bullet Settings
        self.bullet_speed_factor = 8
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = "#e33941"
        self.bullets_allowed = 5

        # Alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 2
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1