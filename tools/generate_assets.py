"""
GATE DOMINION - Asset Generator
================================
AI Role: AI_ARTIST + AI_SOUND_DESIGNER

Generates all placeholder textures (PNG) and audio (WAV) procedurally.
No external dependencies — uses raw binary output only.

Usage:
    python generate_assets.py <project_dir>
"""

import sys
import os
import struct
import zlib
import math


# ============================================================
#  CONFIGURATION
# ============================================================

GAME_NAME = "Gate Dominion"

# All assets to generate: (relative_path, generator_function, kwargs)
TEXTURE_FILES = [
    # Units
    ("assets/textures/units/builder.png",         "tex_builder",      {}),
    ("assets/textures/units/soldier.png",          "tex_soldier",      {}),
    # Structures
    ("assets/textures/structures/powerplant.png",  "tex_powerplant",   {}),
    ("assets/textures/structures/factory.png",     "tex_factory",      {}),
    # UI
    ("assets/textures/ui/button.png",              "tex_button",       {}),
    ("assets/textures/ui/panel.png",               "tex_panel",        {}),
    ("assets/textures/ui/icon_energy.png",         "tex_icon_energy",  {}),
    ("assets/textures/ui/icon_mineral.png",        "tex_icon_mineral", {}),
    # Planets
    ("assets/textures/planets/planet_blue.png",    "tex_planet",       {"r": 40,  "g": 100, "b": 220}),
    ("assets/textures/planets/planet_red.png",     "tex_planet",       {"r": 200, "g": 50,  "b": 50}),
    ("assets/textures/planets/planet_green.png",   "tex_planet",       {"r": 50,  "g": 180, "b": 80}),
]

AUDIO_FILES = [
    ("assets/audio/click.wav",     "wav_click",     {}),
    ("assets/audio/build.wav",     "wav_build",     {}),
    ("assets/audio/shoot.wav",     "wav_shoot",     {}),
    ("assets/audio/explosion.wav", "wav_explosion", {}),
    ("assets/audio/ambient.wav",   "wav_ambient",   {}),
]


# ============================================================
#  PNG HELPER — raw PNG writer (no dependencies)
# ============================================================

def make_png(width, height, pixels):
    """
    Build a PNG file from raw RGBA pixel data.
    pixels: list of rows, each row is list of (r, g, b, a) tuples.
    Returns bytes.
    """
    raw_rows = []
    for row in pixels:
        raw_row = b"\x00"  # filter byte: None
        for r, g, b, a in row:
            raw_row += bytes([r & 0xFF, g & 0xFF, b & 0xFF, a & 0xFF])
        raw_rows.append(raw_row)
    raw_data = b"".join(raw_rows)
    compressed = zlib.compress(raw_data)

    def chunk(ctype, data):
        c = ctype + data
        crc = struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + c + crc

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", compressed)
    png += chunk(b"IEND", b"")
    return png


def filled_rect(pixels, x0, y0, w, h, color):
    """Draw a filled rectangle into the pixel buffer."""
    for y in range(y0, min(y0 + h, len(pixels))):
        for x in range(x0, min(x0 + w, len(pixels[0]))):
            pixels[y][x] = color


def draw_circle(pixels, cx, cy, radius, color):
    """Draw a filled circle into the pixel buffer."""
    height = len(pixels)
    width = len(pixels[0]) if height > 0 else 0
    for y in range(max(0, cy - radius), min(height, cy + radius + 1)):
        for x in range(max(0, cx - radius), min(width, cx + radius + 1)):
            if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                pixels[y][x] = color


def draw_border(pixels, thickness, color):
    """Draw a border around the entire image."""
    h = len(pixels)
    w = len(pixels[0]) if h > 0 else 0
    for y in range(h):
        for x in range(w):
            if x < thickness or x >= w - thickness or y < thickness or y >= h - thickness:
                pixels[y][x] = color


def new_canvas(w, h, bg=(0, 0, 0, 0)):
    """Create a blank pixel buffer."""
    return [[bg for _ in range(w)] for _ in range(h)]


# ============================================================
#  TEXTURE GENERATORS
# ============================================================

def tex_builder():
    """64x64 builder unit — green square with wrench shape."""
    S = 64
    px = new_canvas(S, S, (10, 15, 30, 255))
    # Body — green square
    filled_rect(px, 12, 12, 40, 40, (40, 200, 90, 255))
    # Inner highlight
    filled_rect(px, 18, 18, 28, 28, (60, 230, 110, 255))
    # "B" mark — darker center cross
    filled_rect(px, 28, 14, 8, 36, (20, 140, 60, 255))
    filled_rect(px, 16, 28, 32, 8, (20, 140, 60, 255))
    draw_border(px, 2, (80, 255, 140, 255))
    return make_png(S, S, px)


