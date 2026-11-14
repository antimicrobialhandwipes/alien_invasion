from upgrade_button import UpgradeButton
from variable_label import VariableLabel


class Menu:
    """Upgrade menu, displays player's level, skill points and upgrade buttons. """

    def __init__(self, ai_game):
        self.stats = ai_game.stats
        self.settings = ai_game.settings

        self.level_label = VariableLabel(ai_game, (20, 10), "Level")
        self.skill_points_label = VariableLabel(ai_game, (160, 10), "Skill Points")

        self.ship_speed_label = VariableLabel(ai_game, (350, 10), "Ship Speed")
        self.ship_speed_button = UpgradeButton(ai_game, (560, 35))

        self.bullet_speed_label = VariableLabel(ai_game, (610, 10), "Bullet Speed")
        self.bullet_speed_button = UpgradeButton(ai_game, (850, 35))

    def check_click(self, pos):
        """Spending skill points if an upgrade button was clicked."""
        if self.stats.skill_points <= 0:
            return False

        if self.ship_speed_button.is_clicked(pos):
            self.stats.skill_points -= 1
            self.settings.ship_speed += self.settings.ship_speed_inc
            return True

        if self.bullet_speed_button.is_clicked(pos):
            self.stats.skill_points -= 1
            self.settings.bullet_speed += self.settings.bullet_speed_inc
            return True

        return False

    def draw(self):
        self.level_label.draw_label(self.stats.level)
        self.skill_points_label.draw_label(self.stats.skill_points)

        self.ship_speed_label.draw_label(self.settings.ship_speed)
        self.ship_speed_button.draw_button()

        self.bullet_speed_label.draw_label(self.settings.bullet_speed)
        self.bullet_speed_button.draw_button()
