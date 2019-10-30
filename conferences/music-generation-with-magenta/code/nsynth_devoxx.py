import os
import time

import numpy as np
import tensorflow as tf
from magenta.models.nsynth import utils
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
  "The sample length of the provided samples (and the resultig generation), "
  "the samples needs to have the same length, defaults to 1 second")


def app(unused_argv):
  encoding_mix = mix(FLAGS.wav1,
                     FLAGS.wav2,
                     FLAGS.sample_length,
                     checkpoint=FLAGS.checkpoint)
  date_and_time = time.strftime("%Y-%m-%d_%H%M%S")
  output = os.path.join("output", "synth", f"{date_and_time}.wav")
  synthesize(encoding_mix, output)


def mix(wav1: str,
        wav2: str,
        sample_length: int = 16000,
        sample_rate: int = 16000,
        checkpoint: str = "checkpoints/wavenet-ckpt/model.ckpt-200000") \
    -> np.ndarray:
  encoding1 = encode(wav1, sample_length, sample_rate, checkpoint)
  encoding2 = encode(wav2, sample_length, sample_rate, checkpoint)
  # TODO mix the encodings together
  pass


def encode(wav: str,
           sample_length: int = 16000,
           sample_rate: int = 16000,
           checkpoint: str = "checkpoints/wavenet-ckpt/model.ckpt-200000") \
    -> np.ndarray:
  # TODO load the audio and encode it
  pass


def synthesize(encoding_mix: np.ndarray, output: str) -> None:
  fastgen.synthesize(encoding_mix,
                     checkpoint_path=FLAGS.checkpoint,
                     save_paths=[output])


if __name__ == "__main__":
  tf.logging.set_verbosity(FLAGS.log)
  tf.app.run(app)
