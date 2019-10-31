import platform
import threading
import time

import mido
import tensorflow as tf
from magenta.interfaces.midi import midi_hub
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.models.melody_rnn import melody_rnn_sequence_generator

from constants import MIDI_INPUT_PORT, MIDI_OUTPUT_PORT
from model import SequenceLooper
from timing import Metronome
from timing import Timing
from ws import ActionServer

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string(
  "log", "INFO",
  "The threshold for what messages will be logged. DEBUG, INFO, WARN, ERROR, "
  "or FATAL.")


def app(unused_argv):
  tf.logging.debug("Starting app")

  # Start action server
  action_server = ActionServer()
  action_server.start()

  # Init midi ports, keep direct references to output_ports for
  # direct sending without the hub player
  if platform.system() == "Windows":
    input_ports = [port for port in midi_hub.get_available_input_ports()
                   if MIDI_INPUT_PORT in port]
    output_ports = [port for port in midi_hub.get_available_output_ports()
                    if MIDI_OUTPUT_PORT in port]
    if len(input_ports) is not 1 or len(output_ports) is not 1:
      raise Exception(f"Need exactly 1 midi input ({input_ports}) "
                      f"matching {MIDI_INPUT_PORT}"
                      f"and 1 midi output port ({output_ports}) "
                      f"matching {MIDI_OUTPUT_PORT},"
                      f"you can use LoopMIDI for that")
  else:
    input_ports = [MIDI_INPUT_PORT]
    output_ports = [MIDI_OUTPUT_PORT]
  hub = midi_hub.MidiHub(input_ports, output_ports, None)
  output_port = hub._outport.ports[0]

  # Panic to stop all current messages (note off everywhere)
  [output_port.send(message) for message in mido.ports.panic_messages()]

  # Synchronise event for all the loopers, controlled by the metronome
  bar_start_event = threading.Event()

  # Common stuff
  qpm = 80
  timing = Timing(qpm)

  loopers = []
  try:
    # Init and start the loopers, they block on the event
    drum_looper = SequenceLooper(
      "drums", bar_start_event, action_server, hub,
      "drum_kit_rnn", "drum_kit",
      timing, midi_channel=9, bar_per_loop=2)
    melody_looper = SequenceLooper(
      "melody", bar_start_event, action_server, hub,
      "attention_rnn", "attention_rnn",
      timing, midi_channel=0, bar_per_loop=4)

    loopers.append(drum_looper)
    loopers.append(melody_looper)
    [looper.start() for looper in loopers]

    tf.logging.debug("Loopers started " + str([
      ("drum_looper", drum_looper),
      ("melody_looper", melody_looper)]))

    # Start metronome (wait to make sure everything is started)
    time.sleep(1)
    metronome = Metronome(bar_start_event, timing)
    loopers.append(metronome)
    metronome.start()

    tf.logging.debug("Metronome started " + str([("metronome", metronome)]))

    # Wait for the loopers
    [looper.join() for looper in loopers]
  except KeyboardInterrupt:
    print("SIGINT received, stopping action server, loopers and stuff")
    action_server.stop()
    [looper.stop() for looper in loopers]
    return 1

  return 0


if __name__ == "__main__":
  tf.logging.set_verbosity(FLAGS.log)
  tf.app.run(app)
