class GameStats:
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.score = 0
        self.high_score = self.get_highest()
        self.level = 1

    def get_highest(self):
        with open("data\\history_highest.json", "r+") as f:
            return float(f.read())

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1