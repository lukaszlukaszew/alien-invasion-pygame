"""Module containing all sound features"""

from pygame import mixer


class SoundMixer:
    """Class dedicated to manage all game sounds"""

    def __init__(self):

        self.sound_list = {
            "alien_beam": 0.2,
            "alien_boss_move": 0.5,
            "alien_shoot": 0.3,
            "Boom": 0.5,
            "menu_button_play": 1,
            "ship_bonus_catch": 1,
            "ship_hit_reset": 1,
            "ship_shoot": 0.2,
        }

        self.music_list = {
            "alien_alien_background": 0.3,
            "alien_boss_background": 0.5,
            "menu_end_screen": 0.6,
            "menu_start": 0.3,
            "ship_move": 1,
        }

        self.sounds = {}
        self.music = {}
        self.channels = {}

        for sound, volume in self.sound_list.items():
            self.sounds[sound] = mixer.Sound(f"sounds/{sound}.ogg")
            self.sounds[sound].set_volume(volume)

        for num, music in enumerate(self.music_list.keys()):
            self.channels[music] = mixer.Channel(num)
            self.music[music] = mixer.Sound(f"sounds/{music}.ogg")
            self.music[music].set_volume(self.music_list[music])

        mixer.set_num_channels(150)

    def play_sound(self, sound, loops=0):
        """Play sound directly or bind sound with channel and play"""
        if sound in self.sound_list:
            self.sounds[sound].play(loops=loops)
        else:
            self.channels[sound].play(self.music[sound], loops=loops)

    def fade_out(self, sound, time=2000):
        """Fade out choosen sound directly or bind sound with channel and fade it out"""
        if sound in self.sound_list:
            self.sounds[sound].fadeout(time)
        else:
            self.channels[sound].fadeout(time)
