"""
TASK 3 - MUSICAL TONES, FREQUENCIES & RHYTHM
University of Galway - Winter Bells Lab

Instructions:
1. Read each line comment to understand how NumPy builds bell sound waves.
2. Open the Music Guide tab on the website to test frequencies and rhythms.
3. Complete TODO 1, TODO 2, and TODO 3 to compose your own bell variation.
"""

import numpy as np               # NumPy generates thousands of audio wave samples in fast arrays
import pygame                    # Pygame sends those audio arrays to the Raspberry Pi speakers
import time                      # Built-in time module pauses between notes to hold each beat

# SOUND THEORY -- this task makes sound only; it does not use the Sense HAT.
# A speaker produces sound by moving back and forth. The computer represents
# that movement as a stream of audio samples, then the sound card sends those
# samples to the speaker.
# 1. SAMPLE_RATE says how many samples are made each second (44,100 here).
# 2. A sine wave at frequency f completes f cycles each second: higher f means
#    a higher-pitched note. For example, A4 at 440 Hz completes 440 cycles per
#    second. t is the time of each sample in that wave.
# 3. A real bell is not a steady beep, so we add a quieter octave overtone
#    (2*f) and let both waves fade naturally. Short edge fades prevent clicks.
# 4. Music is described in beats. At TEMPO_BPM beats per minute, one beat lasts
#    60 / TEMPO_BPM seconds. A note's beat count sets its duration; a REST
#    keeps that duration but has frequency zero, so it is silent.
# 5. Finally, floating-point wave values are scaled to signed 16-bit PCM, the
#    sample format configured for Pygame's audio mixer.

SAMPLE_RATE = 44100              # Audio snapshots (samples) per second
VOLUME = 0.35                    # Master loudness from 0.1 (quiet) to 0.7 (loud)

# TODO 1: Experiment with TEMPO_BPM (try 100 for gentle bells, 132 for lively chimes)
TEMPO_BPM = 116                  # Speed in Beats Per Minute
BEAT_SEC = 60.0 / TEMPO_BPM      # Duration of 1 quarter-note beat in seconds (e.g. 60 / 116 = 0.517s)

# HOW PYTHON PARAMETERS SHAPE SOUND:
# Frequency (Hz) controls pitch. Doubling frequency raises a note by one
# octave: C4 = 261.63 Hz and C5 = 523.25 Hz.
# Duration (beats) controls rhythm. Mix eighth notes (0.5), dotted figures
# (0.75 + 0.25), and half notes (2.0) to vary the musical phrase.
# Tempo (TEMPO_BPM) scales all durations through BEAT_SEC = 60.0 / TEMPO_BPM.

# Map the note names used in the melody to their frequencies in Hertz.
NOTES = {
    "C4": 261.63,                # Middle C
    "D4": 293.66,
    "E4": 329.63,
    "F4": 349.23,
    "G4": 392.00,
    "A4": 440.00,                # Concert A tuning reference (440 vibrations/sec)
    "B4": 493.88,
    "C5": 523.25,                # High C (one octave above C4)
    "D5": 587.33,
    "E5": 659.25,
    "G5": 783.99,
    "REST": 0.0,                 # 0.0 Hz represents silence / a musical rest
}

# Configure Pygame to send mono, signed 16-bit PCM to the audio output. The
# mixer's 44,100 Hz setting matches SAMPLE_RATE so sample playback has the
# intended pitch and duration.
pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=1024)


