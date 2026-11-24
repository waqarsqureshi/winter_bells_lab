"""
TASK 2 - SENSE HAT DISPLAY & PIXEL STUDIO ART
University of Galway - Winter Bells Lab

Instructions:
1. Complete TODO 1 to scroll a Winter Bells greeting with custom RGB colours.
2. Open Pixel Studio on the website OR run: python3 pixel_studio_gui.py
3. Load the Winter Bell or Bell template (or paint your own) and paste it into TODO 2.
4. Save and run this file locally on your Raspberry Pi.

This task explores the Sense HAT as a display. Task 1 only checked that the
hardware responds; here you will use scrolling text and a complete 8x8 image.
"""

from sense_hat import SenseHat   # Import the Sense HAT library to control the 8x8 LED matrix
import time                      # Import built-in time module to pause between images

# Create the connection to the HAT. Task 1 checked that this connection works;
# this task explores the HAT as an output device, with no audio playback.
sense = SenseHat()
# Dim the LEDs slightly so colour choices are easier to compare by eye.
sense.low_light = True
# Begin with every pixel off so the message and artwork are easy to see.
sense.clear()

# DISPLAY THEORY: every matrix pixel is made from red, green and blue LEDs.
# Each channel is an intensity from 0 (off) to 255 (brightest); mixing the
# channels creates colours, for example red + green makes yellow. A colour is
# written as [red, green, blue], the same order used by set_pixel and set_pixels.
GALWAY_MAROON = [127, 0, 61]     # Medium Red + slight Blue = University of Galway maroon
GOLD = [255, 205, 20]            # Full Red + high Green + tiny Blue = warm bell gold
ICE_BLUE = [95, 195, 255]        # Cool sky-blue light = winter ice blue
WINTER_BLUE = [30, 120, 220]     # Deep winter blue = bell shading
SNOW_WHITE = [245, 248, 255]     # High Red + Green + Blue = crisp snow white
OFF = [0, 0, 0]                  # All three lights off = dark pixel

# TODO 1: Customise the greeting message, text_colour, and back_colour below.
# show_message() turns letters into pixel patterns and scrolls the columns
# across the same 8x8 grid you will use for your own picture. scroll_speed is
# the delay between shifts in seconds, so a smaller number scrolls faster.
sense.show_message(
    "WINTER BELLS LAB!",         # Text string to scroll across the 8x8 matrix
    scroll_speed=0.07,           # Delay in seconds per column shift (smaller = faster scrolling)
    text_colour=GOLD,            # [R, G, B] colour for the lit letter pixels
    back_colour=GALWAY_MAROON,   # [R, G, B] colour for the background pixels behind the letters
)

# These short names make the 64 colour entries below easier to read as a
# picture. Each alias refers to a complete RGB triplet, not a single channel.
K = OFF                          # Background / off pixel
W = SNOW_WHITE                   # Snow highlight & frost sparkle
B = ICE_BLUE                     # Frosted ice-blue bell body
C = WINTER_BLUE                  # Deep winter-blue shadow
Y = GOLD                         # Golden bell ring & clapper

# TODO 2: Replace this starter list with your 64-pixel art from Pixel Studio!
# PIXEL-ART THEORY: set_pixels() receives one flat list in row-major order.
# - It must contain exactly 64 [R, G, B] entries: 8 rows x 8 columns.
# - Entries 0..7 draw the top row, left to right; entries 56..63 draw the
#   bottom row, left to right.
# - For column x and row y, the list index is (y * 8) + x. For example,
#   column 3 of row 2 is index (2 * 8) + 3 = 19.
my_winter_bell_art = [
    W, K, K, Y, Y, K, K, K,      # Row 0 (indices 0..7): frost sparkle & golden bell ring
    K, K, B, W, B, B, K, K,      # Row 1 (indices 8..15): frosted bell crown
    K, K, B, W, B, C, K, K,      # Row 2 (indices 16..23): upper bell body
    K, B, W, B, B, C, B, K,      # Row 3 (indices 24..31): flaring bell sides
    K, B, W, B, C, C, B, K,      # Row 4 (indices 32..39): lower bell curve
    W, B, B, W, B, C, C, W,      # Row 5 (indices 40..47): snow-frosted bell rim
    K, K, K, Y, Y, K, K, B,      # Row 6 (indices 48..55): golden clapper & ice sparkle
    K, K, K, K, K, K, K, K,      # Row 7 (indices 56..63): clean bottom margin
]

# Check the image dimensions before sending the frame. If the list is not
# exactly 64 pixels, the assertion gives a clearer error than the device API.
assert len(my_winter_bell_art) == 64, "Pixel art must have exactly 64 pixels!"
# Send one complete frame to the matrix; the order of the list determines
# which coordinate receives each colour.
sense.set_pixels(my_winter_bell_art)
# Leave the image on screen long enough to inspect it.
time.sleep(5)

# Always clear the Sense HAT LEDs back to [0, 0, 0] before exiting
sense.clear()
print("Task 2 display complete!")
