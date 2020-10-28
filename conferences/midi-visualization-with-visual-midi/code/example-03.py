from note_seq.protobuf import music_pb2

sequence = music_pb2.NoteSequence()

# Add the notes and configuration to the sequence.
sequence.notes.add(pitch=60, start_time=0.0, end_time=0.5, velocity=80)
sequence.notes.add(pitch=60, start_time=0.5, end_time=1.0, velocity=80)
...
sequence.notes.add(pitch=62, start_time=6.5, end_time=7.0, velocity=80)
sequence.notes.add(pitch=60, start_time=7.0, end_time=8.0, velocity=80)
sequence.total_time = 8
sequence.tempos.add(qpm=60)

print(sequence)
