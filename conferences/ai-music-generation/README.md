# AI music generation

Overview of some AI music generation tools. We'll talk about music generation in general, real world examples, wavenet for voice, magenta for music, AI theory and state of the art.

## Introduction

- generative music spectrum
    - no generation
    - generative playback (playing recorded samples)
    - generative composition (generating score, but not instruments)
    - generative music (generating audio)
    - ... ?
- generative art http://claire-malrieux.com/ (music and image)
    - atlas du temps présent (musée des arts déco 2014): generative playback
    - climat general (venice art biennale 2017): generative playback
    - dreambank (venice art biennale 2019): generative composition
- dreambank (http://www.dreambank.net/)
    - based on a corpus of text
    - can a machine "dream"?
- what we'll see today
    - usage of tools (wavenet, magenta)
    - training on data (magenta)
    - state of the art on AI generative music

## Generative composition

### Wavenet (google / tensorflow)

Voice generation

- using an open source implementation (https://github.com/ibab/tensorflow-wavenet and others)
- using the public api

```bash
# Call Google wavenet API with curl on text/dreambank.quotes
# (one call per line in file, with voice parameters)
./quote2speech text/dreambank.quotes output/voice/mp3
```

### Magenta models (google / tensoflor)

Generative composition. Some pre-trained models are available in magenta.

- image
   - sketch rnn: https://github.com/tensorflow/magenta/tree/master/magenta/models/sketch_rnn
   - style transfert: https://github.com/tensorflow/magenta/tree/master/magenta/models/image_stylization
- score
    - drums rnn: https://github.com/tensorflow/magenta/tree/master/magenta/models/drums_rnn
    - improv rnn: https://github.com/tensorflow/magenta/tree/master/magenta/models/improv_rnn
    - melody rnn: https://github.com/tensorflow/magenta/tree/master/magenta/models/melody_rnn
    - music vae: https://github.com/tensorflow/magenta/tree/master/magenta/models/music_vae
    - onsets and frames: https://github.com/tensorflow/magenta/tree/master/magenta/models/onsets_frames_transcription
    - performance rnn: https://github.com/tensorflow/magenta/tree/master/magenta/models/performance_rnn
    - pianoroll rnn-nade: https://github.com/tensorflow/magenta/tree/master/magenta/models/pianoroll_rnn_nade
    - polyphony rnn: https://github.com/tensorflow/magenta/tree/master/magenta/models/polyphony_rnn
- music
    - nsynth: https://github.com/tensorflow/magenta/tree/master/magenta/models/nsynth

#### Installing Magenta

See https://github.com/tensorflow/magenta#installation.

```bash
# Python 2.x or 3.x
sudo apt install python-pip
# See https://pypi.org/project/magenta/
sudo pip install magenta
# If you want GPU support
pip install magenta-gpu
```

Or build from sources

- git clone magenta (https://github.com/tensorflow/magenta-demos.git)
- install bazel (https://docs.bazel.build/versions/master/install-ubuntu.html)

```bash
bazel build //magenta/tools/pip:build_pip_package
./magenta/tools/build.sh
```

To build then execute a specific target

```bash
bazel build //magenta/models/music_vae:music_vae_generate
bazel-bin/magenta/models/music_vae/music_vae_generate
```

#### Downloading models

```bash
mkdir -p models
mkdir -p checkpoints

# Drum kit RNN
wget -O models/drum_kit_rnn.mag "http://download.magenta.tensorflow.org/models/drum_kit_rnn.mag"

# Melody RNN
wget -O models/attention_rnn.mag "http://download.magenta.tensorflow.org/models/attention_rnn.mag"

# Polyphony RNN
wget -O models/polyphony_rnn.mag "http://download.magenta.tensorflow.org/models/polyphony_rnn.mag"

# Music VAE (2 GB per checkpoint)
wget -O checkpoints/mel_2bar_big.ckpt.tar "http://download.magenta.tensorflow.org/models/music_vae/checkpoints_bundled/mel_2bar_big.ckpt.tar"
wget -O checkpoints/mel_16bar_hierdec.ckpt.tar "http://download.magenta.tensorflow.org/models/music_vae/checkpoints_bundled/mel_16bar_hierdec.ckpt.tar"
wget -O checkpoints/trio_16bar_hierdec.ckpt.tar "http://download.magenta.tensorflow.org/models/music_vae/checkpoints_bundled/trio_16bar_hierdec.ckpt.tar"
wget -O checkpoints/drums_2bar_small.lokl.ckpt.tar "http://download.magenta.tensorflow.org/models/music_vae/checkpoints_bundled/drums_2bar_small.lokl.ckpt.tar"
wget -O checkpoints/drums_2bar_small.hikl.ckpt.tar "http://download.magenta.tensorflow.org/models/music_vae/checkpoints_bundled/drums_2bar_small.hikl.ckpt.tar"
wget -O checkpoints/drums_2bar_nade.full.ckpt.tar "http://download.magenta.tensorflow.org/models/music_vae/checkpoints_bundled/drums_2bar_nade.full.ckpt.tar"

# NSynth (2 GB per checkpoint)
wget -O checkpoints/baseline-ckpt.tar "http://download.magenta.tensorflow.org/models/nsynth/baseline-ckpt.tar"
wget -O checkpoints/wavenet-ckpt.tar "http://download.magenta.tensorflow.org/models/nsynth/wavenet-ckpt.tar"
```

#### Drums RNN (rythmics generation)

```bash
# Generate score based on single kick (default primer)
# (num_output: number of midi files out)
# (num_steps: number steps to generate, double the size of the primer)
# (temperature: smaller the value, closer to the primer)
drums_rnn_generate --config=drum_kit --bundle_file=models/drum_kit_rnn.mag --output_dir=output/drums_rnn/drum_kit/basic --num_outputs=10 --num_steps=64 --temperature=1

# Outputs log-likelihood: the smaller the value, the closer to the primer
# (close to primer)
# INFO:tensorflow:Beam search yields sequence with log-likelihood: -2.849966
# (far to primer)
# INFO:tensorflow:Beam search yields sequence with log-likelihood: -95.074890

# Generate score based on one step of bass drum and hi-hat, then one step of rest, then one step of just hi-hat
# (primer_drums: python array of midi note to prime the model)
drums_rnn_generate --config=drum_kit --bundle_file=models/drum_kit_rnn.mag --output_dir=output/drums_rnn/drum_kit/bd_hat --num_outputs=10 --num_steps=64 --temperature=1 --primer_drums="[(36, 42), (), (42,)]"

# Generate score based on jazz primer
# (primer_midi: midi file to prime the model)
drums_rnn_generate --config=drum_kit --bundle_file=models/drum_kit_rnn.mag --output_dir=output/drums_rnn/drum_kit/jazz --num_outputs=10 --num_steps=64 --temperature=1 --primer_midi=primer/jazz-drum-basic.mid

# Generate score based on jazz primer with high temperature
drums_rnn_generate --config=drum_kit --bundle_file=models/drum_kit_rnn.mag --output_dir=output/drums_rnn/drum_kit/jazz_temp --num_outputs=10 --num_steps=64 --temperature=1.5 --primer_midi=primer/jazz-drum-basic.mid
```

#### Melody / Polyphony RNN (melody generation)

```bash
# Generate score based on mario theme song (monophonic)
# (steps number: 7 bars * 16 steps each = 112 steps for primer)
# (steps number: 112 steps for primer * 2 for generation = 224 steps)
melody_rnn_generate --config=attention_rnn --bundle_file=models/attention_rnn.mag --output_dir=output/melody/attention_rnn/mario_mono --num_outputs=10 --num_steps=224 --primer_midi=primer/mario-cut-mono.mid

# Generate score based on mario theme song (polyphonic)
# (it doesn't work because it isn't trained on polyphonic data)
melody_rnn_generate --config=attention_rnn --bundle_file=models/attention_rnn.mag --output_dir=output/melody/attention_rnn/mario_poly --num_outputs=10 --num_steps=224 --primer_midi=primer/mario-cut-poly.mid

# Generate score based on mario theme song (polyphonic bis)
# (condition_on_primer: option to remove gap on first step of generation)
# (inject_primer_during_generation: same)
polyphony_rnn_generate --config=polyphony_rnn --bundle_file=models/polyphony_rnn.mag --output_dir=output/polyphony/polyphony_rnn/mario_poly --num_outputs=10 --num_steps=224 --primer_midi=primer/mario-cut-poly.mid --condition_on_primer=false --inject_primer_during_generation=true
```

#### Music VAE (score interpolation)

```bash
# Generate simple melodies
# (checkpoint_file: model training checkpoint)
# (mode: sample will generate a new output based on model checkpoint)
music_vae_generate --config=cat-mel_2bar_big --checkpoint_file=checkpoints/mel_2bar_big.ckpt.tar --mode=sample --num_outputs=5 --output_dir=output/music_vae/cat-mel_2bar_big/sample

# Generate more complex melodies (16 bar)
music_vae_generate --config=hierdec-mel_16bar --checkpoint_file=checkpoints/mel_16bar_hierdec.ckpt.tar --mode=sample --num_outputs=5 --output_dir=output/music_vae/hierdec-mel_16bar/sample

# Generate complex rythmics, melody and bass (full track!)
music_vae_generate --config=hierdec-trio_16bar --checkpoint_file=checkpoints/trio_16bar_hierdec.ckpt.tar --mode=sample --num_outputs=5 --output_dir=output/music_vae/hierdec-trio_16bar/sample

# Interpolate between two melodies (mario to zelda)
# (mode: interpolate will generate a new output between the two input provided)
music_vae_generate --config=cat-mel_2bar_big --checkpoint_file=checkpoints/mel_2bar_big.ckpt.tar --mode=interpolate --num_outputs=5 --input_midi_1=primer/mario-cut-2bar-mono.mid --input_midi_2=primer/zelda-cut-2bar-mono.mid --output_dir=output/music_vae/cat-mel_2bar_big/interpolate

# Then append the results together
python append.py output/music_vae/cat-mel_2bar_big/interpolate/mario-to-zelda.mid output/music_vae/cat-mel_2bar_big/interpolate/cat-mel_2bar_big_interpolate_*.mid

# Genere more drums
music_vae_generate --config=cat-drums_2bar_small --checkpoint_file=checkpoints/drums_2bar_small.lokl.ckpt.tar --mode=sample --num_outputs=5 --output_dir=output/music_vae/cat-drums_2bar_small/lokl/sample
music_vae_generate --config=cat-drums_2bar_small --checkpoint_file=checkpoints/drums_2bar_small.hikl.ckpt.tar --mode=sample --num_outputs=5 --output_dir=output/music_vae/cat-drums_2bar_small/hikl/sample
music_vae_generate --config=nade-drums_2bar_full --checkpoint_file=checkpoints/drums_2bar_nade.full.ckpt.tar --mode=sample --num_outputs=5 --output_dir=output/music_vae/nade-drums_2bar_full/sample
```

#### NSynth (audio synthesis)

Doesn't work (checkpoint too old?), test with online version: https://experiments.withgoogle.com/ai/sound-maker/view, see https://github.com/tensorflow/magenta/issues/1315.

```bash
# TODO "error NotFoundError (see above for traceback): Restoring from checkpoint failed. This is most likely due to a Variable name or other graph key that is missing from the checkpoint. Please ensure that you have not altered the graph expected based on the checkpoint"
nsynth_generate --checkpoint_path=checkpoints/wavenet-ckpt/wavenet-ckpt/model.ckpt-200000.index --source_path=wav --save_path=output/nsynth/wavenet --batch_size=4
```

#### Getting help

```bash
# For any command, use "--helpfull" to get the parameters
music_vae_generate --helpfull
```

### Training

- training is super important!
- what do you need? jazz rythmics model? techno melody model? very different
- building your dataset
  (https://github.com/tensorflow/magenta/blob/master/magenta/scripts/README.md)
    - lakh midi dataset (https://colinraffel.com/projects/lmd/), musescore,
      etc.
    - convert midi to NoteSequences (protobuf implementation of midi)
    - data processing in magenta
      (https://github.com/tensorflow/magenta/tree/master/magenta/pipelines)
- some training is out of reach for common mortals, from magenta documentation
  (https://github.com/tensorflow/magenta/tree/master/magenta/models/nsynth)
    - "Training for both these models is very expensive, and likely difficult
      for many practical setups. Nevertheless, We've included training code for
      completeness and transparency. The WaveNet model takes around 10 days
      on 32 K40 gpus (synchronous) to converge at ~200k iterations. The
      baseline model takes about 5 days on 6 K40 gpus (asynchronous)."
    - (K40: 1000 USD nvidia tesla graphic cards)

## AI theory

- RNN (https://en.wikipedia.org/wiki/Recurrent_neural_network): A recurrent
  neural network (RNN) is a class of artificial neural network where
  connections between nodes form a directed graph along a sequence. This allows
  it to exhibit temporal dynamic behavior for a time sequence. Unlike
  feedforward neural networks, RNNs can use their internal state (memory) to
  process sequences of inputs. This makes them applicable to tasks such as
  unsegmented, connected handwriting recognition or speech recognition.
- LSTM (https://en.wikipedia.org/wiki/Long_short-term_memory): Long short-term
  memory (LSTM) units are units of a recurrent neural network (RNN). An RNN
  composed of LSTM units is often called an LSTM network.  A common LSTM unit
  is composed of a cell, an input gate, an output gate and a forget gate. The
  cell remembers values over arbitrary time intervals and the three gates
  regulate the flow of information into and out of the cell.
- VAE (http://kvfrans.com/variational-autoencoders-explained/): An autoencoder
  is a type of artificial neural network used to learn efficient data codings
  in an unsupervised manner. The aim of an autoencoder is to learn a
  representation (encoding) for a set of data, typically for dimensionality
  reduction. Recently, the autoencoder concept has become more widely used for
  learning generative models of data. Some of the most powerful AI in the 2010s
  have involved sparse autoencoders stacked inside of deep neural networks.

## Tools (librairies / midi/ audio)

- Tensorflow: an open source machine learning framework (https://github.com/tensorflow/tensorflow)
- MuseScore: online library of scores (https://musescore.com/)
- MuseScore: application for score composition (https://musescore.org/en)
- TiMidity: midi player (http://timidity.sourceforge.net/)
- VcRack: software modular (https://vcvrack.com/)

## State of the art

- google wavenet (https://deepmind.com/blog/wavenet-generative-model-raw-audio/)
- facebook ai (https://www.youtube.com/watch?v=vdxCqNWTpUs / https://arxiv.org/abs/1805.07848)

