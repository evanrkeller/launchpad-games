
from rtmidi.midiutil import open_midiinput, open_midioutput
import rtmidi


class Launchpad:
    def __init__(self):
        self.midi_in, self.midi_out = self.setup_device()

    def find_launchpad(self):
        midi_in = rtmidi.MidiIn()
        midi_out = rtmidi.MidiOut()

        input_ports = [midi_in.get_port_name(i)
                       for i in range(midi_in.get_port_count())]
        output_ports = [midi_out.get_port_name(
            i) for i in range(midi_out.get_port_count())]

        launchpad_ports = [p for p in input_ports if "Launchpad" in p]

        if not launchpad_ports:
            return None, None

        launchpad_port = launchpad_ports[0]
        input_port_idx = input_ports.index(launchpad_port)
        output_port_idx = output_ports.index(launchpad_port)

        return input_port_idx, output_port_idx

    def setup_device(self):
        input_port_idx, output_port_idx = self.find_launchpad()

        if input_port_idx is None or output_port_idx is None:
            print("Error: No Launchpad device found.")
            sys.exit(1)

        midi_in, _ = open_midiinput(input_port_idx)
        midi_out, _ = open_midioutput(output_port_idx)

        return midi_in, midi_out

    def set_button_color(self, note, red, green, blue):
        self.midi_out.send_message(
            [240, 0, 32, 41, 2, 24, 11, note, red, green, blue, 247])

    def xy_to_note_number(self, x, y):
        if x == 0:
            return 103 + y
        else:
            return (9-x) * 10 + y

    def note_number_to_xy(self, note):
        if note >= 104:
            return 0, note - 103
        else:
            return 9 - (note // 10), note % 10

    def set_all_to_color(self, color):
        self.midi_out.send_message(
            [240, 0, 32, 41, 2, 24, 14, color, 247])

    def set_button_color_by_x_y(self, x, y, red, green, blue):
        note = self.xy_to_note_number(x, y)
        self.set_button_color(note, red, green, blue)

    def exit_programmer_mode(self):
        self.midi_out.send_message([240, 0, 32, 41, 2, 24, 15, 247])
        self.midi_in.close_port()
        self.midi_out.close_port()

    def get_message(self):
        return self.midi_in.get_message()
