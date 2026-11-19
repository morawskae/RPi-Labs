import argparse
from time import sleep

from gpiozero import Button, Device, LED
from gpiozero.pins.mock import MockFactory


def update_leds(button_1, button_2, led_1, led_2):
    led_1.value = button_1.is_pressed
    led_2.value = button_2.is_pressed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true")
    args = parser.parse_args()

    if args.mock:
        Device.pin_factory = MockFactory()

    with (
        Button(5, pull_up=True) as button_1,
        Button(6, pull_up=True) as button_2,
        LED(12) as led_1,
        LED(13) as led_2,
    ):
        if args.mock:
            test_cases = [
                ("Neither pressed", False, False),
                ("Button 1 pressed", True, False),
                ("Both pressed", True, True),
                ("Button 1 released", False, True),
                ("Both released", False, False),
            ]

            for label, pressed_1, pressed_2 in test_cases:
                for button, pressed in (
                    (button_1, pressed_1),
                    (button_2, pressed_2),
                ):
                    if pressed:
                        button.pin.drive_low()
                    else:
                        button.pin.drive_high()

                update_leds(button_1, button_2, led_1, led_2)
                actual = (led_1.is_lit, led_2.is_lit)
                expected = (pressed_1, pressed_2)

                if actual != expected:
                    raise AssertionError(
                        f"{label}: expected {expected}, got {actual}"
                    )

                print(f"PASS {label} -> LEDs {actual}")
        else:
            try:
                while True:
                    update_leds(button_1, button_2, led_1, led_2)
                    sleep(0.01)
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    main()