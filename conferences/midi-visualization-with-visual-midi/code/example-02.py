from pretty_midi import PrettyMIDI
from visual_midi import Plotter
from visual_midi import Preset

# Loading a file on disk using PrettyMidi
pm = PrettyMIDI("./example-01.mid")

# Plot the result using VisualMidi, modifying
# the presentation with Preset
preset = Preset(
    plot_width=1200,
    plot_height=500,
    show_beat=False,
    axis_label_text_font_size="14px",
    label_text_font_size="12px",
    toolbar_location=None,
)
plotter = Plotter(
    preset=preset,
    plot_max_length_bar=4,
)
plotter.show(pm, "/tmp/example-02.html")
