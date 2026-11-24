"""
STANDALONE PIXEL STUDIO (Python Tkinter GUI)
University of Galway - Winter Bells Lab (Task 2 Tool)

Run locally on your Raspberry Pi:
    python3 pixel_studio_gui.py
"""

import tkinter as tk                        # Built-in Python GUI library for windows and buttons
from tkinter import colorchooser, messagebox  # Dialogs for custom RGB picker and info popups

# Try importing Sense HAT so students can preview directly on physical LEDs if connected
try:
    from sense_hat import SenseHat            # Import Sense HAT hardware driver
    HAS_SENSE_HAT = True                      # Flag indicating hardware library is available
except ImportError:
    HAS_SENSE_HAT = False                     # Still runs cleanly on laptops without Sense HAT

# Preset Winter Bells colours stored as (Display Name, (R, G, B)) tuples
PALETTE = [
    ("Galway Maroon", (127, 0, 61)),
    ("Bell Gold", (255, 205, 20)),
    ("Warm Bronze", (180, 125, 15)),
    ("Ice Blue", (95, 195, 255)),
    ("Winter Blue", (30, 120, 220)),
    ("Snow White", (245, 248, 255)),
    ("Pine Green", (20, 145, 55)),
    ("Forest Green", (10, 85, 30)),
    ("Berry Red", (220, 20, 30)),
    ("Carrot Orange", (255, 130, 20)),
    ("Trunk Brown", (135, 75, 35)),
    ("LED Off", (0, 0, 0)),
]

# Short 1-letter RGB colour constants used to define the 7 starting 8x8 templates below
K = (0, 0, 0)         # Off / Black
R = (220, 20, 30)     # Berry Red
G = (20, 145, 55)     # Pine Green
D = (10, 85, 30)      # Deep Forest Green
L = (65, 205, 95)     # Light Pine Green
Y = (255, 205, 20)    # Bell Gold
M = (180, 125, 15)    # Warm Bell Bronze
W = (245, 248, 255)   # Snow White
B = (95, 195, 255)    # Ice Blue
C = (30, 120, 220)    # Deep Winter Blue
N = (135, 75, 35)     # Trunk / Handle Brown
O = (255, 130, 20)    # Carrot Orange
U = (127, 0, 61)      # Galway Maroon

# Dictionary of all 7 starting 64-pixel Winter Bells templates (matches Web Pixel Studio)
TEMPLATES = {
    "Winter Bell": [
        W, K, K, Y, Y, K, K, K,
        K, K, B, W, B, B, K, K,
        K, K, B, W, B, C, K, K,
        K, B, W, B, B, C, B, K,
        K, B, W, B, C, C, B, K,
        W, B, B, W, B, C, C, W,
        K, K, K, Y, Y, K, K, B,
        K, K, K, K, K, K, K, K,
    ],
    "Bell": [
        K, K, K, N, N, K, K, K,
        K, K, Y, Y, Y, M, K, K,
        K, K, Y, W, Y, M, K, K,
        K, Y, W, Y, Y, M, M, K,
        K, Y, Y, Y, M, M, M, K,
        Y, Y, Y, W, Y, M, M, M,
        K, K, K, M, Y, K, K, K,
        K, K, K, K, K, K, K, K,
    ],
    "Snowflake": [
        W, K, K, B, B, K, K, W,
        K, B, K, W, W, K, B, K,
        K, K, W, B, B, W, K, K,
        B, W, B, W, W, B, W, B,
        B, W, B, W, W, B, W, B,
        K, K, W, B, B, W, K, K,
        K, B, K, W, W, K, B, K,
        W, K, K, B, B, K, K, W,
    ],
    "Winter Star": [
        K, K, K, Y, Y, K, K, K,
        K, K, K, Y, Y, K, K, K,
        Y, Y, Y, W, W, Y, Y, Y,
        K, Y, W, Y, Y, W, Y, K,
        K, K, Y, Y, Y, Y, K, K,
        K, Y, Y, K, K, Y, Y, K,
        Y, Y, K, K, K, K, Y, Y,
        Y, K, K, K, K, K, K, Y,
    ],
    "Snowman": [
        K, K, K, K, K, K, K, K,
        K, K, W, W, W, W, K, K,
        K, K, W, C, W, C, K, K,
        K, K, W, W, O, W, K, K,
        K, K, B, B, B, B, K, K,
        K, W, W, K, W, W, W, K,
        K, W, W, W, W, W, W, K,
        K, K, W, W, W, W, K, K,
    ],
    "Winter Pine": [
        K, K, K, Y, Y, K, K, K,
        K, K, K, W, G, K, K, K,
        K, K, G, B, G, W, K, K,
        K, K, D, G, L, G, K, K,
        K, D, G, L, B, G, D, K,
        W, L, B, G, D, Y, G, W,
        K, K, K, N, N, K, K, K,
        K, K, K, N, N, K, K, K,
    ],
    "Winter Frost Pattern": [
        B, B, W, W, B, B, W, W,
        B, Y, W, C, B, Y, W, C,
        W, W, U, U, W, W, U, U,
        W, C, U, Y, W, C, U, Y,
        B, B, W, W, B, B, W, W,
        B, Y, W, C, B, Y, W, C,
        W, W, U, U, W, W, U, U,
        W, C, U, Y, W, C, U, Y,
    ],
}


