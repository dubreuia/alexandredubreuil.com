import os

import magenta.music as mm
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.music import sequences_lib as ss
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2
from magenta.protobuf.music_pb2 import NoteSequence


def reset(sequence: NoteSequence,
          loop_start_time: float,
          loop_end_time: float,
          seconds_per_loop: float):
  sequence = music_pb2.NoteSequence()
  sequence = loop(sequence,
                  loop_start_time,
                  loop_end_time,
                  seconds_per_loop)
  return sequence


def loop(sequence: NoteSequence,
         loop_start_time: float,
         loop_end_time: float,
         seconds_per_loop: float):
  sequence = ss.trim_note_sequence(sequence,
                                   loop_start_time,
                                   loop_end_time)
  sequence = ss.shift_sequence_times(sequence,
                                     seconds_per_loop)
  return sequence


def generate(sequence: NoteSequence,
             name: str,
             bundle_filename: str,
             config_name: str,
             generation_start_time: float,
             generation_end_time: float):
  generator_options = generator_pb2.GeneratorOptions()
  generator_options.args['temperature'].float_value = 1
  generator_options.generate_sections.add(
    start_time=generation_start_time,
    end_time=generation_end_time)
  sequence_generator = get_sequence_generator(name,
                                              bundle_filename,
                                              config_name)
  sequence = sequence_generator.generate(sequence,
                                         generator_options)
  sequence = ss.trim_note_sequence(sequence,
                                   generation_start_time,
                                   generation_end_time)
  return sequence


def get_sequence_generator(name: str,
                           bundle_filename: str,
                           config_name: str):
  if name == "drums":
    generator = drums_rnn_sequence_generator
  elif name == "melody":
    generator = melody_rnn_sequence_generator
  else:
    raise Exception(f"Unknown sequence generator {name}")

  mm.notebook_utils.download_bundle(bundle_filename, "bundles")
  bundle = mm.sequence_generator_bundle.read_bundle_file(
    os.path.join("bundles", bundle_filename))

  generator_map = generator.get_generator_map()
  sequence_generator = generator_map[config_name](
    checkpoint=None, bundle=bundle)
  sequence_generator.initialize()

  return sequence_generator
