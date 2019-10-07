import os
import threading
import time

import magenta.music as mm
import pretty_midi as pm
import tensorflow as tf
from magenta.interfaces.midi.midi_interaction import adjust_sequence_times
from magenta.music import sequences_lib, DEFAULT_STEPS_PER_QUARTER
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2
from magenta.protobuf.music_pb2 import NoteSequence
from visual_midi import Plotter, Preset

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
               sequence_generator,
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
    self._sequence_generator = self._get_sequence_generator(sequence_generator)
    if self._sequence_generator.steps_per_quarter != DEFAULT_STEPS_PER_QUARTER:
      raise Exception(f"Wrong sequence generation number of steps, "
                      f"expected: {DEFAULT_STEPS_PER_QUARTER}, "
                      f"actual: {self._sequence_generator.steps_per_quarter}")
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

  def _get_sequence_generator(self, sequence_generator_generator):
    mm.notebook_utils.download_bundle(self._bundle_filename, "bundles")
    bundle = mm.sequence_generator_bundle.read_bundle_file(
      os.path.join("bundles", self._bundle_filename))

    generator_map = sequence_generator_generator.get_generator_map()
    sequence_generator = generator_map[self._config_name](
      checkpoint=None, bundle=bundle)
    sequence_generator.initialize()

    return sequence_generator

  def _reset_tempos(self, sequence: NoteSequence):
    if sequence.tempos:
      sequence.tempos.remove(sequence.tempos[0])
    tempo = sequence.tempos.add()
    tempo.qpm = self._timing.qpm
    tempo.time = 0
    return sequence

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
      # Update sequence tempo
      sequence = self._reset_tempos(sequence)

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
      generator_options = generator_pb2.GeneratorOptions()
      generator_options.args['temperature'].float_value = 1
      generator_options.generate_sections.add(
        start_time=generation_start_time,
        end_time=generation_end_time)

      action = self._action_server.context.get(self.name, None)

      tf.logging.debug(str(action) + " " + str([
        ("expected_start_time", expected_start_time),
        ("loop_start_time", loop_start_time),
        ("loop_end_time", loop_end_time),
        ("generation_start_time", generation_start_time),
        ("generation_end_time", generation_end_time)]))

      def reset(seq):
        seq = music_pb2.NoteSequence()
        seq = loop(seq)
        return seq

      def loop(seq):
        seq = sequences_lib.trim_note_sequence(seq,
                                               loop_start_time,
                                               loop_end_time)
        seq = sequences_lib.shift_sequence_times(seq, seconds_per_loop)
        seq = self._reset_tempos(seq)
        return seq

      def generate(seq):
        if generation_start_time < seq.total_time:
          tf.logging.error(self.name + " generation error" + str([
            ("generation_start_time", generation_start_time),
            ("total_time", seq.total_time)]))
          return reset(seq)
        seq = self._sequence_generator.generate(seq, generator_options)
        seq = sequences_lib.trim_note_sequence(seq,
                                               generation_start_time,
                                               generation_end_time)
        return seq

      if not action:
        pass
      elif action is ActionType.LOOP:
        sequence = loop(sequence)
      elif action is ActionType.GENERATE:
        sequence = generate(sequence)
      elif action is ActionType.GENERATE_ONCE:
        sequence = generate(sequence)
        self._action_server.context[self.name] = ActionType.LOOP
      elif action is ActionType.GENERATE_4_BARS:
        if bar_count % 4 == 0:
          sequence = generate(sequence)
        else:
          sequence = loop(sequence)
      elif action is ActionType.RESET_ONCE:
        sequence = reset(sequence)
        self._action_server.context[self.name] = ActionType.LOOP
      else:
        raise Exception(f"Unknown action {action}")

      while True:
        # Unlock at the start of the bar
        self._bar_start_event.wait()
        bar_count += 1
        if bar_count % self._bar_per_loop == 0:
          break