def rgb_to_hex(rgb):
    """Convert an (R, G, B) tuple into a Tkinter '#rrggbb' hex string."""
    return "#{:02x}{:02x}{:02x}".format(*rgb)  # Format each channel as 2 hex digits


class PixelStudioApp:
    def __init__(self, root):
        self.root = root                                # Store reference to main Tkinter window
        self.root.title("UoG Winter Bells Lab - Standalone 8x8 Pixel Studio")
        self.root.configure(bg="#0B1628")               # Midnight navy window background

        self.active_color = (95, 195, 255)              # Default brush colour: Ice Blue
        self.grid_colors = [(0, 0, 0)] * 64             # List of 64 RGB tuples for the 8x8 matrix
        self.cells = []                                 # Will hold the 64 clickable cell buttons
        self.sense = SenseHat() if HAS_SENSE_HAT else None  # Connect to Sense HAT if library exists
        if self.sense:
            self.sense.low_light = True                 # Soften LED brightness if Pi HAT attached

        self._build_ui()                                # Construct grid, colour palette, templates, and code box
        self.load_template("Winter Bell")               # Start with the Winter Bell template loaded

    def _build_ui(self):
        # Top window title banner
        header = tk.Label(
            self.root,
            text="University of Galway · Winter Bells 8x8 Sense HAT Pixel Studio",
            font=("Helvetica", 14, "bold"),
            fg="#F5D061",
            bg="#0B1628",
            pady=8,
        )
        header.pack()                                   # Place banner at the top of the window

        # Main 3-column container: 8x8 LED Grid (col 0), Colours (col 1), Templates & Actions (col 2)
        main_frame = tk.Frame(self.root, bg="#0B1628", padx=14, pady=4)
        main_frame.pack()

        # Column 0: Frame holding the 8x8 grid of LED buttons
        grid_frame = tk.Frame(main_frame, bg="#162238", padx=10, pady=10, bd=2, relief="ridge")
        grid_frame.grid(row=0, column=0, padx=(0, 14), sticky="n")

        # Create 64 buttons arranged in 8 rows x 8 columns
        for idx in range(64):
            r, c = divmod(idx, 8)                       # Convert flat index 0..63 into (row, col)
            btn = tk.Button(
                grid_frame,
                width=3,
                height=1,
                bg="#131D31",
                activebackground="#334155",
                relief="flat",
                command=lambda i=idx: self.paint_cell(i),  # Paint pixel i when clicked
            )
            btn.grid(row=r, column=c, padx=2, pady=2)   # Position button at (row, col)
            self.cells.append(btn)                      # Save button widget for colour updates later

        # Column 1: LED Colour Palette Panel
        colour_frame = tk.Frame(main_frame, bg="#0B1628")
        colour_frame.grid(row=0, column=1, padx=(0, 14), sticky="n")

        tk.Label(
            colour_frame,
            text="1. Select LED Colour",
            font=("Helvetica", 10, "bold"),
            fg="#FFFFFF",
            bg="#0B1628",
        ).pack(anchor="w", pady=(0, 4))

        # Create one clickable brush button per colour in PALETTE
        for name, rgb in PALETTE:
            tk.Button(
                colour_frame,
                text=f"{name} [{rgb[0]},{rgb[1]},{rgb[2]}]",
                bg=rgb_to_hex(rgb),
                fg="#FFFFFF" if sum(rgb) < 380 else "#0F172A",  # Contrast text colour automatically
                width=24,
                relief="flat",
                command=lambda col=rgb: self.set_color(col),
            ).pack(pady=1, anchor="w")

        # Button to open OS custom RGB colour chooser
        tk.Button(
            colour_frame,
            text="Pick Custom RGB Colour...",
            bg="#7F003D",
            fg="#FFFFFF",
            width=24,
            pady=3,
            command=self.pick_custom_color,
        ).pack(pady=(6, 0), anchor="w")

        # Column 2: Starting Templates & Export Actions
        ctrl_frame = tk.Frame(main_frame, bg="#0B1628")
        ctrl_frame.grid(row=0, column=2, sticky="n")

        tk.Label(
            ctrl_frame,
            text="2. Load Starting Template",
            font=("Helvetica", 10, "bold"),
            fg="#FFFFFF",
            bg="#0B1628",
        ).pack(anchor="w", pady=(0, 4))

        # Create one button for each of the 7 Winter Bells templates in TEMPLATES
        for template_name in TEMPLATES:
            tk.Button(
                ctrl_frame,
                text=template_name,
                bg="#1E293B",
                fg="#F8FAFC",
                width=25,
                relief="flat",
                command=lambda name=template_name: self.load_template(name),
            ).pack(pady=1, anchor="w")

        tk.Label(
            ctrl_frame,
            text="3. Actions & Export",
            font=("Helvetica", 10, "bold"),
            fg="#FFFFFF",
            bg="#0B1628",
        ).pack(anchor="w", pady=(10, 4))

        # Utility buttons for clearing, physical Pi preview, and copying Python code
        for label, cmd in [
            ("Clear All LEDs", self.clear_grid),
            ("Send to Physical Sense HAT", self.send_to_pi),
            ("Copy Python Code", self.copy_python_code),
        ]:
            tk.Button(
                ctrl_frame,
                text=label,
                bg="#115E3C" if "Copy" in label else "#334155",
                fg="#FFFFFF",
                width=25,
                pady=3,
                command=cmd,
            ).pack(pady=2, anchor="w")

        # Live-updating Python code preview box at the bottom of the window
        self.output_box = tk.Text(
            self.root, height=11, width=92, bg="#08101E", fg="#E2E8F0", font=("Courier", 9)
        )
        self.output_box.pack(padx=14, pady=(6, 12))

    def set_color(self, rgb):
        """Set the active painting brush to the chosen RGB tuple."""
        self.active_color = rgb                         # Update stored brush colour

    def pick_custom_color(self):
        """Open OS colour dialog and convert result into integer RGB values."""
        chosen = colorchooser.askcolor(title="Choose LED RGB Colour")
        if chosen and chosen[0]:                        # Only update if user clicked OK
            self.active_color = tuple(int(v) for v in chosen[0])

    def paint_cell(self, idx):
        """Update pixel at index idx and refresh both grid and generated Python code."""
        self.grid_colors[idx] = self.active_color       # Save active colour into cell idx
        self.refresh_grid()                             # Redraw grid and regenerate Python snippet

    def clear_grid(self):
        """Turn off all 64 pixels."""
        self.grid_colors = [(0, 0, 0)] * 64             # Reset every pixel to black/off
        self.refresh_grid()                             # Redraw grid and regenerate Python snippet

    def load_template(self, name):
        """Load one of the 7 starting 64-pixel Winter Bells templates into the grid."""
        self.grid_colors = list(TEMPLATES[name])        # Make a fresh copy of the chosen 64-pixel list
        self.refresh_grid()                             # Redraw grid and regenerate Python snippet

    def refresh_grid(self):
        """Repaint every button colour and update the Python code box."""
        for idx, rgb in enumerate(self.grid_colors):    # Loop through all 64 pixels
            hex_col = "#131D31" if rgb == (0, 0, 0) else rgb_to_hex(rgb)
            self.cells[idx].configure(bg=hex_col)       # Update button background colour
        self.update_code_preview()                      # Keep bottom Python text box in sync

    def build_python_snippet(self):
        """Format the 64 RGB tuples into a commented 8x8 Python list."""
        rows = []                                       # Collect one formatted string per LED row
        for y in range(8):
            row = ", ".join(f"[{r}, {g}, {b}]" for (r, g, b) in self.grid_colors[y * 8 : y * 8 + 8])
            rows.append(f"    {row},  # Row {y} (indices {y * 8}..{y * 8 + 7})")
        return (
            "# 64 [R, G, B] pixels in row-major order: index = (row * 8) + col\n"
            "# Paste this list into TODO 2 of task2_display_and_art.py\n"
            "my_winter_bell_art = [\n" + "\n".join(rows) + "\n]"
        )

    def update_code_preview(self):
        """Replace text box contents with the latest Python list."""
        self.output_box.delete("1.0", tk.END)           # Clear old code text
        self.output_box.insert("1.0", self.build_python_snippet())  # Insert updated Python snippet

    def send_to_pi(self):
        """Push the current 64-pixel grid directly to a connected Sense HAT."""
        if not self.sense:                              # Guard if running on a PC without Sense HAT
            messagebox.showinfo("Sense HAT", "Physical Sense HAT not detected on this device.")
            return
        self.sense.set_pixels([list(c) for c in self.grid_colors])  # Display art on LED matrix

    def copy_python_code(self):
        """Copy the generated Python list to the system clipboard."""
        code = self.build_python_snippet()              # Generate latest 64-pixel Python snippet
        self.root.clipboard_clear()                     # Empty clipboard before writing
        self.root.clipboard_append(code)                # Put code on OS clipboard
        messagebox.showinfo("Copied!", "64-pixel Python list copied! Paste it into task2_display_and_art.py.")


if __name__ == "__main__":
    root = tk.Tk()                                      # Create the main Tkinter GUI window
    app = PixelStudioApp(root)                          # Initialise Pixel Studio inside the window
    root.mainloop()                                     # Start GUI event loop until window closes
