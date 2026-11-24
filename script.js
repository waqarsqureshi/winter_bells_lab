"use strict";

const COLOURS = {
  K: [0, 0, 0],
  R: [220, 20, 30],
  G: [20, 145, 55],
  D: [10, 85, 30],
  L: [65, 205, 95],
  Y: [255, 205, 20],
  M: [180, 125, 15],
  W: [245, 248, 255],
  B: [95, 195, 255],
  C: [30, 120, 220],
  N: [135, 75, 35],
  O: [255, 130, 20],
  U: [127, 0, 61],
};

const PALETTE = [
  { name: "Galway Maroon", rgb: [127, 0, 61] },
  { name: "Bell Gold", rgb: [255, 205, 20] },
  { name: "Warm Bronze", rgb: [180, 125, 15] },
  { name: "Ice Blue", rgb: [95, 195, 255] },
  { name: "Winter Blue", rgb: [30, 120, 220] },
  { name: "Snow White", rgb: [245, 248, 255] },
  { name: "Pine Green", rgb: [20, 145, 55] },
  { name: "Forest Green", rgb: [10, 85, 30] },
  { name: "Berry Red", rgb: [220, 20, 30] },
  { name: "Carrot Orange", rgb: [255, 130, 20] },
  { name: "Trunk Brown", rgb: [135, 75, 35] },
  { name: "LED Off", rgb: [0, 0, 0] },
];

const TEMPLATES = {
  "Winter Bell": [
    "WKKYYKKK", "KKBWBBKK", "KKBWBCKK", "KBWBBCBK",
    "KBWBCCBK", "WBBWBCCW",
    "KKKYYKKB", "KKKKKKKK",
  ],
  Bell: [
    "KKKNNKKK", "KKYYYMKK", "KKYWYMKK", "KYWYYMMK",
    "KYYYMMMK", "YYYWYMMM", "KKKMYKKK", "KKKKKKKK",
  ],
  Snowflake: [
    "WKKBBKKW", "KBKWWKBK", "KKWBBWKK", "BWBWWBWB",
    "BWBWWBWB", "KKWBBWKK", "KBKWWKBK", "WKKBBKKW",
  ],
  "Winter Star": [
    "KKKYYKKK", "KKKYYKKK", "YYYWWYYY", "KYWYYWYK",
    "KKYYYYKK", "KYYKKYYK", "YYKKKKYY", "YKKKKKKY",
  ],
  Snowman: [
    "KKKKKKKK", "KKWWWWKK", "KKWCWCKK", "KKWWOWKK",
    "KKBBBBKK", "KWWKWWWK", "KWWWWWWK", "KKWWWWKK",
  ],
  "Winter Pine": [
    "KKKYYKKK", "KKKWGKKK", "KKGBGWKK", "KKDGLGKK",
    "KDGLBGDK", "WLBGDYGW", "KKKNNKKK", "KKKNNKKK",
  ],
  "Winter Frost Pattern": [
    "BBWWBBWW", "BYWCBYWC",
    "WWUUWWUU", "WCUYWCUY",
    "BBWWBBWW", "BYWCBYWC", "WWUUWWUU", "WCUYWCUY",
  ],
};

const grid = document.querySelector("#pixel-grid");
const palette = document.querySelector("#palette");
const templateSelect = document.querySelector("#template-select");
const customColour = document.querySelector("#custom-colour");
const eraseButton = document.querySelector("#erase-button");
const clearButton = document.querySelector("#clear-button");
const copyButton = document.querySelector("#copy-button");
const downloadButton = document.querySelector("#download-art-button");
const preview = document.querySelector("#code-preview");
const status = document.querySelector("#studio-status");
const pixelCount = document.querySelector("#pixel-count");
const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector("#site-nav");

let pixels = Array.from({ length: 64 }, () => [0, 0, 0]);
let activeColour = [95, 195, 255];
let focusedPixel = 0;
const pixelButtons = [];

function rgbCss(rgb) {
  return `rgb(${rgb[0]} ${rgb[1]} ${rgb[2]})`;
}

function setStatus(message, isError = false) {
  status.textContent = message;
  status.classList.toggle("status-error", isError);
}

function buildPalette() {
  for (const colour of PALETTE) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "palette-button";
    button.setAttribute("aria-pressed", "false");
    button.setAttribute("aria-label", `${colour.name}, RGB ${colour.rgb.join(", ")}`);
    const swatch = document.createElement("span");
    swatch.className = "swatch";
    swatch.style.backgroundColor = rgbCss(colour.rgb);
    swatch.setAttribute("aria-hidden", "true");
    const name = document.createElement("span");
    name.textContent = colour.name;
    button.append(swatch, name);
    button.addEventListener("click", () => selectColour(colour.rgb, button));
    palette.append(button);
  }
}

function selectColour(rgb, selectedButton = null) {
  activeColour = [...rgb];
  eraseButton.setAttribute("aria-pressed", "false");
  palette.querySelectorAll(".palette-button").forEach((button) => {
    button.setAttribute("aria-pressed", String(button === selectedButton));
  });
  setStatus(`Brush colour: RGB ${activeColour.join(", ")}.`);
}

function updateGrid() {
  pixels.forEach((rgb, index) => {
    const button = pixelButtons[index];
    button.style.backgroundColor = rgbCss(rgb);
    button.setAttribute("aria-label", `Row ${Math.floor(index / 8) + 1}, column ${(index % 8) + 1}, RGB ${rgb.join(", ")}`);
  });
  preview.textContent = buildPythonCode();
  pixelCount.textContent = `${pixels.length} pixels`;
}