def generate_bell_tone(frequency, duration_sec):
    """Build one note as 16-bit PCM samples from its frequency and duration."""
    # Sample count = samples per second * seconds (44,100 * 0.5 = 22,050).
    # At a higher frequency the same duration contains more wave cycles, not
    # more samples; sample count is controlled by time and SAMPLE_RATE.
    num_samples = max(1, int(SAMPLE_RATE * duration_sec))
    # A REST has no oscillation, so return silence for the full note duration.
    if frequency <= 0.0:
        return np.zeros(num_samples, dtype=np.int16)

    # Give every sample an evenly spaced time. endpoint=False avoids adding a
    # sample at duration_sec, which would extend the note by one sample.
    t = np.linspace(0, duration_sec, num_samples, endpoint=False)
    # A bell has a strong fundamental plus brighter partials. This simple
    # approximation mixes a 70% fundamental at frequency with a 30% octave
    # overtone at 2*frequency. The exponential envelopes make both fade away,
    # with the overtone decaying faster. 2*pi*f*t converts cycles into radians.
    wave = (
        0.70 * np.sin(2.0 * np.pi * frequency * t) * np.exp(-2.8 * t)
        + 0.30 * np.sin(2.0 * np.pi * (frequency * 2.0) * t) * np.exp(-5.0 * t)
    )

    # Fade the first and last 15 ms toward zero. Smooth edges avoid sudden
    # amplitude jumps, which are heard as clicks in a speaker.
    fade = min(int(SAMPLE_RATE * 0.015), num_samples // 4)
    if fade > 0:
        wave[:fade] *= np.linspace(0.0, 1.0, fade)   # Fade-in ramp: 0.0 -> 1.0
        wave[-fade:] *= np.linspace(1.0, 0.0, fade)  # Fade-out ramp: 1.0 -> 0.0

    # Apply the master volume and map -1..1 to the mixer's signed 16-bit range.
    return np.clip(wave * VOLUME * 32767, -32768, 32767).astype(np.int16)


def play_melody(melody):
    """Play (note_name, beats) pairs, holding each for its musical beat length."""
    for note_name, beats in melody:
        # Convert beat count into seconds; e.g. two beats last twice as long
        # as one beat, whatever the current tempo.
        dur_sec = beats * BEAT_SEC
        freq = NOTES.get(note_name, 0.0)        # Look up pitch in cycles/second
        if freq > 0.0:                          # A zero-frequency REST stays silent
            # Play 92% of the beat then leave a short gap so repeated chimes
            # remain distinct. The following sleep keeps the beat timing.
            pcm_samples = generate_bell_tone(freq, dur_sec * 0.92)
            # Convert the NumPy sample array into a Pygame sound and play it.
            sound = pygame.sndarray.make_sound(pcm_samples)
            sound.play()                        # Playback starts without blocking
        time.sleep(dur_sec)                     # Wait through the whole note/rest


# A melody is a list of (note_name, beat_count) pairs. The note names are
# looked up in NOTES; beat counts are converted to seconds using BEAT_SEC.
# Try an eighth note (0.5), a dotted figure (0.75 + 0.25), or a half note (2.0).
MELODY_BANK = {
    "Winter Bells": [
        ("E5", 0.5), ("D5", 0.5), ("C5", 0.5), ("G4", 0.5),
        ("A4", 0.5), ("B4", 0.5), ("C5", 1.0),
        ("E5", 0.5), ("D5", 0.5), ("C5", 0.5), ("G4", 0.5),
        ("G5", 0.75), ("E5", 0.25), ("C5", 1.5),
        # TODO 3: Add at least 4 more pairs before this list's closing bracket.
        # Example: ("G4", 0.5), ("A4", 0.5), ("C5", 1.0), ("REST", 0.5)
    ],
    "Galway Winter Chime": [
        ("G4", 0.5), ("C5", 0.5), ("E5", 1.0), ("D5", 0.5),
        ("C5", 0.5), ("A4", 1.0), ("G4", 1.5), ("REST", 0.5),
    ],
    "Snowfall": [
        ("C5", 0.5), ("D5", 0.5), ("E5", 0.75), ("REST", 0.25),
        ("G5", 0.5), ("E5", 0.5), ("C5", 1.0), ("REST", 0.5),
        ("G4", 0.5), ("C5", 1.0),
    ],
    "Bell Echo": [
        ("E5", 1.0), ("REST", 0.5), ("E5", 0.5), ("C5", 1.0),
        ("REST", 0.5), ("D5", 0.5), ("G4", 2.0),
    ],
}

# TODO 2: Choose one exact name from MELODY_BANK, then edit its note pairs.
selected_melody_name = "Winter Bells"
my_winter_melody = MELODY_BANK[selected_melody_name]

try:
    print(f"Playing {selected_melody_name} at {TEMPO_BPM} BPM...")
    play_melody(my_winter_melody)               # Play your composition from start to finish
    print("Task 3 complete!")
finally:
    pygame.mixer.quit()                         # Always close the audio mixer cleanly on exit
