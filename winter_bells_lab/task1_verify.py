"""
TASK 1 - FIRST CONTACT WITH THE RASPBERRY PI SENSE HAT
University of Galway - Winter Bells Lab

This short check confirms that the Sense HAT is connected and that the Pi
can control one of its LEDs. Display artwork and sound come in later tasks.
"""

from sense_hat import SenseHat
import time

# SenseHat() creates the Python handle for the board on the Pi's 40-pin GPIO
# header. The same object provides the LED display, sensors and joystick; this
# first check uses only one LED so we can confirm the hardware connection.
sense = SenseHat()

# The matrix is bright at full power; low_light makes a close-up classroom
# demo more comfortable to view. clear() starts from a known, dark screen.
sense.low_light = True
sense.clear()

# The matrix has 8 columns (x) and 8 rows (y), numbered 0 through 7 from the
# top-left corner. set_pixel(x, y, colour) lights just that coordinate. The
# colour is an [R, G, B] list; each channel ranges from 0 (off) to 255 (bright).
# This single gold pixel checks the HAT without introducing scrolling text,
# pixel art or audio; those are explored in their own tasks.
sense.set_pixel(3, 3, [255, 205, 20])
print("If you can see one gold LED, the Sense HAT is responding.")

# Keep the LED visible long enough to inspect it before clearing the matrix.
time.sleep(2)

# Leave the matrix dark and ready for Task 2.
sense.clear()
print("Task 1 complete! Next: messages and pixel art.")
