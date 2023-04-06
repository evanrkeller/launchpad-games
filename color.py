import sys
import time
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

    midi_out, _ = open_midioutput(output_port_idx)

    return midi_out


def set_button_color(midi_out, x, y, red, green, blue):
    note = ((9 - y) * 10) + x
    midi_out.send_message(
        [240, 0, 32, 41, 2, 24, 11, note, red, green, blue, 247])


def main():
    midi_out = setup_device()

    x = 2
    y = 1
    red = 63
    green = 63
    blue = 63

    set_button_color(midi_out, x, y, red, green, blue)
    time.sleep(5)  # Keep the LED lit for 5 seconds


if __name__ == "__main__":
    main()
