import pygame
import random
import os

# This file was copied from my deathlock repository at
# https://github.com/winterbeak/deathlock-jam

music_muted = False
sfx_muted = False

CHANNEL_COUNT = 16
pygame.mixer.init(22050, -16, CHANNEL_COUNT, 64)
pygame.mixer.set_num_channels(CHANNEL_COUNT)
pygame.init()

channels = [pygame.mixer.Channel(channel) for channel in range(CHANNEL_COUNT)]
soundsets = []

# import debug


def update():
    for soundset in soundsets:
        if soundset.limited:
            for i in reversed(range(len(soundset.durations))):
                if soundset.durations[i] <= 0:
                    del soundset.durations[i]
                else:
                    soundset.durations[i] -= 1

    volume_control.update()


def load_music(path):
    pygame.mixer.music.load(pathify(path))


def play_music():
    pygame.mixer.music.play(-1)


def stop_music():
    pygame.mixer.music.stop()


def set_music_volume(volume):
    pygame.mixer.music.set_volume(volume)


def pathify(string):
    return os.path.join("sounds", string + ".wav")


def load(string):
    return pygame.mixer.Sound(pathify(string))


def play(sound, volume=1.0):
    channel = pygame.mixer.find_channel()
    if channel:
        channel.set_volume(volume * volume_control.volume)
        channel.play(sound)


def load_numbers(path, count):
    """Loads a set of sounds whose filenames are the same except they
    contain incrementing numbers.
    path is a string which should contain a %i representing where the number is.
    count is the amount of sounds.
    """
    paths = [path % (number + 1) for number in range(count)]
    return SoundSet(paths)


def load_strings(path, strings):
    """Loads a set of sounds whose filenames are the same, except they
    all have one part that varies.
    path is the part of the string that stays the same.  must contain a %s
    strings is a list of strings, containing all the differences.
    """
    paths = [path % string for string in strings]
    return SoundSet(paths)


class VolumeControl:
    def __init__(self):
        self.volume = 1.0
        self.target_volume = 1.0
        self.fade_speed = 0.05

    def set_volume(self, volume):
        self.volume = volume
        self.target_volume = volume

    def fade_to(self, volume):
        self.target_volume = volume

    def update(self):
        if self.volume < self.target_volume:
            self.volume += self.fade_speed

            if self.volume > self.target_volume:
                self.volume = self.target_volume

        elif self.volume > self.target_volume:
            self.volume -= self.fade_speed

            if self.volume < self.target_volume:
                self.volume = self.target_volume

        set_music_volume(self.volume * MUSIC_VOLUME)


volume_control = VolumeControl()


class SoundSet:
    def __init__(self, paths):
        self.sounds = [load(path) for path in paths]
        self.variants = len(self.sounds)
        self.lastPlayed = 0
        soundsets.append(self)

        self.limited = False
        self.limit = 0
        self.durations = []
        self.sound_duration = 0

        self.delayed = False

    def play(self, sound_id, volume=1.0, force_play=False):
        if not force_play:
            if sfx_muted:
                return

            if self.limited and len(self.durations) >= self.limit:
                return

            for duration in self.durations:
                if duration > self.sound_duration - 2:
                    return

        if volume > 1.0:
            volume = 1.0

        play(self.sounds[sound_id], volume)
        self.lastPlayed = sound_id

        if self.limited:
            self.durations.append(self.sound_duration)

    def play_random(self, volume=1.0, force_play=False):
        if self.variants == 1:
            sound_id = 0
        else:
            sound_id = random.randint(0, self.variants - 1)
            while sound_id == self.lastPlayed:
                sound_id = random.randint(0, self.variants - 1)

        self.play(sound_id, volume, force_play)

    def set_volumes(self, volume):
        for sound in self.sounds:
            sound.set_volume(volume)

    def set_sound_limit(self, limit, sounds_length):
        """Limits the amount of sounds the soundset can play at once.
        sound_duration is an approximation of the sound's lenght in frames.
        can't automate sound_duration since pygame's sound.length() returns
        to the nearest second.
        """
        self.limited = True
        self.limit = limit
        self.sound_duration = sounds_length
