from time import sleep
import RPi.GPIO as GPIO

BUTTON_1 = 5
BUTTON_2 = 6
LED_1 = 12
LED_2 = 13


def update_leds(gpio):
    button_1_pressed = gpio.input(BUTTON_1) == gpio.LOW
    button_2_pressed = gpio.input(BUTTON_2) == gpio.LOW

    gpio.output(LED_1, gpio.HIGH if button_1_pressed else gpio.LOW)
    gpio.output(LED_2, gpio.HIGH if button_2_pressed else gpio.LOW)


def run_on_pi():

    GPIO.setmode(GPIO.BCM)

    try:
        GPIO.setup(BUTTON_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(LED_1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(LED_2, GPIO.OUT, initial=GPIO.LOW)

        while True:
            update_leds(GPIO)
            sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

    from unittest.mock import Mock, call

    gpio = Mock(LOW=0, HIGH=1)

    test_cases = [
        ("Neither pressed", gpio.HIGH, gpio.HIGH, gpio.LOW, gpio.LOW),
        ("Button 1 pressed", gpio.LOW, gpio.HIGH, gpio.HIGH, gpio.LOW),
        ("Both pressed", gpio.LOW, gpio.LOW, gpio.HIGH, gpio.HIGH),
        ("Button 1 released", gpio.HIGH, gpio.LOW, gpio.LOW, gpio.HIGH),
        ("Both released", gpio.HIGH, gpio.HIGH, gpio.LOW, gpio.LOW),
    ]

    for label, button_1_level, button_2_level, led_1_level, led_2_level in test_cases:
        button_levels = {
            BUTTON_1: button_1_level,
            BUTTON_2: button_2_level,
        }
        gpio.input.side_effect = button_levels.__getitem__
        gpio.output.reset_mock()

        update_leds(gpio)

        expected = [call(LED_1, led_1_level), call(LED_2, led_2_level)]
        actual = gpio.output.call_args_list

        if actual != expected:
            raise AssertionError(f"{label}: expected {expected}, got {actual}")

        print(f"PASS: {label}")

def main():
    run_on_pi()


if __name__ == "__main__":
    main()