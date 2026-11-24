#!/bin/bash
# ==============================================================
# University of Galway - Winter Bells Lab (Pre-Task Setup Script)
# Installs Sense HAT, Pygame, NumPy, Tkinter, and Python editors
# ==============================================================

# Print a welcome banner in the Terminal
echo "==========================================================="
echo "  Prelab - Winter Bells Lab Pre-Task Setup"
echo "==========================================================="

# 1. Verify Python 3 is installed on this computer
if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERROR] Python 3 not found. Please install python3."
    exit 1
fi
echo "[OK] Found $(python3 --version)"

# 2. Check if this script is running on a physical Raspberry Pi
if [ -f /proc/device-tree/model ] && grep -qi "Raspberry Pi" /proc/device-tree/model; then
    # Read the Raspberry Pi board model name safely
    MODEL=$(tr -d '\0' < /proc/device-tree/model)
    echo "[OK] Raspberry Pi detected: $MODEL"
else
    echo "[INFO] Non-Pi environment detected (desktop/VM mode)."
fi

# Helper function: install an apt package only if it exists in apt repositories
install_if_available() {
    PKG="$1"    # First argument: apt package name (e.g. python3-pygame)
    LABEL="$2"  # Second argument: friendly label for Terminal output
    if apt-cache show "$PKG" >/dev/null 2>&1; then
        echo "Installing $LABEL ($PKG)..."
        sudo apt-get install -y "$PKG" || echo "[WARN] Could not install $PKG automatically."
    else
        echo "[SKIP] Apt package '$PKG' is not available in your repositories."
    fi
}

# 3. Refresh the apt package list (continue safely if offline so pre-installed libraries still verify)
echo ""
echo "Updating package lists..."
if ! sudo apt-get update; then
    echo "[WARN] apt-get update failed (offline or repository issue). Checking existing packages..."
fi

# 4. Check each required Python library individually before attempting install
for pair in "sense_hat:python3-sense-hat:Sense HAT" "pygame:python3-pygame:Pygame" "numpy:python3-numpy:NumPy" "tkinter:python3-tk:Tkinter GUI"; do
    MOD="${pair%%:*}"    # Extract Python module name before first ':'
    REST="${pair#*:}"    # Extract remaining string after first ':'
    PKG="${REST%%:*}"    # Extract apt package name
    LABEL="${REST#*:}"   # Extract friendly label
    if python3 -c "import $MOD" 2>/dev/null; then
        echo "[OK] $LABEL ($MOD) is already available."
    else
        install_if_available "$PKG" "$LABEL"
    fi
done

# 5. Check whether Thonny or Geany editors are installed (without failing if one is absent)
for editor in "thonny:Thonny IDE" "geany:Geany Editor"; do
    CMD="${editor%%:*}"
    LABEL="${editor#*:}"
    if command -v "$CMD" >/dev/null 2>&1; then
        echo "[OK] $LABEL is already installed."
    else
        install_if_available "$CMD" "$LABEL"
    fi
done

# 6. Final Python import verification across all four libraries
echo ""
echo "Verifying Python packages..."
ALL_OK=1
for mod in sense_hat pygame numpy tkinter; do
    if python3 -c "import $mod" 2>/dev/null; then
        echo "[OK]      $mod is ready"
    else
        echo "[MISSING] $mod could not be imported"
        ALL_OK=0
    fi
done

# 7. Print final readiness status
echo ""
if [ $ALL_OK -eq 1 ]; then
    echo "SUCCESS! Pre-Task complete. Your Raspberry Pi is ready for the lab."
    echo "Next: Run task1_verify.py, then work through the tasks in order."
else
    echo "WARNING: One or more packages could not be imported."
    echo "If using a Python virtual environment, create it with --system-site-packages."
fi
