# Music Generation with Magenta Code Samples

## Installation

Installing with [miniconda](https://docs.conda.io/en/latest/miniconda.html) is easier, we need Magenta version 1.1.7.

```bash
# Create and activate new conda environment
conda create --name magenta python=3.6
conda activate magenta

# Install python dependencies
pip install magenta==1.1.7 \
            visual_midi \
            python-socketio \ 
            eventlet \
            scikit-image

# Install javascript dependencies
npm install
```

## Usage

```bash
# Start application, then go to http://127.0.0.1:5000/ and click stuff
python app.py

# TODO start live
# TODO check cello sounds for the synth like https://www.youtube.com/watch?time_continue=97&v=rU2ieu5o5DQ
```

```bash
# TODO
curl --output "checkpoints/wavenet-ckpt.tar" "http://download.magenta.tensorflow.org/models/nsynth/wavenet-ckpt.tar"

# TODO
python nsynth.py --checkpoint="checkpoints/wavenet-ckpt/model.ckpt-200000" --wav1="sounds/83249__zgump__bass-0205-crop.wav" --wav2="sounds/371192__karolist__acoustic-kick-long.wav" --sample_length="80000"
```

## Magenta.js demos

- [IRCAM demo 01](https://alexandredubreuil.com/conferences/music-generation-with-magenta/code/ircam-demo-01.html): Showcase a simple usage of GanSynth
- [IRCAM demo 02](https://alexandredubreuil.com/conferences/music-generation-with-magenta/code/ircam-demo-02.html): Showcase a combined usage of MusicVae and GanSynth

## Freesounds

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication:

- The wav file "sounds/83249__zgump__bass-0205.wav" is from
https://freesound.org/people/zgump/sounds/83249/
- The wav file "sounds/371192__karolist__acoustic-kick.wav" is from
https://freesound.org/people/karolist/sounds/371192/
