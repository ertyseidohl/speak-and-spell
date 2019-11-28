
from gtts import gTTS
import pygame

import os
import io
import time
import sys

os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.display.init()
screen = pygame.display.set_mode((1,1))
pygame.mixer.init(frequency=24000, size=32, channels=1, buffer=4096)

clock = pygame.time.Clock()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def speak(mytext):
    if not mytext:
        print('got empty text buffer')
        return
    if not any(char.isalpha() or char.isnumeric() for char in mytext):
        print('got nonalpha text buffer: ' + mytext)
        return
    if not os.path.exists('./speak_cache/' + mytext + '.mp3'):
        gtts_output = gTTS(text=mytext, lang='en', slow=False)
        gtts_output.save('./speak_cache/' + mytext + '.mp3')
        print('not cached, loading')
    pygame.mixer.music.load('./speak_cache/' + mytext + '.mp3')
    pygame.mixer.music.play()
    while(pygame.mixer.music.get_busy()):
        clock.tick(1)

buffer_text = ''
running = True
getch = _GetchUnix()
while running:
    new_char = getch()
    if new_char == '\n':
        speak(buffer_text)
        buffer_text = ''
    else:
        buffer_text += new_char
        speak(new_char)
    clock.tick()
