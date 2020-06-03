class Settings:
    def __init__(self):
        self.bg_color = (230, 230, 230)
        self.screen_width = 1200
        self.screen_height = 600

        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 10

        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        self.speedup_scale = 2
        self.score_scale = 2

        self.alien_score = 100
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.alien_score = 100

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_score *= (self.score_scale)