def tex_soldier():
    """64x64 soldier unit — blue square with sword shape."""
    S = 64
    px = new_canvas(S, S, (10, 15, 30, 255))
    # Body — blue
    filled_rect(px, 12, 12, 40, 40, (50, 90, 200, 255))
    filled_rect(px, 18, 18, 28, 28, (70, 120, 230, 255))
    # Sword — vertical line + cross guard
    filled_rect(px, 30, 10, 4, 44, (200, 200, 220, 255))
    filled_rect(px, 22, 24, 20, 4, (200, 200, 220, 255))
    draw_border(px, 2, (100, 150, 255, 255))
    return make_png(S, S, px)


def tex_powerplant():
    """64x64 power plant — yellow with lightning bolt."""
    S = 64
    px = new_canvas(S, S, (10, 15, 30, 255))
    # Building body
    filled_rect(px, 8, 16, 48, 40, (180, 170, 40, 255))
    filled_rect(px, 12, 20, 40, 32, (220, 210, 60, 255))
    # Roof
    filled_rect(px, 4, 12, 56, 8, (140, 130, 30, 255))
    # Lightning bolt (simplified as zigzag)
    filled_rect(px, 30, 22, 8, 6, (255, 255, 200, 255))
    filled_rect(px, 26, 28, 8, 6, (255, 255, 200, 255))
    filled_rect(px, 30, 34, 8, 6, (255, 255, 200, 255))
    filled_rect(px, 26, 40, 8, 6, (255, 255, 200, 255))
    draw_border(px, 2, (255, 230, 80, 255))
    return make_png(S, S, px)


def tex_factory():
    """64x64 factory — purple with gear symbol."""
    S = 64
    px = new_canvas(S, S, (10, 15, 30, 255))
    # Building body
    filled_rect(px, 8, 20, 48, 36, (100, 50, 160, 255))
    filled_rect(px, 12, 24, 40, 28, (130, 70, 190, 255))
    # Chimney
    filled_rect(px, 14, 8, 10, 16, (80, 40, 130, 255))
    filled_rect(px, 40, 10, 10, 14, (80, 40, 130, 255))
    # Gear — circle in center
    draw_circle(px, 32, 38, 8, (200, 180, 230, 255))
    draw_circle(px, 32, 38, 4, (100, 50, 160, 255))
    draw_border(px, 2, (170, 120, 230, 255))
    return make_png(S, S, px)


def tex_button():
    """128x64 UI button — rounded-look rectangle."""
    W, H = 128, 64
    px = new_canvas(W, H, (0, 0, 0, 0))
    # Main body
    filled_rect(px, 2, 2, W - 4, H - 4, (50, 60, 90, 220))
    # Top highlight
    filled_rect(px, 4, 4, W - 8, 8, (80, 90, 130, 200))
    # Bottom shadow
    filled_rect(px, 4, H - 12, W - 8, 8, (30, 35, 60, 200))
    draw_border(px, 2, (100, 120, 180, 255))
    return make_png(W, H, px)


def tex_panel():
    """128x128 UI panel background."""
    S = 128
    px = new_canvas(S, S, (20, 25, 45, 230))
    # Inner area
    filled_rect(px, 4, 4, S - 8, S - 8, (30, 35, 60, 240))
    # Top bar accent
    filled_rect(px, 4, 4, S - 8, 6, (60, 80, 140, 255))
    draw_border(px, 2, (70, 90, 150, 255))
    return make_png(S, S, px)


def tex_icon_energy():
    """32x32 energy icon — yellow lightning bolt."""
    S = 32
    px = new_canvas(S, S, (0, 0, 0, 0))
    yellow = (255, 220, 40, 255)
    # Lightning bolt shape
    filled_rect(px, 14, 2, 6, 5, yellow)
    filled_rect(px, 11, 7, 6, 5, yellow)
    filled_rect(px, 14, 12, 6, 5, yellow)
    filled_rect(px, 11, 17, 6, 5, yellow)
    filled_rect(px, 14, 22, 6, 5, yellow)
    filled_rect(px, 11, 27, 6, 3, yellow)
    return make_png(S, S, px)


def tex_icon_mineral():
    """32x32 mineral icon — cyan diamond."""
    S = 32
    px = new_canvas(S, S, (0, 0, 0, 0))
    cyan = (40, 200, 230, 255)
    dark = (20, 120, 160, 255)
    # Diamond shape — draw a centered diamond
    cx, cy = S // 2, S // 2
    for y in range(S):
        for x in range(S):
            dx = abs(x - cx)
            dy = abs(y - cy)
            if dx + dy <= 12:
                px[y][x] = cyan if dx + dy <= 9 else dark
    return make_png(S, S, px)


