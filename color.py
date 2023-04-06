import rtmidi
from rtmidi.midiutil import open_midioutput


def find_launchpad():
    midi_out = rtmidi.MidiOut()
    output_ports = [midi_out.get_port_name(
        i) for i in range(midi_out.get_port_count())]
    launchpad_ports = [p for p in output_ports if "Launchpad" in p]

    if not launchpad_ports:
        return None

    launchpad_port = launchpad_ports[0]
    output_port_idx = output_ports.index(launchpad_port)

    return output_port_idx


def setup_device():
    output_port_idx = find_launchpad()

    if output_port_idx is None:
        print("Error: No Launchpad device found.")
        sys.exit(1)

    _, midi_out = open_midioutput(output_port_idx)

    return midi_out


def set_button_color(midi_out, x, y, red, green):
    if y == 9:  # Top row buttons
        note = x
    else:
        note = 10 * (9 - y) + x

    color = (green << 4) | red
    midi_out.send_message([144, note, color])


def main():
    midi_out = setup_device()

    x = 2
    y = 1
    red = 3
    green = 3

    set_button_color(midi_out, x, y, red, green)


if __name__ == "__main__":
    main()
