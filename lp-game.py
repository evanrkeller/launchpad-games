import asyncio
import nest_asyncio
import random
import time
from launchpad_utils import Launchpad

lp = Launchpad()
lp.set_all_to_color(0)
score = 0


async def fade_button_color(note, red, green, blue):
    for i in range(0, 17):
        lp.set_button_color(note, 0, 64-(i*4), 0)
        await asyncio.sleep(0.01)


async def check_button_pressed(note, x, y):
    global score
    start_time = time.time()
    pressed = False

    while time.time() - start_time < 5:
        event = lp.get_message()
        if event:
            msg, _ = event
            if len(msg) == 3:
                status, event_note, velocity = msg

                if status == 144 and velocity > 0 and event_note == note:
                    pressed = True
                    break
        await asyncio.sleep(0.01)

    if pressed:
        score += 10
        lp.set_button_color(note, 0, 63, 0)
        await asyncio.sleep(0.5)
    else:
        score -= 10
        lp.set_button_color(note, 63, 0, 0)
        await asyncio.sleep(0.5)

    lp.set_button_color(note, 0, 0, 0)
    print(f"Current score: {score}")


async def light_up_random_button():
    x = random.randint(1, 8)
    y = random.randint(1, 8)
    note = lp.xy_to_note_number(x, y)
    lp.set_button_color(note, 0, 0, 63)
    asyncio.create_task(check_button_pressed(note, x, y))


async def light_up_random_button_periodically():
    while True:
        asyncio.create_task(light_up_random_button())
        await asyncio.sleep(1)


async def main():

    lp.set_all_to_color(0)

    try:
        nest_asyncio.apply()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(light_up_random_button_periodically())
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting...")
        # Exit Programmer mode
        lp.exit_programmer_mode()

if __name__ == "__main__":
    asyncio.run(main())
