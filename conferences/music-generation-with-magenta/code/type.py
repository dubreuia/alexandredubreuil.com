from enum import Enum


class ActionType(Enum):
  LOOP = 0
  GENERATE = 1
  GENERATE_ONCE = 2
  GENERATE_4_BARS = 3
  RESET_ONCE = 4
  STOP = 5
