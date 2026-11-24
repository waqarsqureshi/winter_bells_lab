UNIVERSITY OF GALWAY
WINTER BELLS LAB
Raspberry Pi Sense HAT | Two-hour practical
======================================================================

Welcome to the Winter Bells lab. We will get to know the Raspberry Pi
Sense HAT by trying a few things it can do: show a simple light, display
our own pixel art, make a short piece of sound, and then bring the light
and music together. The aim is to explore the hardware and spark ideas
for Semester 2 and the hackathon; this is not a Python theory exercise.

The Sense HAT connects to the Pi's 40-pin GPIO header. Its 8x8 matrix
has 64 RGB LEDs, each of which can mix red, green and blue values from 0
to 255. A five-way joystick gives a project simple user input. The
temperature, humidity and pressure sensors, along with the accelerometer,
gyroscope and magnetometer, let projects respond to their environment or
movement. We'll focus on the display today, leaving the other sensors as
ideas to revisit later.

WHAT'S IN THE LAB PACK?
----------------------------------------------------------------------
README.txt
    These instructions and quick troubleshooting notes.
setup_pi.sh
    Checks for the software libraries and editors used in the lab.
task1_verify.py
    Checks the Sense HAT connection by lighting one LED.
task2_display_and_art.py
    Displays a scrolling message and your 8x8 pixel-art design.
pixel_studio_gui.py
    Standalone 8x8 Pixel Studio with seven starter templates.
task3_music_tones.py
    Creates a melody with NumPy and plays it through Pygame.
task4_winter_bells_symphony.py
    Combines the LED scenes and music in one timed performance.
solutions.zip
    Completed fallback versions of all four task scripts. Extract this
    only if you need help getting unstuck.

The printable handout and its LaTeX source are supplied with the lab
materials. Keep the image and University logo alongside the .tex file
when recompiling the PDF.

GETTING READY (10 MINUTES)
----------------------------------------------------------------------
On the Raspberry Pi, open a terminal and go to the extracted lab folder:

    cd ~/winter_bells_lab
    chmod +x setup_pi.sh
    ./setup_pi.sh

The setup script checks for sense_hat, pygame, numpy and tkinter, and
reports whether they are ready. Open the task files in Thonny or Geany.
If you use Geany, set its Execute command to:

    python3 "%f"

Read the comments in each script before running it. They explain what
the hardware or sound is doing and point out the places you can
personalise.

THE ACTIVITIES
----------------------------------------------------------------------

1. First contact with the Sense HAT
   File: task1_verify.py

   This first program is deliberately small. It connects to the Sense
   HAT, lights one gold LED near the centre of the matrix for two seconds,
   and clears the display. The comments introduce the board connection,
   RGB colour values and the x/y coordinates of a single pixel. There is
   no scrolling message, pixel-art activity or sound in this task.

2. Make something for the display
   Files: task2_display_and_art.py and pixel_studio_gui.py

   Now use the matrix as a tiny screen. Choose your own scrolling greeting
   and its foreground/background colours, then open Pixel Studio either
   on the lab website or locally:

       python3 pixel_studio_gui.py

   Try one of the seven templates (Winter Bell, Bell, Snowflake, Winter
   Star, Snowman, Winter Pine or Winter Frost Pattern), or draw a design
   of your own. Copy the generated 64-pixel RGB list into TODO 2 in
   task2_display_and_art.py and run it on the Pi. The comments explain
   why pixels are listed row by row and how to find a pixel's list index.

3. Make a chime
   File: task3_music_tones.py

   This task is about sound only; it does not use the Sense HAT. A digital
   sound is stored as a sequence of samples. Here NumPy samples a sine
   wave 44,100 times per second. Its frequency, measured in Hertz, is the
   number of cycles per second and determines the note's pitch. The script
   adds a quieter octave overtone and a decaying envelope to make a bell
   sound less like a steady beep, then sends the 16-bit audio samples to
   the speaker through Pygame.

   Listen to the default melody, then try changing TEMPO_BPM, pitches and
   beat counts. At a tempo of B beats per minute, one beat lasts 60/B
   seconds; a note lasting two beats therefore lasts twice as long as a
   one-beat note. A REST has zero frequency but still occupies its beats.
   Choose a ready-made tune in selected_melody_name: Winter Bells,
   Galway Winter Chime, Snowfall or Bell Echo. Add note-and-beat pairs to
   the Winter Bells list, or edit another tune. The Music Guide also has
   presets. Quick reference:

       A4 = 440.00 Hz       C5 = 523.25 Hz       G5 = 783.99 Hz
       0.5 beat = eighth    1 beat = quarter     2 beats = half note
       REST = silence

4. Bring the lights and sound together
   File: task4_winter_bells_symphony.py

   For the final activity, make the melody sections your own, add to the
   snow scene or reuse your pixel art, and write a closing message. The
   program builds the audio from note frequencies and beat lengths while
   changing Sense HAT scenes against the same elapsed-time clock. Listen
   and watch: can your group make each scene feel distinct enough for
   another group to guess what is happening?

SPACE PROJECT IDEAS
----------------------------------------------------------------------
The handout references Astro Pi Mission Space Lab for examples of
student experiments on the ISS, and a Raspberry Pi Foundation article
with 3D-printable Astro Pi flight-case parts. The printed case is a
project model, not equipment certified for spaceflight.

BEFORE YOU LEAVE
----------------------------------------------------------------------
Stop a running task with Ctrl+C or Thonny's Stop button. The combined
show clears the Sense HAT when it exits. If LEDs remain on, run
sense.clear(). If there is no sound, check the Raspberry Pi desktop's
audio menu and select HDMI or your headphones/speakers. If Pixel Studio
reports an invalid image, check that it contains exactly 64 pixels:
eight rows of eight.

If you need a fallback, extract solutions.zip in this folder and run the
corresponding script from solutions/. Try the task first, then compare
your version with the completed example.
