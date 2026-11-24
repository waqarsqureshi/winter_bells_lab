"""
TASK 4 - COMBINE DISPLAY & AUDIO: THE WINTER BELLS SYMPHONY
University of Galway - Winter Bells Lab (Final Capstone)

Instructions:
1. Audio plays on a background thread while the main thread updates
   Sense HAT LED scenes in sync with a shared time.monotonic() clock.
2. Complete TODO 1, TODO 2, and TODO 3 to personalise your Symphony.
3. Short on time? Copy solutions/task4_winter_bells_symphony_solution.py.

The earlier tasks kept the hardware display and music separate. Here, each
note has a beat duration and each group of notes belongs to a named LED scene.
The same elapsed-time clock advances both timelines so the lights follow the
music; comments below explain how samples and beats form the audio.
"""

import math                      # Provides pi for sine wave calculations
import threading                 # Runs audio monitoring concurrently with LED animations
import time                      # Provides monotonic clock and short loop sleeps
import numpy as np               # Synthesises the entire song waveform into memory
import pygame                    # Plays the synthesised composition waveform
from sense_hat import SenseHat   # Controls the 8x8 RGB LED matrix

SAMPLE_RATE = 44100              # 44,100 audio samples are played each second
TEMPO_BPM = 116                  # Musical tempo in beats per minute
BEAT_SEC = 60.0 / TEMPO_BPM      # Convert tempo to the duration of one beat
VOLUME = 0.38                    # Output volume (0.1 to 0.7)

# Define RGB colour palette (values 0 to 255)
K = [0, 0, 0]                    # Off
Y = [255, 205, 20]               # Bell gold
M = [180, 125, 15]               # Warm bronze
W = [245, 248, 255]              # Snow white
B = [95, 195, 255]               # Ice blue
C = [30, 120, 220]               # Deep winter blue
U = [127, 0, 61]                 # University of Galway maroon

# A musical note's frequency (Hertz) is its sine-wave cycles per second;
# a larger frequency sounds higher. A REST has frequency zero and is silent.
NOTES = {
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23,
    "G4": 392.00, "A4": 440.00, "B4": 493.88,
    "C5": 523.25, "D5": 587.33, "E5": 659.25, "G5": 783.99, "REST": 0.0,
}

# TODO 1: Customise or extend the melody sections.
# Each tuple is (scene_name, [(note_name, beat_count), ...]). Beat counts
# determine note lengths through BEAT_SEC; the section name selects its LEDs.
SECTIONS = [
    ("winter_bell", [("E5", 0.5), ("D5", 0.5), ("C5", 0.5), ("G4", 0.5), ("A4", 0.5), ("B4", 0.5), ("C5", 1.0)]),
    ("snow", [("C5", 0.5), ("B4", 0.5), ("A4", 0.5), ("G4", 0.5), ("F4", 0.5), ("E4", 0.5), ("D4", 0.5), ("C4", 1.0)]),
    ("lights", [("G5", 0.5), ("E5", 0.5), ("C5", 0.5), ("G4", 0.5), ("C5", 0.5), ("E5", 0.5), ("G5", 1.5)]),
]


def build_music():
    """Build the PCM audio and record the time window for each LED scene."""
    chunks = []                  # List of NumPy waveform arrays (one chunk per note)
    timeline = []                # Stores (scene_name, start_sec, end_sec) to sync LEDs with audio
    cursor = 0.0                 # Cumulative timestamp in seconds from the start of the song

    for name, notes in SECTIONS:
        start = cursor           # Mark when this scene begins in the finished song
        for note, beats in notes:
            # Turn musical beats into real time. At 116 BPM, one beat is just
            # over half a second; a note lasting two beats takes twice as long.
            dur = beats * BEAT_SEC
            # Make samples for 94% of the beat, leaving a short gap before the next note.
            n = max(1, int(SAMPLE_RATE * dur * 0.94))
            freq = NOTES.get(note, 0.0)                 # Frequency in Hz (0.0 for REST)
            if freq > 0:
                # Each timestamp is a sample time. The sine wave repeats at
                # 'freq' cycles/second; 2*freq adds a brighter octave overtone.
                t = np.linspace(0, dur * 0.94, n, endpoint=False)
                # Blend fundamental (f) + octave overtone (2*f) with exponential bell decay
                w = (
                    0.70 * np.sin(2.0 * math.pi * freq * t) * np.exp(-2.8 * t)
                    + 0.30 * np.sin(2.0 * math.pi * (freq * 2.0) * t) * np.exp(-5.0 * t)
                ) * VOLUME
            else:
                w = np.zeros(n, dtype=np.float32)       # Array of zeros = silence during REST
            # Pad the final 6% with silence so the note still occupies its full beat.
            pad = np.zeros(max(0, int(SAMPLE_RATE * dur) - n), dtype=np.float32)
            chunks.append(np.concatenate([w, pad]))     # Combine sounded part + silent gap
            cursor += dur                               # Advance by sound plus its silent tail
        # The LED loop uses these time bounds to select the matching scene.
        timeline.append((name, start, cursor))

    # Join samples in musical order and convert the wave to signed 16-bit PCM
    # for the Pygame mixer.
    pcm = np.clip(np.concatenate(chunks) * 32767, -32768, 32767).astype(np.int16)
    return pygame.sndarray.make_sound(pcm), timeline, cursor


