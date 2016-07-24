""" Another courageous attempt to create a text-based planting game.
    This file is going to be the new version of main.py
"""

import sys
import threading
import time


# from Sound.listen import play_messenger  # <<- the .wav file can't be seen

__author__ = 'Jero'
__version__ = 0.1

# TODO:
#   * create another method in Leaf() that will enumerate all active thread
#   * make a list of valid commands
#   * make sure to trim extra spaces of user's input


def play_messenger():
    """ Play a sound that was inspired from Facebook Messenger """

    sound = 'audio/wav/messenger-sound-notification.wav'

    import winsound
    winsound.PlaySound(sound, winsound.SND_FILENAME)


def play_real_music():
    """ Play a nice chilling song #eurekamoment """

    import vlc

    song = 'audio/mp3/Oo - Up Dharma Down.mp3'
    leaf_music_player = vlc.MediaPlayer(song)
    leaf_music_player.play()
    print("enjoy your music while planting :)")


class Leaf(threading.Thread):
    """ Main object for playing the game """

    seed_basket = {'tomato': 60,
                   'mushroom': 60,
                   'cocoa': 300,
                   'plum': 300,
                   'pickle': 180,
                   'onion': 15,
                   'eggplant': 30,
                   'melon': 900,
                   'test': 5,
                   'strawberry': 225,
                   'guaba': 239}

    def __init__(self, seed=None):
        threading.Thread.__init__(self)
        self.seed = seed

    def run(self):
        time.sleep(self.seed_basket[self.seed])
        print("\n%s planted! nicely done mate :)" % self.seed)
        play_messenger()  # play a nice sound after planting :)

    def whats_planting(self):
        """ Show active thread """

        print("planting %s" % self.seed)


if __name__ == '__main__':
    game = Leaf()

    while True:
        seed = input("leaf :: ")
        if seed in ['exit', 'quit']:      # TODO: you need to have a list of commands here
            sys.exit()

        if seed in game.seed_basket:
            game = Leaf(seed)

            if seed == 'guaba':     # Eureka moment
                play_real_music()

            game.whats_planting()
            game.start()
        else:
            print("No '%s' inside your basket :(" % seed)