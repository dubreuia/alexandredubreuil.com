from pretty_midi import PrettyMIDI
from visual_midi import Plotter

# Loading a file on disk using PrettyMidi,
# and show some information
pm = PrettyMIDI("./example-01.mid")
print(pm.instruments)
print(pm.instruments[0].notes)
print(pm.instruments[0].notes[0])
print(pm.get_tempo_changes())

# Plot the result using VisualMidi
plotter = Plotter()
plotter.show(pm, "/tmp/example-01.html")