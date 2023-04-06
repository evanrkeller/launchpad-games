import sys
import time
import launchpad_py as launchpad


def main():
    lp = launchpad.LaunchpadMk2()

    if not lp.Open():
        print("Error: Launchpad Mk2 not found.")
        sys.exit(1)

    x = 2
    y = 1
    red = 63
    green = 63
    blue = 63

    lp.LedCtrlXY(x, y, red, green, blue)
    time.sleep(5)  # Keep the LED lit for 5 seconds

    lp.Reset()  # Turn off all LEDs
    lp.Close()  # Close the connection


if __name__ == "__main__":
    main()
