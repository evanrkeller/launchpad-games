import sys
import time
import rtmidi
import threading
from rtmidi.midiutil import open_midiinput, open_midioutput
import random

score = 0


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

                [x, y] = note_number_to_xy(note)

                if status == 144 and velocity > 0:  # Button down
                    # Set color to green when pressed
                    set_button_color(midi_out, note, 0, 63, 0)
                elif status == 144 and velocity == 0:  # Button up
                    # Set color to off when released
                    fade_thread = threading.Thread(
                        target=fade_button_color, args=(midi_out, note, 0, 63, 0))
                    fade_thread.start()


def fade_button_color(midi_out, note, red, green, blue):
    for i in range(0, 17):
        set_button_color(midi_out, note, 0, 64-(i*4), 0)
        time.sleep(0.005)


def set_all_to_color(midi_out, color):
    midi_out.send_message(
        [240, 0, 32, 41, 2, 24, 14, color, 247])


def set_button_color(midi_out, note, red, green, blue):
    midi_out.send_message(
        [240, 0, 32, 41, 2, 24, 11, note, red, green, blue, 247])


def set_button_color_by_x_y(midi_out, x, y, red, green, blue):
    note = (y - 1) * 16 + x
    set_button_color(midi_out, note, red, green, blue)


def xy_to_note_number(x, y):
    if x == 0:
        return 103 + y
    else:
        return (9-x) * 10 + y


def note_number_to_xy(note):
    if note >= 104:
        return 0, note - 103
    else:
        return 9 - (note // 10), note % 10


def check_button_pressed(midi_out, midi_in, note, x, y):
    global score
    start_time = time.time()
    pressed = False

    while time.time() - start_time < 5:
        event = midi_in.get_message()
        if event:
            msg, _ = event
            if len(msg) == 3:
                status, event_note, velocity = msg
                [event_x, event_y] = note_number_to_xy(event_note)

                if status == 144 and velocity > 0 and event_note == note:
                    pressed = True
                    break

    if pressed:
        score += 10
        set_button_color(midi_out, note, 0, 63, 0)
        time.sleep(0.5)
    else:
        score -= 10
        set_button_color(midi_out, note, 63, 0, 0)
        time.sleep(0.5)

    set_button_color(midi_out, note, 0, 0, 0)
    print(f"Current score: {score}")


def light_up_random_button(midi_out):
    x = random.randint(1, 8)
    y = random.randint(1, 8)
    note = xy_to_note_number(x, y)
    set_button_color(midi_out, note, 0, 0, 63)
    check_button_thread = threading.Thread(
        target=check_button_pressed, args=(midi_out, midi_in, note, x, y))
    check_button_thread.start()


def light_up_random_button_periodically(midi_out):
    while True:
        light_up_random_button(midi_out)
        time.sleep(1)


def main():
    global midi_in, midi_out
    midi_in, midi_out = setup_device()
    set_all_to_color(midi_out, 0)

    random_button_thread = threading.Thread(
        target=light_up_random_button_periodically(midi_out))
    random_button_thread.daemon = True
    random_button_thread.start()

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
