import os
import threading
import time

import magenta.music as mm
import pretty_midi as pm
import tensorflow as tf
from magenta.interfaces.midi.midi_interaction import adjust_sequence_times
from magenta.protobuf import music_pb2
from visual_midi import Plotter, Preset

import sequences
from timing import Timing
from type import ActionType
from ws import ActionServer


class SequenceLooper(threading.Thread):
  def __init__(self,
               name: str,
               bar_start_event,
               action_server: ActionServer,
               midi_hub,
               bundle_name: str,
               config_name: str,
               timing: Timing,
               midi_channel: int = 1,
               bar_per_loop: int = 2):
    super(SequenceLooper, self).__init__()
    self.name = name
    self._stop_signal = False
    self._bar_start_event = bar_start_event
    self._action_server = action_server
    self._midi_hub = midi_hub
    self._bundle_filename = bundle_name + ".mag"
    self._config_name = config_name
    self._timing = timing
    self._midi_channel = midi_channel
    self._bar_per_loop = bar_per_loop
    model_dir = os.path.join("output", "models")
    if not os.path.exists(model_dir):
      os.makedirs(model_dir)
    self._output_plot = os.path.join("output", "models", self.name + ".html")
    self._output_midi = os.path.join("output", "models", self.name + ".mid")
    self._plotter = Plotter(plot_max_length_bar=16,
                            live_reload=True,
                            preset=Preset(config="PRESET_SMALL"))

  def stop(self):
    self._stop_signal = True

  def run(self):
    sequence = music_pb2.NoteSequence()
    player = self._midi_hub.start_playback(sequence, allow_updates=True)
    player._channel = self._midi_channel

    pretty_midi = pm.PrettyMIDI()
    pretty_midi.instruments.append(pm.Instrument(0))

    # Wait for the dreamer and store the time with the delta
    wall_start_time = time.time()
    self._bar_start_event.wait()

    bar_count = 0
    while not self._stop_signal:
      # Number of seconds we should be at the beginning of this loop
      expected_start_time = self._timing.get_expected_start_time(bar_count)
      # Number of actual seconds since we started this thread from wall clock,
      # which is smaller then the expected start time because
      # TODO I don't know why actually but it works
      # The difference is between: the actual wakeup time and the expected
      # (calculated) start time. By keeping this we can adjust the sequence
      # according to the drift.
      diff_time = self._timing.get_diff_time(wall_start_time, bar_count)

      tf.logging.debug("Playing " + str(self._timing.get_timing_args(
        wall_start_time, bar_count)))

      # Player
      sequence_adjusted = music_pb2.NoteSequence()
      sequence_adjusted.CopyFrom(sequence)
      sequence_adjusted = adjust_sequence_times(sequence_adjusted,
                                                wall_start_time - diff_time)
      player.update_sequence(sequence_adjusted, start_time=expected_start_time)

      # Plotter
      pretty_midi = mm.midi_io.note_sequence_to_pretty_midi(sequence)
      self._plotter.save(pretty_midi, self._output_plot)
      pretty_midi.write(self._output_midi)

      # Sets timing
      seconds_per_bar = self._timing.get_seconds_per_bar()
      seconds_per_loop = self._bar_per_loop * seconds_per_bar
      loop_start_time = expected_start_time
      loop_end_time = loop_start_time + seconds_per_loop
      generation_start_time = loop_end_time
      generation_end_time = generation_start_time + seconds_per_loop

      action = self._action_server.context.get(self.name, None)

      tf.logging.debug(str(action) + " " + str([
        ("expected_start_time", expected_start_time),
        ("loop_start_time", loop_start_time),
        ("loop_end_time", loop_end_time),
        ("generation_start_time", generation_start_time),
        ("generation_end_time", generation_end_time)]))

      if not action:
        pass
      elif action is ActionType.LOOP:
        sequence = sequences.loop(sequence,
                                  loop_start_time,
                                  loop_end_time,
                                  seconds_per_loop)
      elif action is ActionType.GENERATE:
        sequence = sequences.generate(sequence,
                                      self.name,
                                      self._bundle_filename,
                                      self._config_name,
                                      generation_start_time,
                                      generation_end_time)
      elif action is ActionType.GENERATE_ONCE:
        sequence = sequences.generate(sequence,
                                      self.name,
                                      self._bundle_filename,
                                      self._config_name,
                                      generation_start_time,
                                      generation_end_time)
        self._action_server.context[self.name] = ActionType.LOOP
      elif action is ActionType.RESET_ONCE:
        sequence = sequences.reset(loop_start_time,
                                   loop_end_time,
                                   seconds_per_loop)
        self._action_server.context[self.name] = ActionType.LOOP
      else:
        raise Exception(f"Unknown action {action}")

      while True:
        # Unlock at the start of the bar
        self._bar_start_event.wait()
        bar_count += 1
        if bar_count % self._bar_per_loop == 0:
          break
