class Sound:
    def __init__(self, mixer):
        self.shoot_sound = mixer.Sound("sound\\ZR2014.WAV")
        self.alien_sound = mixer.Sound("sound\\win game coin.wav")
        self.ship_sound = mixer.Sound("sound\\error.wav")
        self.gg_sound = mixer.Sound("sound\\gameover-cartoon2.wav")
        self.confirm_sound = mixer.Sound("sound\\confirm-button.wav")
        self.lvlup_sound = mixer.Sound("sound\\achievement.wav")