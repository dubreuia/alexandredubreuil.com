# Music Generation with Magenta: Using Machine Learning in Arts

**2019/15/10**

> This is the text transcript of the presentation [Music Generation with Magenta: Using Machine Learning in Arts](https://alexandredubreuil.com/conferences/music-generation-with-magenta/music-generation-with-magenta-using-machine-learning-in-arts.html), made at Devoxx Belgium 2019.

## Outline

- [Generative Music](#generative-music)
    - [Make music without being a musician](#make-music-without-being-a-musician)
    - ["Why you should build silly things" - Monica Dinculescu](#why-you-should-build-silly-things---monica-dinculescu)
    - [Helping people build generative systems](#helping-people-build-generative-systems)
    - ["The weird and the strange is good" - Brian Eno](#the-weird-and-the-strange-is-good---brian-eno)
    - [Representation: MIDI](#representation-midi)
    - [Representation: audio](#representation-audio)
    - [Machine Learning](#machine-learning)
    - [Music generation with RNNs (MIDI)](#music-generation-with-rnns-midi)
    - [Long-term structure with LSTMs (MIDI)](#long-term-structure-with-lstms-midi)
    - [Latent space interpolation with VAEs (MIDI)](#latent-space-interpolation-with-vaes-midi)
    - [Audio generation with WaveNet Autoencoders (audio)](#audio-generation-with-wavenet-autoencoders-audio)
    - [What's in Magenta?](#whats-in-magenta)
- [Live code: Generate a track](#live-code-generate-a-track)
    - [STEP 1: make everything sound like a cat](#step-1-make-everything-sound-like-a-cat)
    - [STEP 1: The sounds](#step-1-the-sounds)
    - [STEP 1: Entry point](#step-1-entry-point)
    - [STEP 1: Encode](#step-1-encode)
    - [STEP 1: Mix](#step-1-mix)
    - [STEP 1: Synthesize](#step-1-synthesize)
    - [STEP 1: GANSynth](#step-1-gansynth)
    - [STEP 1: The results](#step-1-the-results)
    - [STEP 2: sequence the cats](#step-2-sequence-the-cats)
    - [STEP 2: Reset](#step-2-reset)
    - [STEP 2: Loop](#step-2-loop)
    - [STEP 2: Generate](#step-2-generate)
    - [STEP 2: Sequence generator](#step-2-sequence-generator)
    - [Wrapping up](#wrapping-up)
    - [Can we do better?](#can-we-do-better)
- [Training](#training)
    - [Why?](#why)
    - [Datasets: LAKHS (midi)](#datasets-lakhs-midi)
    - [Datasets: NSynth (audio)](#datasets-nsynth-audio)
    - [Building the dataset](#building-the-dataset)
    - [Create SequenceExamples](#create-sequenceexamples)
    - [Train and evaluate the model](#train-and-evaluate-the-model)
    - [Tensorboard](#tensorboard)
- [Interaction with the outside world](#interaction-with-the-outside-world)
    - [Python to everything using MIDI](#python-to-everything-using-midi)
    - [Magenta in the browser with Magenta.js](#magenta-in-the-browser-with-magentajs)
    - [Melody Mixer](#melody-mixer)
    - [Neural Drum Machine](#neural-drum-machine)
    - [GANHarp](#ganharp)
    - [Easy peasy](#easy-peasy)
    - [Magenta in your DAW with Magenta Studio](#magenta-in-your-daw-with-magenta-studio)
- [Closing](#closing)
    - [Dreambank - Can a machine dream?](#dreambank---can-a-machine-dream)
    - [Hands-on Music Generation with Magenta](#hands-on-music-generation-with-magenta)


## Generative Music

"Generative art is an artwork partially or completely created by an autonomous system."

### Make music without being a musician

Maybe you don't know how to <strong>improvise</strong>, maybe you need help to <strong>compose</strong>.

### "Why you should build silly things" - Monica Dinculescu
    
It is okay to make art without taking ourselves seriously. The important thing is to <strong>create systems that makes this possible</strong>.

### Helping people build generative systems

Art exhibit, generative radio, interactive art.

### "The weird and the strange is good" - Brian Eno

Generative systems makes tons of mistakes (also humans), <strong>but mistakes are good</strong>.

### Representation: MIDI

MIDI is a musical representation analogous to <strong>sheet music</strong>, where note has a pitch, velocity, and time.

Working with MIDI shows the underlying <strong>structure of the music</strong>, but doesn't define the actual sound, you'll need to use instruments (numeric or analogic).

<img src="../../conferences/music-generation-with-magenta/resources/midi.png" alt="MIDI diagram"/>

### Representation: audio

Working with audio is harder because you have to handle 16000 samples per seconds (at least) and keep track of the general structure. Generating audio is more direct than MIDI.

<img src="../../conferences/music-generation-with-magenta/resources/spectrogram.png" alt="Audio diagram"/>
<!-- https://upload.wikimedia.org/wikipedia/commons/c/c5/Spectrogram-19thC.png -->

### Machine Learning

Hand crafting the rules of a painting or the rules of a music style might be a hard task. That's why Machine Learning is so interesting in arts: it can learn complex functions.

### Music generation with RNNs (MIDI)

<img src="../../conferences/music-generation-with-magenta/resources/rnn.png" alt="RNN diagram"/>
<!-- https://www.asimovinstitute.org/wp-content/uploads/2016/09/rnn.png -->

Recurrent Neural Networks (RNNs) solves two important properties for music generation: they <strong>operate on sequences for the inputs and outputs</strong> and they <strong>can remember past events</strong>.

### Long-term structure with LSTMs (MIDI)

<img src="../../conferences/music-generation-with-magenta/resources/lstm.png" alt="LSTM diagram"/>
<!-- https://www.asimovinstitute.org/wp-content/uploads/2016/09/lstm.png -->
          
Most RNN uses Long Short-Term Memory (LSTM) cells, since by themselves, RNNs are hard to train because of the problems of vanishing and exploding gradient, making long-term dependencies hard to learn.

By using <strong>input, output and forget gates</strong> in the cell, LSTMs can learn mechanisms to keep or forget information as they go.

### Latent space interpolation with VAEs (MIDI)

<img src="../../conferences/music-generation-with-magenta/resources/vae.png" alt="VAE diagram"/>
<!-- https://www.asimovinstitute.org/wp-content/uploads/2016/09/vae.png -->

Variational Autoencoders (VAEs) are a pair of networks where an encoder reduces the input to a lower dimensionality (<strong>latent space</strong>), from which a decoder tries to reproduce the input.

The latent space is continuous and follows a probability distribution, meaning it is possible to sample from it. VAEs are inherently generative models: they can <strong>sample</strong> and <strong>interpolate</strong> (smoothly move in the latent space) between two points.

href="">https://www.asimovinstitute.org/wp-content/uploads/2016/09/vae.png</a></span>

### Audio generation with WaveNet Autoencoders (audio)

<img src="../../conferences/music-generation-with-magenta/resources/wavenet.png" alt="Wavenet diagram"/>
<!-- https://magenta.tensorflow.org/assets/nsynth_05_18_17/encoder-decoder.png -->

WaveNet is a convolutional neural network (CNN) taking raw signal as an input and synthesizing output audio sample by sample.

The WaveNet Autoencoder present in Magenta is a Wavenet-style AE network capable of learning its own temporal embedding, resulting in a latent space from which is it possible to <strong>sample </strong> and <strong>mix</strong> elements.

### What's in Magenta?

<table class="smaller">
  <thead>
  <tr>
    <th>Model</th>
    <th>Network</th>
    <th>Repr.</th>
    <th>Encoding</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>DrumsRNN</td>
    <td>LSTM</td>
    <td>MIDI</td>
    <td>polyphonic-ish</td>
  </tr>
  <tr>
    <td>MelodyRNN</td>
    <td>LSTM</td>
    <td>MIDI</td>
    <td>monophonic</td>
  </tr>
  <tr>
    <td>PolyphonyRNN</td>
    <td>LSTM</td>
    <td>MIDI</td>
    <td>polyphonic</td>
  </tr>
  <tr>
    <td>PerformanceRNN</td>
    <td>LSTM</td>
    <td>MIDI</td>
    <td>polyphonic, groove</td>
  </tr>
  <tr>
    <td>MusicVAE</td>
    <td>VAE</td>
    <td>MIDI</td>
    <td>multiple</td>
  </tr>
  <tr>
    <td>NSynth</td>
    <td>Wavenet AE</td>
    <td>Audio</td>
    <td>-</td>
  </tr>
  <tr>
    <td>GANSynth</td>
    <td>GAN</td>
    <td>Audio</td>
    <td>-</td>
  </tr>
  </tbody>
</table>


## Live code: Generate a track

### STEP 1: make everything sound like a cat.

We'll use NSynth to mix cat sounds with other sounds.

### STEP 1: The sounds

<img src="../../conferences/music-generation-with-magenta/resources/rainbowgram-bass-01.png" class="no_border" alt="Audio diagram"/>
<audio controls>
<source src="../../conferences/music-generation-with-magenta/code/sounds/83249__zgump__bass-0205__crop.wav"
        type="audio/wav"/>
</audio>
        
<img src="../../conferences/music-generation-with-magenta/resources/rainbowgram-metal-01.png" class="no_border" alt="Audio diagram"/>
<audio controls>
<source
    src="../../conferences/music-generation-with-magenta/code/sounds/160045__jorickhoofd__metal-hit-with-metal-bar-resonance__crop.wav"
    type="audio/wav"/>
</audio>

<img src="../../conferences/music-generation-with-magenta/resources/rainbowgram-cat-01.png" class="no_border" alt="Audio diagram"/>
<audio controls>
<source src="../../conferences/music-generation-with-magenta/code/sounds/412017__skymary__cat-meow-short__crop.wav"
        type="audio/wav"/>
</audio>

<img src="../../conferences/music-generation-with-magenta/resources/rainbowgram-flute-01.png" class="no_border" alt="Audio diagram"/>
<audio controls>
<source src="../../conferences/music-generation-with-magenta/code/sounds/427567__maria-mannone__flute__crop.wav"
        type="audio/wav"/>
</audio>

### STEP 1: Entry point

See "code/nsynth.py" and method <code>app</code> in this repo.

```python
def app(unused_argv):
encoding1, encoding2 = encode([FLAGS.wav1, FLAGS.wav2],
                    sample_length=FLAGS.sample_length,
                    sample_rate=FLAGS.sample_rate,
                    checkpoint=FLAGS.checkpoint)
encoding_mix = mix(encoding1, encoding2)
synthesize(encoding_mix, checkpoint=FLAGS.checkpoint)
```

### STEP 1: Encode

See "code/nsynth.py" and method <code>encode</code> in this repo.

```python
def encode(paths: List[str],
sample_length: int = 16000,
sample_rate: int = 16000,
checkpoint: str = "checkpoints/wavenet-ckpt/model.ckpt-200000") \
    -> np.ndarray:
    audios = []
    for path in paths:
    audio = utils.load_audio(path,
                     sample_length=sample_length,
                     sr=sample_rate)
    audios.append(audio)
    audios = np.array(audios)
    encodings = fastgen.encode(audios, checkpoint, sample_length)
    return encodings
```

### STEP 1: Mix

See "code/nsynth.py" and method <code>mix</code> in this repo.

```python
def mix(encoding1: np.ndarray,
encoding2: np.ndarray) \
    -> np.ndarray:
    encoding_mix = (encoding1 + encoding2) / 2.0
    return encoding_mix
```

### STEP 1: Synthesize

See "code/nsynth.py" and method <code>synthesize</code> in this repo.

```python
def synthesize(encoding_mix: np.ndarray,
   checkpoint: str = "checkpoints/wavenet-ckpt/model.ckpt-200000"):
    os.makedirs(os.path.join("output", "synth"), exist_ok=True)
    date_and_time = time.strftime("%Y-%m-%d_%H%M%S")
    output = os.path.join("output", "synth", f"{date_and_time}.wav")
    encoding_mix = np.array([encoding_mix])
    fastgen.synthesize(encoding_mix,
             checkpoint_path=checkpoint,
             save_paths=[output])
```

### STEP 1: GANSynth

As shown, the NSynth instrument is nice, but really slow for the
audio synthesis. You should use <strong>GANSynth</strong>.

### STEP 1: The results

<img src="../../conferences/music-generation-with-magenta/resources/83249_412017_rainbowgram_trim.png" class="no_border" alt="Audio diagram"/>
<span>Bass + Cat</span>
<audio controls>
  <source src="../../conferences/music-generation-with-magenta/code/sounds/83249_412017_bass_cat.wav"
          type="audio/wav"/>
</audio>

<img src="../../conferences/music-generation-with-magenta/resources/83249_427567_rainbowgram_trim.png" class="no_border" alt="Audio diagram"/>
<span>Bass + Flute</span>
<audio controls>
  <source src="../../conferences/music-generation-with-magenta/code/sounds/83249_427567_bass_flute.wav"
          type="audio/wav"/>
</audio>

<img src="../../conferences/music-generation-with-magenta/resources/83249_160045_rainbowgram_trim.png" class="no_border" alt="Audio diagram"/>
<span>Bass + Metal</span>
<audio controls>
  <source src="../../conferences/music-generation-with-magenta/code/sounds/83249_160045_bass_metal.wav"
          type="audio/wav"/>
</audio>

<img src="../../conferences/music-generation-with-magenta/resources/160045_83249_rainbowgram_trim.png" class="no_border" alt="Audio diagram"/>
<span>Metal + Bass</span>
<audio controls>
  <source src="../../conferences/music-generation-with-magenta/code/sounds/160045_83249_metal_bass.wav"
          type="audio/wav"/>
</audio>

<img src="../../conferences/music-generation-with-magenta/resources/160045_412017_rainbowgram_trim.png" class="no_border" alt="Audio diagram"/>
<span>Metal + Cat</span>
<audio controls>
  <source src="../../conferences/music-generation-with-magenta/code/sounds/160045_412017_metal_cat.wav"
          type="audio/wav"/>
</audio>

<img src="../../conferences/music-generation-with-magenta/resources/160045_427567_rainbowgram_trim.png" class="no_border" alt="Audio diagram"/>
<span>Metal + Flute</span>
<audio controls>
  <source src="../../conferences/music-generation-with-magenta/code/sounds/160045_427567_metal_flute.wav"
          type="audio/wav"/>
</audio>

### STEP 2: sequence the cats

We'll use DrumsRNN and MelodyRNN to generate MIDI to play the
samples.

### STEP 2: Reset

See "code/sequences.py" and method <code>reset</code> in this repo.

```python
def reset(loop_start_time: float,
loop_end_time: float,
seconds_per_loop: float):
    sequence = music_pb2.NoteSequence()
    sequence = loop(sequence,
          loop_start_time,
          loop_end_time,
          seconds_per_loop)
    return sequence
```

### STEP 2: Loop

See "code/sequences.py" and method <code>loop</code> in this repo.

```python
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
```

### STEP 2: Generate

See "code/sequences.py" and method <code>generate</code> in this repo.

```python
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
```

### STEP 2: Sequence generator

See "code/sequences.py" and method
<code>get_sequence_generator</code> in this repo.

```python
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
```

### Wrapping up

This generative music demo helped us improvise and compose around an
idea: a track composed of a percussion, a melody, and a cat
&#x1F63A;. We could <strong>interact</strong> with the system
and it helped us improvise around a theme.

### Can we do better?

Was it perfect? No, we had little happy accidents.

<img src="../../conferences/music-generation-with-magenta/resources/bob-ross.jpg" alt="RNN diagram"/>
<!-- https://2.bp.blogspot.com/_s5_5vgBh1Zo/TJVmnBJW-bI/AAAAAAAAAHc/Mcgu8_el_84/s1600/Bob_Ross.jpg -->

Maybe we could have had more control over the sequences. Maybe we
wanted to improvise around a <strong>musical style</strong>,
or a <strong>specific structure</strong>.

## Training

### Why?

The pre-trained models in Magenta are good, but if for example
you want to generate a <strong>specific style</strong>, generate a
<strong>specific time signature</strong> (3/4 for example), or a
<strong>specific instrument </strong>(cello for example) you'll
need to train your own.

### Datasets: LAKHS (MIDI)

A good place to start is the LAKHS dataset, a 180,000 MIDI files
dataset, (partially) matched with the Million Song Dataset
(metadata like artist, release, genre).

- https://colinraffel.com/projects/lmd/
- http://millionsongdataset.com/

### Datasets: NSynth (audio)

A large-scale and high-quality dataset of annotated musical notes.
Training audio requires lots of ../../conferences/music-generation-with-magenta/resources, but can be achieved using
GANSynth.

- https://magenta.tensorflow.org/datasets/nsynth

### Building the dataset

From MIDI, ABCNotation, MusicXML files to <code>NoteSequence</code>.

```bash
convert_dir_to_note_sequences \
--input_dir="/path/to/dataset/jazz_midi/drums/v1" \
--output_file="/tmp/notesequences.tfrecord" \
--recursive
```
```bash
...
Converted MIDI file /path/to/dataset/jazz_midi/drums/v1/TRVUCSW12903CF536D.mid.
Converted MIDI file /path/to/dataset/jazz_midi/drums/v1/TRWSJLM128F92DF651.mid.
...
```

### Create SequenceExamples

The sequence examples are fed into the model, it contains a sequence
of inputs and a sequence of labels that represents the drum track.
Those are split to eval and training sets.

```bash
drums_rnn_create_dataset \
--config="drum_kit" \
--input="/tmp/notesequences.tfrecord" \
--output_dir="/tmp/drums_rnn/sequence_examples" \
--eval_ratio=0.10
```
```bash
...
DAGPipeline_DrumsExtractor_training_drum_track_lengths_in_bars:
[8,10): 1
[10,20): 8
[20,30): 8
[30,40): 29
[40,50): 1
[50,100): 2
...
```

### Train and evaluate the model

Launch the training, using a specific configuration and
hyperparameters.

```bash
drums_rnn_train \
--config="drum_kit" \
--run_dir="/tmp/drums_rnn/logdir/run1" \
--sequence_example_file="/tmp/drums_rnn/sequence_examples/training_drum_tracks.tfrecord" \
--hparams="batch_size=64,rnn_layer_sizes=[64,64]" \
--num_training_steps=20000
```
```bash
...
Saving checkpoints for 0 into /tmp/drums_rnn/logdir/run1/train/model.ckpt.
Accuracy = 0.013341025, Global Step = 1, Loss = 6.2323294, Perplexity = 508.9396
Accuracy = 0.43837976, Global Step = 11, Loss = 5.1239195, Perplexity = 167.99252 (50.009 sec)
global_step/sec: 0.199963
Saving checkpoints for 12 into /tmp/drums_rnn/logdir/run1/train/model.ckpt.
...
```

### Tensorboard

You can launch TensorBoard and go to http://localhost:6006 to view
the TensorBoard dashboard.

```bash
tensorboard --logdir="/tmp/drums_rnn/logdir"
```

## Interaction with the outside world

### Python to everything using MIDI

Magenta can send MIDI, which is understood by basically everything
that makes sound: <strong>DAWs</strong> (like Ableton Live),
<strong>software synthesizers</strong> (like fluidsynth),
<strong>hardware synthesizers</strong> (though USB or MIDI cable),
etc.

### Magenta in the browser with Magenta.js

You can use Magenta and most of its models in the browser, using
Magenta.js (which in turns uses Tensorflow.js).

### Melody Mixer

<img src="../../conferences/music-generation-with-magenta/resources/melody-mixer.png" alt="RNN diagram"/>
<!-- https://experiments.withgoogle.com/ai/melody-mixer/view/ -->

### Neural Drum Machine

<img src="../../conferences/music-generation-with-magenta/resources/neural-drum-machine.png" alt="RNN diagram"/>
<!-- https://codepen.io/teropa/full/JLjXGK -->

### GANHarp

<img src="../../conferences/music-generation-with-magenta/resources/ganharp.png" alt="RNN diagram"/>
<!-- https://ganharp.ctpt.co -->

### Easy peasy

```html
<html>
    <head>
        <!-- Load @magenta/music -->
        <script src="https://cdn.jsdelivr.net/npm/@magenta/music@^1.0.0">
        </script>
        <script>
            // Instantiate model by loading desired config.
            const model = new mm.MusicVAE(
                'https://storage.googleapis.com/magentadata/' +
                'js/checkpoints/music_vae/trio_4bar');
            const player = new mm.Player();
            
            // Samples from MusicVAE and play the sample
            function play() {
                player.resumeContext();
                model.sample(1)
                     .then((samples) => player.start(samples[0], 80));
            }
        </script>
    </head>
    <body><button onclick="play()"><h1>Play Trio</h1></button></body>
</html>
```

### Magenta in your DAW with Magenta Studio

Using Magenta.js and Max4Live (MaxMSP) process, Magenta Studio can
be used directly in Ableton Live.

<video autoplay="" loop="" muted="" playsinline="">
<source src="../common/video/hero.mp4" type="video/mp4">
</video>
<!-- https://magenta.tensorflow.org/studio/assets/studio/hero.mp4 -->

## Closing

### Dreambank - Can a machine dream?

Generative music using Magenta and Ableton Live.
<img src="../../conferences/music-generation-with-magenta/resources/dreambank.jpg" alt="Dreambank image"/>

### Hands-on Music Generation with Magenta

Upcoming book on <strong>Packt Publishing</strong>, expected
publication date in <strong>January 2020</strong>.

<img src="../../conferences/music-generation-with-magenta/resources/magenta-book-icon.png" alt="Dreambank image"/>
<img src="../../conferences/music-generation-with-magenta/resources/packt-logo.png" alt="Dreambank image"/>
