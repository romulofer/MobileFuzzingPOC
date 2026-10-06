# Mobile Fuzzing POC

A proof of concept that uses an RP2040 microcontroller (Raspberry Pi Pico or Pico Zero) as a USB
HID device to automate repeated login attempts against a form, for testing how a device or app
handles many fast, automated login attempts (lockout, throttling, rate limiting).

The board enumerates as a USB keyboard. When the physical button is pressed, it reads
username/password pairs from `wordlist.txt` and types each pair into whatever field currently has
focus, submitting between attempts.

## How it works

1. The board boots and waits (ready LED on).
2. Pressing the start button begins the run (running LED on, ready LED off).
3. For each line in `wordlist.txt`, the script types the username, tabs to the password field,
   types the password, and submits.
4. When the wordlist is exhausted, the board returns to the ready state.

Because it acts as a keyboard, it has no awareness of what is on screen. It assumes a specific
tab order and field layout, and simply plays back keystrokes on a timer. Test with
`testPage.html` first to confirm timing and tab order before pointing it at a real target.

## Hardware

- An RP2040 board running [Adafruit CircuitPython](https://circuitpython.org/) 8.x
  (`boot_out.txt` in this repo was generated on CircuitPython 8.2.7)
- A momentary push button (start button)
- Two LEDs (ready / running), each with a current-limiting resistor
- A USB cable to the target device

Two board variants are included, with different pin assignments:

| Signal | `code.py` (Pico) | `code(rp2040ZERO).py` (Pico Zero) |
|---|---|---|
| Start button | `GP9` (pulled up, active low) | `GP1` (pulled up, active low) |
| Ready LED | `GP7` | `GP6` |
| Running LED | `GP4` | `GP15` |

The Pico Zero variant also types a URL (`serverUrl`) before the credentials, for targets where
the login page needs to be opened first, and clears each field with backspace before typing into
it.

## Files

| File | Purpose |
|---|---|
| `code.py` | Main script for the Pico wiring. CircuitPython runs whatever is named `code.py` on boot. |
| `code(rp2040ZERO).py` | Variant for the Pico Zero wiring and an extra "open URL first" step. Rename to `code.py` on the board to use it. |
| `mobile_fuzzing_POC.py` | Earlier version of `code.py`, kept for reference (no 20 second startup delay). |
| `wordlist.txt` | `username,password` pairs, one per line. |
| `lib/adafruit_hid/` | The [Adafruit HID CircuitPython library](https://github.com/adafruit/Adafruit_CircuitPython_HID), compiled (`.mpy`), required for keyboard emulation. |
| `build.py` | Copies a given script to `output/code.py`, to prepare a file for deployment. |
| `testPage.html` | A minimal local login form for testing the board's timing and tab order safely, without a real target. |
| `boot_out.txt` | CircuitPython version/board info reported by the board this was developed on. |
| `settings.toml` | CircuitPython settings file (empty in this repo). |

## Setup

1. Flash the board with CircuitPython 8.x following the
   [CircuitPython installation guide](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython).
2. Wire the start button and the two LEDs to the pins listed above (button to ground through the
   pin, pulled up in software; each LED through a resistor to ground).
3. Copy `lib/adafruit_hid/` to the `lib/` folder on the `CIRCUITPY` drive.
4. Copy `wordlist.txt` to the root of `CIRCUITPY`, editing it first with the credentials you want
   to try, one `username,password` pair per line.
5. Copy the script for your board to the root of `CIRCUITPY` as `code.py`:
   - Pico: use `code.py` as is.
   - Pico Zero: copy `code(rp2040ZERO).py` and rename it to `code.py`, and set `serverUrl` to
     the page you want opened first (or remove that step if not needed).
6. Plug the board into the target device's USB port. After the startup delay, the ready LED
   turns on.

`build.py` can help prepare a file for step 5 from elsewhere in the project:

```sh
python build.py path/to/script.py   # copies it to ./output/code.py
```

### Testing safely

Before using the board against a real target, open `testPage.html` in a browser on a test
machine and run the board against it. It accepts only `your_username` / `your_password` and
alerts on anything else, so you can confirm the button, LEDs, timing, and tab order all work
before trying the board against anything else.

## Intended use and limits

This is a proof of concept for testing login throttling and lockout behavior on devices and
accounts you own or are explicitly authorized to test. Typing credentials via HID emulation is
indistinguishable, from the target's point of view, from a person typing them, which is the
point: it is a way to check whether a login screen resists many fast automated attempts. Only use
it against systems you own or have explicit written authorization to test, and check that doing
so does not violate the target's terms of service or local law.

The script has no target detection or error recovery: it assumes the field layout and timing
tested with `testPage.html` match the real target, and it will keep typing on that assumption. A
mismatch (wrong field focused, unexpected dialog) can type credentials in unintended places.

## License

No license file is currently included; all rights are reserved by the author unless a license is
added. Open an issue if you would like to use this under specific terms.
