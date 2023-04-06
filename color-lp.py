import sys
import time
import launchpad_py as launchpad


def lightup(lp, x, y, red, green, blue):  # light up a single LED
    lp.LedCtrlXY(x, y, red, green, blue)


def main():
    lp = launchpad.LaunchpadMk2()

    if not lp.Open():
        print("Error: Launchpad Mk2 not found.")
        sys.exit(1)

    for x in range(9):
        for y in range(9):
            lightup(lp, x, y, 63, 63, 63)
            time.sleep(1)  # Keep the LED lit for 5 seconds

    lp.Reset()  # Turn off all LEDs
    lp.Close()  # Close the connection


if __name__ == "__main__":
    main()
