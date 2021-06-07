# Demo of consolekit's spinners

# stdlib
import time

# this package
from consolekit.utils import braille_spinner, hidden_cursor, snake_spinner, solidus_spinner

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
