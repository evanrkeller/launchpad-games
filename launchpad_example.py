import sys
import time
import rtmidi
from rtmidi.midiutil import open_midiinput, open_midioutput


def find_launchpad():
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


def setup_device():
    input_port_idx, output_port_idx = find_launchpad()

    if input_port_idx is None or output_port_idx is None:
        print("Error: No Launchpad device found.")
        sys.exit(1)

    midi_in, _ = open_midiinput(input_port_idx)
    midi_out, _ = open_midioutput(output_port_idx)

    return midi_in, midi_out


def handle_button_event(midi_in, midi_out):
    while True:
        event = midi_in.get_message()
        if event:
            msg, _ = event
            if len(msg) == 3:
                status, note, velocity = msg

                x = note % 10
                y = 9 - (note // 10)

                if status == 144:  # Button down
                    print(f"Button ({x}, {y}) pressed")
                    # Set color to green when pressed
                    set_button_color(midi_out, x, y, 0, 63, 0)
                elif status == 128:  # Button up
                    print(f"Button ({x}, {y}) released")
                    # Set color to off when released
                    set_button_color(midi_out, x, y, 0, 0, 0)


def set_button_color(midi_out, x, y, red, green, blue):
    if y == 9:  # Top row buttons
        note = x
    else:
        note = 10 * (9 - y) + x

    midi_out.send_message(
        [240, 0, 32, 41, 2, 24, 11, note, red, green, blue, 247])


def main():
    midi_in, midi_out = setup_device()
    print("Launchpad Mk2 ready, press buttons or press Ctrl+C to exit...")

    # Enter Programmer mode
    midi_out.send_message([240, 0, 32, 41, 2, 24, 14, 247])

    try:
        handle_button_event(midi_in, midi_out)
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting...")
        # Exit Programmer mode
        midi_out.send_message([240, 0, 32, 41, 2, 24, 15, 247])
        midi_in.close_port()
        midi_out.close_port()


if __name__ == "__main__":
    main()
