import sys
from launchpad_utils import Launchpad

lp = Launchpad()
lp.set_all_to_color(0)


def hsl_to_rgb(h, s, l):
    def hue_to_rgb(p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1/6:
            return p + (q - p) * 6 * t
        if t < 1/2:
            return q
        if t < 2/3:
            return p + (q - p) * (2/3 - t) * 6
        return p

    if s == 0:
        r, g, b = l, l, l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)

    return int(r * 63), int(g * 63), int(b * 63)


def create_spectrum():
    for x in range(1, 9):
        for y in range(0, 9):
            hue = (y-1) / 9
            saturation = 1
            lightness = (x ** (1.6)) / (9 ** (1.6))
            red, green, blue = hsl_to_rgb(hue, saturation, lightness)
            lp.set_button_color_by_x_y(x, y, red, green, blue)


def main():
    lp.set_all_to_color(0)

    try:
        create_spectrum()
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting...")
        # Exit Programmer mode
        lp.exit_programmer_mode()


if __name__ == "__main__":
    main()