def tex_planet(r=100, g=100, b=200):
    """64x64 planet — colored circle with shading."""
    S = 64
    cx, cy = S // 2, S // 2
    radius = 28
    px = new_canvas(S, S, (0, 0, 0, 0))
    for y in range(S):
        for x in range(S):
            dx = x - cx
            dy = y - cy
            dist_sq = dx * dx + dy * dy
            if dist_sq <= radius * radius:
                # Simple shading: lighter top-left, darker bottom-right
                shade = 1.0 - (dx + dy) / (radius * 3.0)
                shade = max(0.3, min(1.3, shade))
                pr = int(r * shade)
                pg = int(g * shade)
                pb = int(b * shade)
                px[y][x] = (min(255, pr), min(255, pg), min(255, pb), 255)
    return make_png(S, S, px)


# ============================================================
#  WAV HELPER — raw WAV writer (no dependencies)
# ============================================================

def make_wav(samples, sample_rate=22050, channels=1, bits=16):
    """
    Build a WAV file from a list of float samples (-1.0 to 1.0).
    Returns bytes.
    """
    num_samples = len(samples)
    bytes_per_sample = bits // 8
    data_size = num_samples * channels * bytes_per_sample
    max_val = (2 ** (bits - 1)) - 1

    # Convert float samples to int16
    raw = b""
    for s in samples:
        clamped = max(-1.0, min(1.0, s))
        raw += struct.pack("<h", int(clamped * max_val))

    # WAV header
    header = b"RIFF"
    header += struct.pack("<I", 36 + data_size)  # file size - 8
    header += b"WAVE"
    # fmt chunk
    header += b"fmt "
    header += struct.pack("<I", 16)               # chunk size
    header += struct.pack("<H", 1)                 # PCM format
    header += struct.pack("<H", channels)
    header += struct.pack("<I", sample_rate)
    header += struct.pack("<I", sample_rate * channels * bytes_per_sample)
    header += struct.pack("<H", channels * bytes_per_sample)
    header += struct.pack("<H", bits)
    # data chunk
    header += b"data"
    header += struct.pack("<I", data_size)

    return header + raw


def generate_tone(freq, duration, sample_rate=22050, volume=0.5, wave="sine"):
    """Generate a simple waveform."""
    num_samples = int(sample_rate * duration)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        if wave == "sine":
            val = math.sin(2.0 * math.pi * freq * t) * volume
        elif wave == "square":
            val = volume if math.sin(2.0 * math.pi * freq * t) >= 0 else -volume
        elif wave == "sawtooth":
            val = (2.0 * (t * freq - math.floor(t * freq + 0.5))) * volume
        elif wave == "noise":
            # Simple pseudo-noise using sine mixing
            val = (math.sin(freq * t * 6.283) *
                   math.sin(freq * 1.37 * t * 6.283) *
                   math.sin(freq * 2.71 * t * 6.283)) * volume
        else:
            val = 0.0
        samples.append(val)
    return samples


def apply_envelope(samples, attack=0.01, decay=0.1, sustain=0.7, release=0.2):
    """Apply a simple ADSR envelope to samples."""
    total = len(samples)
    if total == 0:
        return samples

    sr = 22050
    a_end = int(attack * sr)
    d_end = a_end + int(decay * sr)
    r_start = total - int(release * sr)

    result = []
    for i, s in enumerate(samples):
        if i < a_end:
            # Attack
            env = i / max(1, a_end)
        elif i < d_end:
            # Decay
            progress = (i - a_end) / max(1, d_end - a_end)
            env = 1.0 - progress * (1.0 - sustain)
        elif i < r_start:
            # Sustain
            env = sustain
        else:
            # Release
            progress = (i - r_start) / max(1, total - r_start)
            env = sustain * (1.0 - progress)
        result.append(s * env)
    return result


# ============================================================
#  AUDIO GENERATORS
# ============================================================

def wav_click():
    """Short UI click sound."""
    samples = generate_tone(800, 0.08, volume=0.6, wave="sine")
    samples += generate_tone(600, 0.04, volume=0.3, wave="sine")
    samples = apply_envelope(samples, attack=0.002, decay=0.02, sustain=0.3, release=0.05)
    return make_wav(samples)


