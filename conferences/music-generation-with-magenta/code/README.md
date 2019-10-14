# Code for: Music Generation with Magenta

## Installation

Installing with conda or [miniconda](https://docs.conda.io/en/latest/miniconda.html) is easier.

```bash
# Create and activate new conda environment
conda create --name magenta python=3.6
conda activate magenta

# Install python dependencies
pip install magenta python-socketio eventlet scikit-image

# Install javascript dependencies
npm install
```

## Usage

```bash
# Start application, then go to http://127.0.0.1:5000/ and click stuff
python app.py
```

```bash
# TODO
curl --output "checkpoints/wavenet-ckpt.tar" "http://download.magenta.tensorflow.org/models/nsynth/wavenet-ckpt.tar"

# TODO
python nsynth.py --checkpoint="checkpoints/wavenet-ckpt/model.ckpt-200000" --wav1="synth/83249__zgump__bass-0205-crop.wav" --wav2="synth/371192__karolist__acoustic-kick-long.wav" --sample_length="80000"
```

## Freesounds

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication:

- The wav file "synth/83249__zgump__bass-0205-crop.wav" is a derived 
version of https://freesound.org/people/zgump/sounds/83249/
- The wav file "synth/371192__karolist__acoustic-kick-long.wav" is a derived 
version of https://freesound.org/people/karolist/sounds/371192/
