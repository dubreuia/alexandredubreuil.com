import os
import time
from typing import List

import numpy as np
import tensorflow as tf
from magenta.models.nsynth.utils import load_audio
from magenta.models.nsynth.wavenet import fastgen

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string(
  "log", "DEBUG",
  "The threshold for what messages will be logged. DEBUG, INFO, WARN, ERROR, "
  "or FATAL.")

tf.app.flags.DEFINE_string(
  "checkpoint",
  "checkpoints/wavenet-ckpt/model.ckpt-200000",
  "The checkpoint to use, defaults to wavenet")

tf.app.flags.DEFINE_string(
  "wav1",
  "sounds/160045__jorickhoofd__metal-hit-with-metal-bar-resonance__crop.wav",
  "The first sample to mix, defaults to a metal piece hit of 1 second")

tf.app.flags.DEFINE_string(
  "wav2",
  "sounds/412017__skymary__cat-meow-short__crop.wav",
  "The second sample to mix, defaults to a cute cat meow of 1 second")

tf.app.flags.DEFINE_integer(
  "sample_length",
  16000,
  "The sample length of the provided samples (and the resulting generation), "
  "the samples needs to have the same length, defaults to 1 second")

tf.app.flags.DEFINE_integer(
  "sample_rate",
  16000,
  "The sample rate of the provided samples, defaults to 16000 second")


def encode(paths: List[str],
           sample_length: int = 16000,
           sample_rate: int = 16000,
           checkpoint: str = "checkpoints/wavenet-ckpt/model.ckpt-200000") \
    -> np.ndarray:
  # TODO load audio and encode it using nsynth
  pass


def mix(encoding1: np.ndarray,
        encoding2: np.ndarray) \
    -> np.ndarray:
  # TODO mix the encodings together
  pass


def synthesize(encoding_mix: np.ndarray,
               checkpoint: str = "checkpoints/wavenet-ckpt/model.ckpt-200000"):
  os.makedirs(os.path.join("output", "synth"), exist_ok=True)
  date_and_time = time.strftime("%Y-%m-%d_%H%M%S")
  output = os.path.join("output", "synth", f"{date_and_time}.wav")
  # TODO synthetize the encodings into audio with nsynth
  pass


def app(unused_argv):
  encoding1, encoding2 = encode([FLAGS.wav1, FLAGS.wav2],
                                sample_length=FLAGS.sample_length,
                                sample_rate=FLAGS.sample_rate,
                                checkpoint=FLAGS.checkpoint)
  encoding_mix = mix(encoding1, encoding2)
  synthesize(encoding_mix, checkpoint=FLAGS.checkpoint)


if __name__ == "__main__":
  tf.logging.set_verbosity(FLAGS.log)
  tf.app.run(app)
