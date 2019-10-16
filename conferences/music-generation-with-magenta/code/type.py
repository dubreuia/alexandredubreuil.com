from enum import Enum


class ActionType(Enum):
  LOOP = 0
  GENERATE = 1
  GENERATE_ONCE = 2
  RESET_ONCE = 4
  STOP = 5
