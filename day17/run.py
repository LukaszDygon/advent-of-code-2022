from enum import IntEnum
from aoc_helpers import input_helper

class Shape(IntEnum):
  BAR = 0
  CROSS = 1
  ANGLE = 2
  COLUMN = 3
  SQUARE = 4

class Rock():
  def __init__(self, shape: Shape, pos: complex) -> None:
    self.position = pos
    if shape == Shape.BAR:
        self._positions = {0 + 0j, 1 + 0j, 2 + 0j, 3 + 0j}
    elif shape == Shape.CROSS:
        self._positions = {1 + 2j, 0 + 1j, 1 + 1j, 2 + 1j, 1}
    elif shape ==  Shape.ANGLE:
        self._positions = {2 + 2j, 2 + 1j, 0, 1, 2}
    elif shape ==  Shape.COLUMN:
        self._positions = {0, 0 + 1j, 0 + 2j, 0 + 3j}
    elif shape ==  Shape.SQUARE:
        self._positions = {0 + 1j, 1 + 1j, 0, 1}

  def positions(self) -> set[complex]:
    return {p + self.position for p in self._positions}

  def move(self, delta: complex) -> None:
    self.position += delta


class Chamber():
  def __init__(self, width: int, winds: str) -> None:
    self.width = width
    self.winds = winds

    self.filled: set[complex] = set()
    self.columns = [-1 for _ in range(width)]
    self.base_height = 0
    self.top = -1
    self.rock: Shape = Shape.BAR
    self.wind_idx = 0

  def __str__(self) -> str:
    return "".join(
      '|' + "".join('#' if x + y * 1j in self.filled else '.' for x in range(self.width)) + "|\n"
      for y in range(self.top, -1, -1)
    ) + '+' + '-' * self.width + '+'

  def __add_rock(self, rock: Rock) -> None:
    positions = rock.positions()
    self.filled |= positions

    for col, height in ((int(p.real), int(p.imag)) for p in positions):
      self.columns[col] = max(self.columns[col], height)
      self.top = max(self.top, height)

  def __trim_filled(self) -> None:
    if (height := min(self.columns) + 1) > 0:
      self.filled = {p - height * 1j for p in self.filled if p.imag >= height}
      self.base_height += height
      self.top -= height
      self.columns = [c - height for c in self.columns]

  def height(self) -> int:
    return self.base_height + self.top + 1

  def simulate_fall(self) -> None:
    rock = Rock(self.rock, 2 + (self.top + 4) * 1j)
    positions = rock.positions()
    move = 0 + 0j

    while True:
      wind_dir = -1 if self.winds[self.wind_idx] == '<' else 1
      self.wind_idx = (self.wind_idx + 1) % len(self.winds)

      next_positions = {p + wind_dir for p in positions}
      if all(p.real >= 0 and p.real < self.width and p not in self.filled for p in next_positions):
        move += wind_dir
        positions = next_positions

      next_positions = {p + -1j for p in positions}
      if any(p.imag < 0 or p in self.filled for p in next_positions):
        break

      move += -1j
      positions = next_positions

    rock.move(move)
    self.__add_rock(rock)
    self.__trim_filled()

    self.rock = (self.rock + 1) % len(Shape)  # type: ignore

def main() -> None:
  jets = input_helper.get_lines(17)[0]

  human_size = 2022
  elephant_size = 1_000_000_000_000

  cavern = Chamber(7, jets)
  attempt = 0
  jump_height = 0
  state = {}

  while attempt < elephant_size:
    cavern.simulate_fall()
    attempt += 1

    state_key = (cavern.rock, cavern.wind_idx, tuple(cavern.columns))
    if attempt > human_size and state_key in state:
      attempts, height = state[state_key]
      loops = ((elephant_size - attempts) // (attempt - attempts)) - 1
      jump_height = loops * (cavern.height() - height)
      attempt += loops * (attempt - attempts)
      state = {}

    state[state_key] = (attempt, cavern.height())

    if attempt == human_size:
      print(f'Tower height after {human_size} moves: {jump_height + cavern.height()}')

  print(f'Tower height after {elephant_size} moves: {jump_height + cavern.height()}')

if __name__ == '__main__':
  main()