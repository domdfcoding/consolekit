# Demo of consolekit's spinners

from itertools import cycle
import time
from consolekit.utils import braille_spinner, solidus_spinner, snake_spinner
from consolekit.utils import hidden_cursor

REPEATS = 50
SLEEP = 0.5

with hidden_cursor():

	for _ in range(REPEATS):
		print(f"\r{next(braille_spinner)}", end='')
		time.sleep(SLEEP)

	for _ in range(REPEATS):
		print(f"\r{next(solidus_spinner)}", end='')
		time.sleep(SLEEP)

	for _ in range(REPEATS):
		print(f"\r{next(snake_spinner)}", end='')
		time.sleep(SLEEP)