function paint(index) {
  pixels[index] = [...activeColour];
  updateGrid();
  setStatus(`Updated row ${Math.floor(index / 8) + 1}, column ${(index % 8) + 1}.`);
}

function buildGrid() {
  for (let index = 0; index < 64; index += 1) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "pixel-cell";
    button.dataset.index = String(index);
    button.tabIndex = index === 0 ? 0 : -1;
    button.setAttribute("aria-label", `Row ${Math.floor(index / 8) + 1}, column ${(index % 8) + 1}, LED off`);
    button.addEventListener("click", () => paint(index));
    button.addEventListener("pointerover", (event) => {
      if (event.buttons === 1) paint(index);
    });
    button.addEventListener("keydown", (event) => {
      const row = Math.floor(index / 8);
      const column = index % 8;
      const movements = {
        ArrowUp: row > 0 ? index - 8 : index,
        ArrowDown: row < 7 ? index + 8 : index,
        ArrowLeft: column > 0 ? index - 1 : index,
        ArrowRight: column < 7 ? index + 1 : index,
      };
      if (Object.hasOwn(movements, event.key)) {
        event.preventDefault();
        focusPixel(movements[event.key]);
      }
      if ((event.key === " " || event.key === "Enter") && !event.repeat) {
        event.preventDefault();
        paint(index);
      }
    });
    pixelButtons.push(button);
    grid.append(button);
  }
}

function focusPixel(index) {
  focusedPixel = index;
  pixelButtons.forEach((button, buttonIndex) => {
    button.tabIndex = buttonIndex === focusedPixel ? 0 : -1;
  });
  pixelButtons[focusedPixel].focus();
}

function loadTemplate(name) {
  if (name === "Blank") {
    pixels = Array.from({ length: 64 }, () => [0, 0, 0]);
    updateGrid();
    setStatus("Blank 8×8 canvas loaded.");
    return;
  }
  const rows = TEMPLATES[name];
  if (!rows || rows.length !== 8 || rows.some((row) => row.length !== 8)) {
    setStatus(`Could not load "${name}": the design must have exactly 8 rows of 8 pixels.`, true);
    return;
  }
  pixels = rows.join("").split("").map((symbol) => {
    const rgb = COLOURS[symbol];
    if (!rgb) throw new Error(`Unknown pixel colour: ${symbol}`);
    return [...rgb];
  });
  if (pixels.length !== 64) {
    throw new Error(`Template "${name}" produced ${pixels.length} pixels instead of 64.`);
  }
  updateGrid();
  setStatus(`${name} template loaded.`);
}

function buildPythonCode() {
  const rows = [];
  for (let rowIndex = 0; rowIndex < 8; rowIndex += 1) {
    const row = pixels
      .slice(rowIndex * 8, rowIndex * 8 + 8)
      .map((rgb) => `[${rgb.join(", ")}]`)
      .join(", ");
    const first = rowIndex * 8;
    rows.push(`    ${row},  # Row ${rowIndex} (indices ${first}..${first + 7})`);
  }
  return [
    "# 64 [R, G, B] pixels in row-major order: index = (row * 8) + col",
    "# Paste this list into TODO 2 of task2_display_and_art.py",
    "my_winter_bell_art = [",
    ...rows,
    "]",
  ].join("\n");
}

async function copyPythonCode() {
  const code = buildPythonCode();
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(code);
    } else {
      const temporary = document.createElement("textarea");
      temporary.value = code;
      temporary.setAttribute("readonly", "");
      temporary.style.position = "fixed";
      temporary.style.opacity = "0";
      document.body.append(temporary);
      temporary.select();
      const copied = document.execCommand("copy");
      temporary.remove();
      if (!copied) throw new Error("The browser did not allow clipboard access.");
    }
    setStatus("Copied the 64-pixel Python list. Paste it into TODO 2.");
  } catch (error) {
    setStatus(`Could not copy automatically: ${error.message} You can select and copy the code preview instead.`, true);
  }
}

function downloadPythonCode() {
  try {
    const blob = new Blob([`${buildPythonCode()}\n`], { type: "text/x-python;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "winter_bell_pixel_art.py";
    document.body.append(link);
    link.click();
    link.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    setStatus("Downloaded winter_bell_pixel_art.py with the 64-pixel list.");
  } catch (error) {
    setStatus(`Could not create the download: ${error.message}`, true);
  }
}

buildPalette();
buildGrid();
updateGrid();
loadTemplate("Winter Bell");

templateSelect.addEventListener("change", () => loadTemplate(templateSelect.value));
customColour.addEventListener("input", () => {
  const hex = customColour.value.slice(1);
  const rgb = [0, 2, 4].map((offset) => Number.parseInt(hex.slice(offset, offset + 2), 16));
  selectColour(rgb);
});
eraseButton.addEventListener("click", () => {
  activeColour = [0, 0, 0];
  palette.querySelectorAll(".palette-button").forEach((button) => button.setAttribute("aria-pressed", "false"));
  eraseButton.setAttribute("aria-pressed", "true");
  setStatus("Erase selected: painted pixels will be turned off.");
});
clearButton.addEventListener("click", () => {
  pixels = Array.from({ length: 64 }, () => [0, 0, 0]);
  updateGrid();
  setStatus("Canvas cleared.");
});
copyButton.addEventListener("click", copyPythonCode);
downloadButton.addEventListener("click", downloadPythonCode);

navToggle.addEventListener("click", () => {
  const isExpanded = navToggle.getAttribute("aria-expanded") === "true";
  navToggle.setAttribute("aria-expanded", String(!isExpanded));
  siteNav.classList.toggle("is-open", !isExpanded);
});
siteNav.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    navToggle.setAttribute("aria-expanded", "false");
    siteNav.classList.remove("is-open");
  });
});
