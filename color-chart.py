import time
import rtmidi
from rtmidi.midiutil import open_midiinput, open_midioutput


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


def set_led_color(midi_out, x, y, red, green, blue):
    led_number = (y - 1) * 16 + x
    color_value = 16 * (red // 4) + (green // 4) * 4 + (blue // 4)
    sysex_message = [240, 0, 32, 41, 2, 24, 3, led_number, color_value, 247]
    midi_out.send_message(sysex_message)


def create_color_chart(midi_out):
    for y in range(1, 5):
        for x in range(1, 9):
            red_intensity = (x - 1) * 8
            green_intensity = (x - 1) * 8
            blue_intensity = (x - 1) * 8

            # Top-left quadrant: varying red intensities
            set_led_color(midi_out, x, y, red_intensity, 0, 0)

            # Top-right quadrant: varying green intensities
            set_led_color(midi_out, x + 4, y, 0, green_intensity, 0)

            # Bottom-left quadrant: varying blue intensities
            set_led_color(midi_out, x, y + 4, 0, 0, blue_intensity)

            # Bottom-right quadrant: varying red, green, and blue intensities
            set_led_color(midi_out, x + 4, y + 4, red_intensity,
                          green_intensity, blue_intensity)


midi_out = rtmidi.MidiOut()
launchpad_port = find_launchpad()

if launchpad_port is None:
    print("Error: Launchpad not found.")
    exit(1)

midi_out.open_port(launchpad_port)
create_color_chart(midi_out)

time.sleep(10)  # Display the color chart for 10 seconds

midi_out.close_port()
