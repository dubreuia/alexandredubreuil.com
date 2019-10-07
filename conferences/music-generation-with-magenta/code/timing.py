import threading
import time
from typing import List

import tensorflow as tf
from magenta.music import DEFAULT_QUARTERS_PER_MINUTE
from magenta.music import DEFAULT_STEPS_PER_BAR
from magenta.music import DEFAULT_STEPS_PER_QUARTER


class Timing:

  def __init__(self,
               qpm: float = DEFAULT_QUARTERS_PER_MINUTE,
               steps_per_quarter: int = DEFAULT_STEPS_PER_QUARTER,
               steps_per_bar: int = DEFAULT_STEPS_PER_BAR):
    self.qpm = qpm
    self.steps_per_quarter = steps_per_quarter
    self.steps_per_bar = steps_per_bar

  def get_seconds_per_step(self) -> float:
    return 60.0 / self.qpm / self.steps_per_quarter

  def get_seconds_per_bar(self) -> float:
    return self.steps_per_bar * self.get_seconds_per_step()

  def get_expected_start_time(self,
                              bar_count: int) -> float:
    return bar_count * self.get_seconds_per_bar()

  def get_relative_wall_time(self,
                             wall_start_time: float) -> float:
    return time.time() - wall_start_time

  def get_diff_time(self,
                    wall_start_time: float,
                    bar_count: int) -> float:
    expected_start_time = self.get_expected_start_time(bar_count)
    relative_wall_time = self.get_relative_wall_time(wall_start_time)
    return expected_start_time - relative_wall_time

  def get_sleep_time(self,
                     wall_start_time: float) -> float:
    seconds_per_bar = self.get_seconds_per_bar()
    relative_wall_time = self.get_relative_wall_time(wall_start_time)
    return seconds_per_bar - (relative_wall_time % seconds_per_bar)

  def get_timing_args(self,
                      wall_start_time: float,
                      bar_count: int) -> List[tuple]:
    return [
      ("qpm", self.qpm),
      ("wall_start_time", wall_start_time),
      ("bar_count", bar_count),
      ("seconds_per_step", self.get_seconds_per_step()),
      ("seconds_per_bar", self.get_seconds_per_bar()),
      ("expected_start_time", self.get_expected_start_time(bar_count)),
      ("relative_wall_time", self.get_relative_wall_time(wall_start_time)),
      ("diff_time", self.get_diff_time(wall_start_time, bar_count)),
      ("sleep_time", self.get_sleep_time(wall_start_time)),
    ]


class Metronome(threading.Thread):

  def __init__(self,
               output_port,
               bar_start_event,
               timing: Timing):
    super(Metronome, self).__init__()
    self._stop_signal = False
    self._output_port = output_port
    self._bar_start_event = bar_start_event
    self._timing = timing

  def stop(self):
    self._stop_signal = True

  def run(self):
    wall_start_time = time.time()

    bar_count = 0
    while not self._stop_signal:
      tf.logging.debug("Waking up " + str(
        self._timing.get_timing_args(wall_start_time, bar_count)))

      # Releases the waiting threads at the beginning of the bar
      self._bar_start_event.set()

      # Clears the signal so that threads block when they loop
      self._bar_start_event.clear()

      # Sleeps for the proper remaining time by removing the time it
      # took to execute this loop out of the expected next tick
      sleep_time = self._timing.get_sleep_time(wall_start_time)
      time.sleep(sleep_time)

      bar_count = bar_count + 1

    # Releases the waiting threads to exit
    self._bar_start_event.set()
