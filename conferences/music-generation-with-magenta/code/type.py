from enum import Enum, auto


class ActionType(Enum):
  LOOP = auto()
  GENERATE = auto()
  GENERATE_ONCE = auto()
  RESET_ONCE = auto()
  RESET_GENERATE = auto()
  STOP = auto()
