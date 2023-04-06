import sys
import time
import rtmidi
from rtmidi.midiutil import open_midioutput


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
                status, x, y = msg

                if status == 144:  # Button down
                    print(f"Button ({x}, {y}) pressed")
                    # Set color to green when pressed
                    set_button_color(midi_out, x, y, 21)
                elif status == 128:  # Button up
                    print(f"Button ({x}, {y}) released")
                    # Set color to off when released
                    set_button_color(midi_out, x, y, 0)


def set_all_to_color(midi_out, color):
    midi_out.send_message(
        [240, 0, 32, 41, 2, 24, 14, color, 247])


def set_button_color(midi_out, note, red, green, blue):
    midi_out.send_message(
        [240, 0, 32, 41, 2, 24, 11, note, red, green, blue, 247])


def set_button_color_by_x_y(midi_out, x, y, red, green, blue):
    note = (y - 1) * 16 + x
    set_button_color(midi_out, note, red, green, blue)


def create_color_chart(midi_out):
    for y in range(1, 5):
        for x in range(1, 9):
            red_intensity = (x - 1) * 8
            green_intensity = (x - 1) * 8
            blue_intensity = (x - 1) * 8

            # Top-left quadrant: varying red intensities
            set_button_color_by_x_y(midi_out, x, y, red_intensity, 0, 0)

            # Top-right quadrant: varying green intensities
            set_button_color_by_x_y(midi_out, x + 4, y, 0, green_intensity, 0)

            # Bottom-left quadrant: varying blue intensities
            set_button_color_by_x_y(midi_out, x, y + 4, 0, 0, blue_intensity)

            # Bottom-right quadrant: varying red, green, and blue intensities
            set_button_color_by_x_y(midi_out, x + 4, y + 4, red_intensity,
                                    green_intensity, blue_intensity)


def xy_to_note_number(x, y):
    if x == 0:
        return 103 + y
    else:
        return (9-x) * 10 + y


def main():
    midi_in, midi_out = setup_device()
    set_all_to_color(midi_out, 0)

    # set top left button to red
    set_button_color(midi_out, xy_to_note_number(1, 1), 63, 0, 0)

    # set top right button to green
    set_button_color(midi_out, xy_to_note_number(1, 8), 0, 63, 0)

    # set bottom left button to blue
    set_button_color(midi_out, xy_to_note_number(8, 1), 0, 0, 63)

    # set bottom right button to white
    set_button_color(midi_out, xy_to_note_number(8, 8), 63, 63, 63)

    # set the top left special button to yellow
    set_button_color(midi_out, xy_to_note_number(0, 1), 63, 63, 0)

    # set the top right special button to purple
    set_button_color(midi_out, xy_to_note_number(0, 8), 63, 0, 63)

    # set the right top special button to cyan
    set_button_color(midi_out, xy_to_note_number(1, 9), 0, 63, 63)

    # set the right bottom special button to orange
    set_button_color(midi_out, xy_to_note_number(8, 9), 63, 31, 0)

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
