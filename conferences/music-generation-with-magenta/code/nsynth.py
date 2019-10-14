import time

import tensorflow as tf
from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string(
  "checkpoint",
  "checkpoints/wavenet-ckpt/model.ckpt-200000",
  "TODO")

tf.app.flags.DEFINE_string(
  "wav1",
  "synth/83249__zgump__bass-0205-crop.wav",
  "TODO")

tf.app.flags.DEFINE_string(
  "wav2",
  "synth/371192__karolist__acoustic-kick-long.wav",
  "TODO")

tf.app.flags.DEFINE_integer(
  "sample_length",
  80000,
  "TODO")


def encode(wav: str,
           sample_length: int = None,
           sample_rate: int = 16000,
           checkpoint=None):
  audio = utils.load_audio(wav,
                           sample_length=sample_length,
                           sr=sample_rate)
  encoding = fastgen.encode(audio, checkpoint, sample_length)
  return encoding


def mix(wav1: str,
        wav2: str,
        sample_length: int = None,
        sample_rate: int = 16000,
        checkpoint=None):
  encoding1 = encode(wav1, sample_length, sample_rate, checkpoint)
  encoding2 = encode(wav2, sample_length, sample_rate, checkpoint)
  encoding_mix = (encoding1 + encoding2) / 2.0
  return encoding_mix


if __name__ == "__main__":
  # TODO check sample length
  encoding_mix = mix(FLAGS.wav1,
                     FLAGS.wav2,
                     FLAGS.sample_length,
                     checkpoint=FLAGS.checkpoint)
  date_and_time = time.strftime("%Y-%m-%d_%H%M%S")
  fastgen.synthesize(encoding_mix,
                     checkpoint_path=FLAGS.checkpoint,
                     save_paths=[f"output/synth/{date_and_time}.wav"])
