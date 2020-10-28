from note_seq import midi_to_note_sequence
from note_seq.midi_io import note_sequence_to_pretty_midi
from note_seq.protobuf import music_pb2
from visual_midi import Plotter

sequence = music_pb2.NoteSequence()

# Add the notes and configuration to the sequence.
sequence.notes.add(pitch=60, start_time=0.0, end_time=0.5, velocity=80)
sequence.notes.add(pitch=60, start_time=0.5, end_time=1.0, velocity=80)
...
sequence.notes.add(pitch=62, start_time=6.5, end_time=7.0, velocity=80)
sequence.notes.add(pitch=60, start_time=7.0, end_time=8.0, velocity=80)
sequence.total_time = 8
sequence.tempos.add(qpm=60)

# Convert "note-seq" -> "pretty-midi"
pretty_midi = note_sequence_to_pretty_midi(sequence)
print(pretty_midi)

# Convert "pretty-midi" -> "note-seq"
sequence = midi_to_note_sequence(pretty_midi)
print(sequence)

# Convert "pretty-midi" -> "visual-midi"
plotter = Plotter()
plotter.show(pretty_midi, "/tmp/example-04.html")