def wav_build():
    """Building placement sound — ascending tone."""
    s1 = generate_tone(200, 0.15, volume=0.5, wave="sawtooth")
    s2 = generate_tone(300, 0.15, volume=0.5, wave="sawtooth")
    s3 = generate_tone(400, 0.2, volume=0.4, wave="sine")
    samples = s1 + s2 + s3
    samples = apply_envelope(samples, attack=0.01, decay=0.1, sustain=0.6, release=0.15)
    return make_wav(samples)


def wav_shoot():
    """Laser/shoot sound — short descending tone."""
    samples = generate_tone(1200, 0.05, volume=0.7, wave="square")
    samples += generate_tone(600, 0.05, volume=0.5, wave="square")
    samples += generate_tone(300, 0.05, volume=0.3, wave="sine")
    samples = apply_envelope(samples, attack=0.005, decay=0.03, sustain=0.4, release=0.05)
    return make_wav(samples)


def wav_explosion():
    """Explosion sound — noise burst with low rumble."""
    noise = generate_tone(80, 0.4, volume=0.8, wave="noise")
    rumble = generate_tone(50, 0.5, volume=0.6, wave="sine")
    # Mix noise and rumble
    length = max(len(noise), len(rumble))
    samples = []
    for i in range(length):
        n = noise[i] if i < len(noise) else 0.0
        r = rumble[i] if i < len(rumble) else 0.0
        samples.append((n + r) * 0.5)
    samples = apply_envelope(samples, attack=0.005, decay=0.15, sustain=0.4, release=0.3)
    return make_wav(samples)


def wav_ambient():
    """Ambient background — low drone, 3 seconds."""
    dur = 3.0
    s1 = generate_tone(60, dur, volume=0.15, wave="sine")
    s2 = generate_tone(90, dur, volume=0.10, wave="sine")
    s3 = generate_tone(120, dur, volume=0.05, wave="sine")
    samples = []
    for i in range(len(s1)):
        v2 = s2[i] if i < len(s2) else 0.0
        v3 = s3[i] if i < len(s3) else 0.0
        samples.append(s1[i] + v2 + v3)
    samples = apply_envelope(samples, attack=0.5, decay=0.5, sustain=0.8, release=0.8)
    return make_wav(samples)


# ============================================================
#  FILE WRITER
# ============================================================

def write_binary(project_dir, relative_path, data):
    """Write binary data to a file, creating directories as needed."""
    full_path = os.path.join(project_dir, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "wb") as f:
        f.write(data)
    return full_path


# ============================================================
#  MAIN
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_assets.py <project_dir>")
        sys.exit(1)

    project_dir = os.path.abspath(sys.argv[1])
    print(f"  Project directory: {project_dir}")
    print(f"  Game: {GAME_NAME}")
    print()

    # --- Map generator names to functions ---
    tex_generators = {
        "tex_builder":      tex_builder,
        "tex_soldier":      tex_soldier,
        "tex_powerplant":   tex_powerplant,
        "tex_factory":      tex_factory,
        "tex_button":       tex_button,
        "tex_panel":        tex_panel,
        "tex_icon_energy":  tex_icon_energy,
        "tex_icon_mineral": tex_icon_mineral,
        "tex_planet":       tex_planet,
    }

    wav_generators = {
        "wav_click":     wav_click,
        "wav_build":     wav_build,
        "wav_shoot":     wav_shoot,
        "wav_explosion": wav_explosion,
        "wav_ambient":   wav_ambient,
    }

    generated = []

    # --- Textures ---
    print("  Generating textures...")
    for rel_path, gen_name, kwargs in TEXTURE_FILES:
        gen_func = tex_generators.get(gen_name)
        if not gen_func:
            print(f"  WARNING: No generator '{gen_name}', skipping {rel_path}")
            continue
        data = gen_func(**kwargs)
        write_binary(project_dir, rel_path, data)
        generated.append(rel_path)
        print(f"  [OK] {rel_path}")

    print()

    # --- Audio ---
    print("  Generating audio...")
    for rel_path, gen_name, kwargs in AUDIO_FILES:
        gen_func = wav_generators.get(gen_name)
        if not gen_func:
            print(f"  WARNING: No generator '{gen_name}', skipping {rel_path}")
            continue
        data = gen_func(**kwargs)
        write_binary(project_dir, rel_path, data)
        generated.append(rel_path)
        print(f"  [OK] {rel_path}")

    # --- Summary ---
    print()
    print("  ========================================")
    print(f"  ASSET GENERATION COMPLETE: {GAME_NAME}")
    print(f"  Textures: {len(TEXTURE_FILES)}")
    print(f"  Audio:    {len(AUDIO_FILES)}")
    print(f"  Total:    {len(generated)} files")
    print("  ========================================")
    print()
    print("  Generated files:")
    for f in generated:
        print(f"    - {f}")
    print()
    print("  All assets ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