def show_winter_bell_scene(sense, beat):
    """Scene 1: Draw an 8x8 Winter Bell whose golden clapper swings left and right on each beat."""
    swing_left = (beat % 2) == 0
    cl_left = Y if swing_left else K                    # Clapper left position
    cl_right = K if swing_left else Y                   # Clapper right position
    sparkle_l = W if swing_left else K                  # Top-left frost sparkle
    sparkle_r = K if swing_left else W                  # Top-right frost sparkle
    # Push an explicit 8x8 list of 64 [R, G, B] values (Row 0 top .. Row 7 bottom)
    sense.set_pixels([
        sparkle_l, K, K, Y, Y, K, K, sparkle_r,         # Row 0: swinging frost sparkle & bell ring
        K, K, B, W, B, B, K, K,                         # Row 1: frosted bell crown
        K, K, B, W, B, C, K, K,                         # Row 2: upper bell body
        K, B, W, B, B, C, B, K,                         # Row 3: flaring bell sides
        K, B, W, B, C, C, B, K,                         # Row 4: lower bell curve
        W, B, B, W, B, C, C, W,                         # Row 5: frosted bell rim
        K, K, cl_left, Y, Y, cl_right, K, B,            # Row 6: swinging golden clapper
        K, K, K, K, K, K, K, K,                         # Row 7: bottom margin
    ])


def show_snow_scene(sense, beat):
    """Scene 2: TODO 2 - Generate 64 snow pixels mathematically using list index i (0..63)."""
    # Loop i from 0 to 63: use modulo (%) remainder math to place white (W) & ice-blue (B) flakes
    # Adding 'beat' shifts which LEDs light up on every beat, creating twinkling snowfall!
    pixels = [W if (i + beat) % 5 == 0 else (B if (i + beat) % 7 == 0 else K) for i in range(64)]
    sense.set_pixels(pixels)                            # Update all 64 LEDs in one frame


def show_lights_scene(sense, beat):
    """Scene 3: Pulse ice blue, snow white, bell gold, and Galway maroon across all 64 pixels."""
    colours = [B, W, Y, U]                              # Winter Bells palette to cycle through
    # Light every even pixel ((i + beat) % 2 == 0) with a rotating palette colour, others off (K)
    pixels = [colours[(i + beat) % len(colours)] if (i + beat) % 2 == 0 else K for i in range(64)]
    sense.set_pixels(pixels)                            # Render pattern onto the 8x8 LED matrix


def main():
    sense = SenseHat()                           # Initialise Sense HAT
    sense.low_light = True
    sense.clear()
    # Configure the sound card for the same sample rate and 16-bit mono format
    # used by build_music(); this keeps the generated frequencies at pitch.
    pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=1024)

    sound, timeline, total_dur = build_music()   # Build song & section timestamps
    stop_event = threading.Event()               # Shared flag to stop threads cleanly
    # A monotonic clock only moves forward, so elapsed scene times are not
    # affected by the computer's wall-clock time changing during playback.
    start_time = time.monotonic()                # Shared clock reference for music & LEDs

    def audio_worker():
        """Worker thread: starts audio and stops immediately if stop_event is triggered."""
        ch = sound.play()
        while not stop_event.is_set() and ch is not None and ch.get_busy():
            stop_event.wait(0.05)
        if ch is not None:
            ch.stop()

    # Audio playback can continue while the main thread refreshes the LEDs.
    thread = threading.Thread(target=audio_worker, daemon=True)
    last_step = -1                               # Tracks the most recent half-beat index

    try:
        thread.start()                           # Start playing music in background thread
        while not stop_event.is_set():
            elapsed = time.monotonic() - start_time
            if elapsed >= total_dur:             # End loop once composition finishes
                break
            # Refresh the picture every half-beat for a little movement
            # without updating the display on every pass through the loop.
            step = int(elapsed / (BEAT_SEC * 0.5))
            if step != last_step:                # Update Sense HAT once per half-beat
                last_step = step
                active = next((name for name, s, e in timeline if s <= elapsed < e), "lights")
                if active == "winter_bell":
                    show_winter_bell_scene(sense, step)
                elif active == "snow":
                    show_snow_scene(sense, step)
                else:
                    show_lights_scene(sense, step)
            time.sleep(0.02)                     # Small sleep keeps CPU usage low

        thread.join(timeout=1.0)                 # Wait for audio thread to finish
        # TODO 3: Customise your finale greeting text and colours!
        sense.show_message("WINTER BELLS!", scroll_speed=0.06, text_colour=Y, back_colour=U)
    except KeyboardInterrupt:
        print("\nStopped safely.")
    finally:
        stop_event.set()                         # Signal worker thread to halt
        pygame.mixer.stop()                      # Stop any active audio
        pygame.mixer.quit()                      # Close mixer
        sense.clear()                            # Turn off all 64 LEDs on exit


if __name__ == "__main__":
    main()
