"""
GATE DOMINION - Visual & Gameplay Polish Generator
====================================================
AI Role: AI_ARTIST + AI_FX_DESIGNER + AI_GAMEPLAY_TUNER

Final quality pass that transforms the functional prototype into a
visually coherent 2D strategy game.  Generates animated sprite sheets,
particle effects, a UI theme, camera juice, and gameplay balance scripts.

Runs AFTER all other generators.

Usage:
    python generate_polish.py <project_dir>
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

FRAME_SIZE = 64
SHEET_COLS = 4
SHEET_ROWS = 4
SHEET_W = FRAME_SIZE * SHEET_COLS   # 256
SHEET_H = FRAME_SIZE * SHEET_ROWS   # 256
NUM_FRAMES = SHEET_COLS * SHEET_ROWS  # 16

# --- File tables ---
SPRITESHEET_FILES = [
    ("assets/spritesheets/builder_idle.png",     "spr_builder_idle"),
    ("assets/spritesheets/builder_walk.png",     "spr_builder_walk"),
    ("assets/spritesheets/builder_build.png",    "spr_builder_build"),
    ("assets/spritesheets/soldier_idle.png",     "spr_soldier_idle"),
    ("assets/spritesheets/soldier_walk.png",     "spr_soldier_walk"),
    ("assets/spritesheets/soldier_attack.png",   "spr_soldier_attack"),
    ("assets/spritesheets/soldier_die.png",      "spr_soldier_die"),
    ("assets/spritesheets/powerplant_idle.png",  "spr_powerplant_idle"),
    ("assets/spritesheets/powerplant_work.png",  "spr_powerplant_work"),
    ("assets/spritesheets/factory_idle.png",     "spr_factory_idle"),
    ("assets/spritesheets/factory_work.png",     "spr_factory_work"),
]

SCRIPT_FILES = [
    ("scripts/polish/balance_data.gd",     "gen_balance_data"),
    ("scripts/polish/ai_tuning.gd",        "gen_ai_tuning"),
    ("scripts/polish/object_pool.gd",      "gen_object_pool"),
    ("scripts/polish/animation_setup.gd",  "gen_animation_setup"),
    ("scripts/polish/camera_fx.gd",        "gen_camera_fx"),
    ("scripts/polish/ui_animator.gd",      "gen_ui_animator"),
    ("scripts/polish/ui_tooltips.gd",      "gen_ui_tooltips"),
]

EFFECT_FILES = [
    ("effects/muzzle_flash.tscn",   "gen_muzzle_flash"),
    ("effects/explosion.tscn",      "gen_explosion"),
    ("effects/build_sparks.tscn",   "gen_build_sparks"),
    ("effects/teleport_flash.tscn", "gen_teleport_flash"),
]

THEME_FILE = ("ui/theme.tres", "gen_theme")


# ============================================================
#  PNG HELPERS  (standalone, no external deps)
# ============================================================

def make_png(width, height, pixels):
    """Build a PNG from RGBA pixel rows."""
    raw = b""
    for row in pixels:
        raw += b"\x00"
        for r, g, b, a in row:
            raw += bytes([r & 0xFF, g & 0xFF, b & 0xFF, a & 0xFF])
    compressed = zlib.compress(raw)

    def chunk(ct, d):
        c = ct + d
        crc = struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack(">I", len(d)) + c + crc

    out = b"\x89PNG\r\n\x1a\n"
    out += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    out += chunk(b"IDAT", compressed)
    out += chunk(b"IEND", b"")
    return out


def new_canvas(w, h, bg=(0, 0, 0, 0)):
    return [[bg for _ in range(w)] for _ in range(h)]


def _rect(px, ox, oy, x, y, w, h, color):
    """Draw filled rect at spritesheet offset (ox,oy) + local (x,y)."""
    sh = len(px)
    sw = len(px[0]) if sh else 0
    for py in range(max(0, oy + y), min(sh, oy + y + h)):
        for pxx in range(max(0, ox + x), min(sw, ox + x + w)):
            px[py][pxx] = color


def _circle(px, ox, oy, cx, cy, r, color):
    """Draw filled circle at offset (ox,oy) + local center (cx,cy)."""
    sh = len(px)
    sw = len(px[0]) if sh else 0
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                fy, fx = oy + cy + dy, ox + cx + dx
                if 0 <= fy < sh and 0 <= fx < sw:
                    px[fy][fx] = color


def _alpha(color, a):
    """Return color with modified alpha (0.0-1.0)."""
    return (color[0], color[1], color[2], max(0, min(255, int(color[3] * a))))


# ============================================================
#  SPRITESHEET CREATOR
# ============================================================

def create_spritesheet(frame_drawer):
    """Create a 256x256 PNG with 4x4 grid of 64x64 frames."""
    pixels = new_canvas(SHEET_W, SHEET_H, (0, 0, 0, 0))
    for idx in range(NUM_FRAMES):
        col = idx % SHEET_COLS
        row = idx // SHEET_COLS
        frame_drawer(pixels, col * FRAME_SIZE, row * FRAME_SIZE, idx)
    return make_png(SHEET_W, SHEET_H, pixels)


# ============================================================
#  COLOR PALETTES
# ============================================================

# Builder
B_HAT    = (240, 210, 50, 255)
B_SKIN   = (220, 180, 140, 255)
B_BODY   = (40, 200, 90, 255)
B_BODY_D = (30, 150, 70, 255)
B_TOOL   = (180, 140, 80, 255)
DARK     = (50, 50, 60, 255)
BOOT     = (70, 70, 80, 255)
SPARK    = (255, 230, 80, 255)

# Soldier
S_HELM   = (30, 50, 120, 255)
S_BODY   = (50, 90, 200, 255)
S_BODY_D = (40, 70, 160, 255)
S_WEAP   = (180, 180, 200, 255)

# PowerPlant
PP_ROOF  = (160, 150, 30, 255)
PP_BODY  = (220, 210, 60, 255)
PP_BOLT  = (255, 255, 200, 255)
PP_GLOW  = (255, 240, 100, 255)
PP_BASE  = (60, 60, 70, 255)

# Factory
F_CHIM   = (80, 40, 130, 255)
F_ROOF   = (90, 50, 140, 255)
F_BODY   = (130, 70, 190, 255)
F_GEAR   = (200, 180, 230, 255)
F_BASE   = (60, 60, 70, 255)
F_SMOKE  = (150, 150, 160, 140)


# ============================================================
#  BASE DRAW HELPERS — reusable character / structure shapes
# ============================================================

def _draw_builder(px, ox, oy, bob=0, ll_y=0, rl_y=0, rarm_y=0,
                  tool_vis=False, tool_y=0, sparks=False, a=1.0):
    """Draw builder character with configurable animation offsets."""
    _rect(px, ox, oy, 25, 10 + bob,  14, 6,  _alpha(B_HAT, a))
    _rect(px, ox, oy, 26, 16 + bob,  12, 8,  _alpha(B_SKIN, a))
    _rect(px, ox, oy, 22, 24 + bob,  20, 14, _alpha(B_BODY, a))
    _rect(px, ox, oy, 18, 25 + bob,   4, 12, _alpha(B_BODY_D, a))       # left arm
    _rect(px, ox, oy, 42, 25 + bob + rarm_y, 4, 12, _alpha(B_BODY_D, a))  # right arm
    _rect(px, ox, oy, 24, 38 + ll_y,  7, 10, _alpha(DARK, a))
    _rect(px, ox, oy, 33, 38 + rl_y,  7, 10, _alpha(DARK, a))
    _rect(px, ox, oy, 24, 44 + ll_y,  7, 4,  _alpha(BOOT, a))
    _rect(px, ox, oy, 33, 44 + rl_y,  7, 4,  _alpha(BOOT, a))
    if tool_vis:
        _rect(px, ox, oy, 44, 30 + bob + tool_y, 4, 10, _alpha(B_TOOL, a))
    if sparks:
        _rect(px, ox, oy, 44, 40 + bob + tool_y, 3, 3, SPARK)
        _rect(px, ox, oy, 48, 38 + bob + tool_y, 2, 2, SPARK)


def _draw_soldier(px, ox, oy, bob=0, ll_y=0, rl_y=0, wpn_x=0, wpn_dy=0,
                  tilt=0, a=1.0):
    """Draw soldier character with configurable animation offsets."""
    _rect(px, ox, oy, 24 + tilt, 8 + bob,  16, 10, _alpha(S_HELM, a))
    _rect(px, ox, oy, 26 + tilt, 16 + bob, 12, 8,  _alpha(B_SKIN, a))
    _rect(px, ox, oy, 22 + tilt, 24 + bob, 20, 14, _alpha(S_BODY, a))
    _rect(px, ox, oy, 18 + tilt, 25 + bob,  4, 12, _alpha(S_BODY_D, a))
    _rect(px, ox, oy, 42 + tilt, 25 + bob,  4, 12, _alpha(S_BODY_D, a))
    # Weapon
    _rect(px, ox, oy, 46 + tilt + wpn_x, 20 + bob + wpn_dy, 4, 16, _alpha(S_WEAP, a))
    # Legs
    _rect(px, ox, oy, 24 + tilt, 38 + ll_y, 7, 10, _alpha(DARK, a))
    _rect(px, ox, oy, 33 + tilt, 38 + rl_y, 7, 10, _alpha(DARK, a))
    _rect(px, ox, oy, 24 + tilt, 44 + ll_y, 7, 4,  _alpha(BOOT, a))
    _rect(px, ox, oy, 33 + tilt, 44 + rl_y, 7, 4,  _alpha(BOOT, a))


def _draw_powerplant(px, ox, oy, bolt_shift=0, glow_phase=0.0):
    """Draw power plant structure."""
    _rect(px, ox, oy, 10, 10, 44, 6,  PP_ROOF)
    _rect(px, ox, oy, 14, 16, 36, 32, PP_BODY)
    _rect(px, ox, oy, 10, 48, 44, 6,  PP_BASE)
    # Lightning bolt (zigzag)
    by = 20
    for i in range(4):
        shift = bolt_shift if i % 2 == 0 else -bolt_shift
        _rect(px, ox, oy, 28 + shift, by, 8, 5, PP_BOLT)
        by += 6
    # Glow aura
    if glow_phase > 0.5:
        _rect(px, ox, oy, 12, 18, 2, 28, _alpha(PP_GLOW, 0.5))
        _rect(px, ox, oy, 50, 18, 2, 28, _alpha(PP_GLOW, 0.5))


def _draw_factory(px, ox, oy, smoke_y=0, gear_frame=0):
    """Draw factory structure."""
    _rect(px, ox, oy, 16, 6,  8, 14, F_CHIM)
    _rect(px, ox, oy, 40, 8,  8, 12, F_CHIM)
    _rect(px, ox, oy, 12, 18, 40, 6,  F_ROOF)
    _rect(px, ox, oy, 14, 24, 36, 26, F_BODY)
    _rect(px, ox, oy, 10, 50, 44, 6,  F_BASE)
    # Gear in center
    _circle(px, ox, oy, 32, 38, 8, F_GEAR)
    _circle(px, ox, oy, 32, 38, 4, F_BODY)
    # Gear teeth (rotate based on frame)
    offsets = [(0, -9), (9, 0), (0, 9), (-9, 0)]
    start = gear_frame % 4
    for i in range(4):
        dx, dy = offsets[(start + i) % 4]
        _rect(px, ox, oy, 31 + dx, 37 + dy, 3, 3, F_GEAR)
    # Smoke
    if smoke_y != 0:
        _rect(px, ox, oy, 17, max(0, 4 - smoke_y), 6, 4, F_SMOKE)
        _rect(px, ox, oy, 41, max(0, 6 - smoke_y), 5, 3, F_SMOKE)


# ============================================================
#  FRAME DRAWERS  (one per animation, called for each frame)
# ============================================================

def _frame_builder_idle(px, ox, oy, idx):
    p = (idx / NUM_FRAMES) * 2 * math.pi
    _draw_builder(px, ox, oy, bob=int(math.sin(p) * 2))


def _frame_builder_walk(px, ox, oy, idx):
    p = (idx / NUM_FRAMES) * 2 * math.pi
    bob = int(math.sin(p * 2) * 1)
    ll = int(math.sin(p) * 3)
    rl = int(math.sin(p + math.pi) * 3)
    _draw_builder(px, ox, oy, bob=bob, ll_y=ll, rl_y=rl)


def _frame_builder_build(px, ox, oy, idx):
    p = (idx / NUM_FRAMES) * 2 * math.pi
    bob = int(math.sin(p * 2) * 1)
    arm_y = int(abs(math.sin(p)) * 8)
    tool_y = int(abs(math.sin(p)) * 6)
    do_sparks = math.sin(p) > 0.7
    _draw_builder(px, ox, oy, bob=bob, rarm_y=arm_y,
                  tool_vis=True, tool_y=tool_y, sparks=do_sparks)


def _frame_soldier_idle(px, ox, oy, idx):
    p = (idx / NUM_FRAMES) * 2 * math.pi
    _draw_soldier(px, ox, oy, bob=int(math.sin(p) * 1))


def _frame_soldier_walk(px, ox, oy, idx):
    p = (idx / NUM_FRAMES) * 2 * math.pi
    bob = int(math.sin(p * 2) * 1)
    ll = int(math.sin(p) * 3)
    rl = int(math.sin(p + math.pi) * 3)
    _draw_soldier(px, ox, oy, bob=bob, ll_y=ll, rl_y=rl)


def _frame_soldier_attack(px, ox, oy, idx):
    p = (idx / NUM_FRAMES) * 2 * math.pi
    thrust = int(max(0, math.sin(p)) * 10)
    bob = int(math.sin(p * 2) * 1)
    _draw_soldier(px, ox, oy, bob=bob, wpn_x=thrust, wpn_dy=-thrust // 2)
    # Muzzle flash on thrust peak
    if math.sin(p) > 0.85:
        _rect(px, ox, oy, 52 + thrust, 22 + bob, 5, 5, (255, 255, 180, 255))


def _frame_soldier_die(px, ox, oy, idx):
    progress = idx / max(1, NUM_FRAMES - 1)
    tilt = int(progress * 14)
    sink = int(progress * 6)
    alpha = max(0.15, 1.0 - progress * 0.85)
    _draw_soldier(px, ox, oy, bob=sink, tilt=tilt, a=alpha)


def _frame_pp_idle(px, ox, oy, idx):
    p = (idx / NUM_FRAMES) * 2 * math.pi
    _draw_powerplant(px, ox, oy, bolt_shift=0, glow_phase=0.5 + math.sin(p) * 0.3)


def _frame_pp_work(px, ox, oy, idx):
    p = (idx / NUM_FRAMES) * 2 * math.pi
    shift = int(math.sin(p) * 3)
    _draw_powerplant(px, ox, oy, bolt_shift=shift, glow_phase=0.5 + math.sin(p) * 0.5)
    # Energy particles
    if idx % 3 == 0:
        ey = 16 + (idx * 2) % 28
        _rect(px, ox, oy, 52, ey, 3, 3, PP_GLOW)


def _frame_fac_idle(px, ox, oy, idx):
    _draw_factory(px, ox, oy, smoke_y=0, gear_frame=0)


def _frame_fac_work(px, ox, oy, idx):
    p = (idx / NUM_FRAMES) * 2 * math.pi
    smoke = int((idx % 8) * 1.5)
    _draw_factory(px, ox, oy, smoke_y=smoke, gear_frame=idx)


# ============================================================
#  SPRITESHEET WRAPPER FUNCTIONS
# ============================================================

def spr_builder_idle():    return create_spritesheet(_frame_builder_idle)
def spr_builder_walk():    return create_spritesheet(_frame_builder_walk)
def spr_builder_build():   return create_spritesheet(_frame_builder_build)
def spr_soldier_idle():    return create_spritesheet(_frame_soldier_idle)
def spr_soldier_walk():    return create_spritesheet(_frame_soldier_walk)
def spr_soldier_attack():  return create_spritesheet(_frame_soldier_attack)
def spr_soldier_die():     return create_spritesheet(_frame_soldier_die)
def spr_powerplant_idle(): return create_spritesheet(_frame_pp_idle)
def spr_powerplant_work(): return create_spritesheet(_frame_pp_work)
def spr_factory_idle():    return create_spritesheet(_frame_fac_idle)
def spr_factory_work():    return create_spritesheet(_frame_fac_work)


# ============================================================
#  GDSCRIPT GENERATORS — POLISH SCRIPTS
# ============================================================

def gen_balance_data():
    """Centralized balance constants for easy tuning."""
    return '''## BalanceData
## Centralized gameplay balance constants.
## Adjust values here to tune the entire game.
extends Node

# =============== Units ===============
# Builder
const BUILDER_HP        := 80.0
const BUILDER_SPEED     := 120.0
const BUILD_COST_POWER  := 50.0
const BUILD_COST_FACTORY:= 100.0

# Soldier
const SOLDIER_HP        := 120.0
const SOLDIER_SPEED     := 160.0
const SOLDIER_DAMAGE    := 15.0
const SOLDIER_RANGE     := 80.0
const SOLDIER_COOLDOWN  := 1.0
const SOLDIER_COST      := 30.0

# =============== Structures ===============
const BASE_HP           := 600.0
const POWERPLANT_HP     := 300.0
const FACTORY_HP        := 400.0

# =============== Economy ===============
const START_ENERGY      := 100.0
const START_MINERALS    := 50.0
const ENERGY_PER_SEC    := 5.0
const PRODUCTION_TIME   := 5.0

# =============== Game Feel ===============
const SPAWN_BOUNCE_SCALE := 1.3
const SPAWN_BOUNCE_TIME  := 0.25
const DAMAGE_FLASH_TIME  := 0.1
const CAMERA_SHAKE_INTENSITY := 8.0
const CAMERA_SHAKE_DECAY := 5.0
'''


def gen_ai_tuning():
    """AI behavior parameters with difficulty scaling."""
    return '''## AITuning
## Configurable AI behavior parameters.
extends Node

# =============== Base timers ===============
const BASE_SPAWN_INTERVAL  := 8.0
const BASE_ATTACK_INTERVAL := 15.0
const INITIAL_SPAWN_DELAY  := 3.0
const INITIAL_ATTACK_DELAY := 10.0

# =============== Difficulty ===============
## Difficulty multiplier: higher = harder (more frequent spawns/attacks).
var difficulty: float = 1.0

# =============== Army limits ===============
const MAX_ENEMY_SOLDIERS := 20
const ATTACK_MIN_ARMY    := 3


func get_spawn_interval() -> float:
\treturn BASE_SPAWN_INTERVAL / difficulty


func get_attack_interval() -> float:
\treturn BASE_ATTACK_INTERVAL / difficulty


func increase_difficulty(amount: float = 0.1) -> void:
\tdifficulty = minf(difficulty + amount, 3.0)
\tprint("[AITuning] Difficulty now: ", difficulty)


func reset() -> void:
\tdifficulty = 1.0
'''


def gen_object_pool():
    """Simple node pooling system to reduce allocations."""
    return '''## ObjectPool
## Reusable node pool. Call get_node() to obtain and release_node() to return.
extends Node

# pool_key -> Array[Node]
var _pools: Dictionary = {}


func get_pooled(scene_path: String) -> Node:
\t## Get a node from pool, or instantiate a new one.
\tif _pools.has(scene_path) and not _pools[scene_path].is_empty():
\t\tvar node: Node = _pools[scene_path].pop_back()
\t\tnode.set_process(true)
\t\tnode.set_physics_process(true)
\t\tnode.visible = true
\t\treturn node
\t# No pooled instance — create fresh
\tvar packed := load(scene_path) as PackedScene
\tif packed:
\t\treturn packed.instantiate()
\treturn null


func release_pooled(node: Node, scene_path: String) -> void:
\t## Return a node to the pool instead of freeing it.
\tif not _pools.has(scene_path):
\t\t_pools[scene_path] = []
\tnode.set_process(false)
\tnode.set_physics_process(false)
\tnode.visible = false
\tif node.get_parent():
\t\tnode.get_parent().remove_child(node)
\t_pools[scene_path].append(node)


func clear_pool(scene_path: String = "") -> void:
\t## Free all pooled nodes (or all pools if no key given).
\tif scene_path != "":
\t\tif _pools.has(scene_path):
\t\t\tfor n in _pools[scene_path]:
\t\t\t\tn.queue_free()
\t\t\t_pools[scene_path].clear()
\telse:
\t\tfor key in _pools:
\t\t\tfor n in _pools[key]:
\t\t\t\tn.queue_free()
\t\t_pools.clear()
'''


def gen_animation_setup():
    """Loads sprite sheets and creates SpriteFrames at runtime."""
    return '''## AnimationSetup
## Loads 4x4 sprite sheets and creates SpriteFrames resources.
## Attach to units/structures, then call setup_animations().
extends Node

const FRAME_SIZE := 64
const SHEET_COLS := 4
const SHEET_ROWS := 4
const NUM_FRAMES := SHEET_COLS * SHEET_ROWS  # 16

# Preloaded animation data: {anim_name: sheet_path}
var _cache: Dictionary = {}


func create_sprite_frames(sheets: Dictionary, fps: float = 10.0) -> SpriteFrames:
\t## Build a SpriteFrames resource from a dict of {anim_name: sheet_path}.
\tvar sf := SpriteFrames.new()
\t# Remove the default animation
\tif sf.has_animation("default"):
\t\tsf.remove_animation("default")

\tfor anim_name in sheets:
\t\tvar path: String = sheets[anim_name]
\t\tvar tex := load(path) as Texture2D
\t\tif not tex:
\t\t\tpush_warning("[AnimSetup] Failed to load: " + path)
\t\t\tcontinue

\t\tsf.add_animation(anim_name)
\t\tsf.set_animation_speed(anim_name, fps)
\t\tsf.set_animation_loop(anim_name, true)

\t\t# Create AtlasTexture for each frame in the 4x4 grid
\t\tfor idx in range(NUM_FRAMES):
\t\t\tvar col := idx % SHEET_COLS
\t\t\tvar row := idx / SHEET_COLS
\t\t\tvar atlas := AtlasTexture.new()
\t\t\tatlas.atlas = tex
\t\t\tatlas.region = Rect2(
\t\t\t\tcol * FRAME_SIZE, row * FRAME_SIZE,
\t\t\t\tFRAME_SIZE, FRAME_SIZE
\t\t\t)
\t\t\tsf.add_frame(anim_name, atlas)

\treturn sf


func setup_unit_animations(sprite: AnimatedSprite2D, unit_type: String) -> void:
\t## Convenience: set up all animations for a given unit type.
\tvar sheets := {}
\tmatch unit_type:
\t\t"builder":
\t\t\tsheets = {
\t\t\t\t"idle":  "res://assets/spritesheets/builder_idle.png",
\t\t\t\t"walk":  "res://assets/spritesheets/builder_walk.png",
\t\t\t\t"build": "res://assets/spritesheets/builder_build.png",
\t\t\t}
\t\t"soldier":
\t\t\tsheets = {
\t\t\t\t"idle":   "res://assets/spritesheets/soldier_idle.png",
\t\t\t\t"walk":   "res://assets/spritesheets/soldier_walk.png",
\t\t\t\t"attack": "res://assets/spritesheets/soldier_attack.png",
\t\t\t\t"die":    "res://assets/spritesheets/soldier_die.png",
\t\t\t}
\tif sheets.is_empty():
\t\treturn
\tsprite.sprite_frames = create_sprite_frames(sheets)
\tsprite.play("idle")


func setup_structure_animations(sprite: AnimatedSprite2D, struct_type: String) -> void:
\t## Set up animations for a structure.
\tvar sheets := {}
\tmatch struct_type:
\t\t"powerplant":
\t\t\tsheets = {
\t\t\t\t"idle": "res://assets/spritesheets/powerplant_idle.png",
\t\t\t\t"work": "res://assets/spritesheets/powerplant_work.png",
\t\t\t}
\t\t"factory":
\t\t\tsheets = {
\t\t\t\t"idle": "res://assets/spritesheets/factory_idle.png",
\t\t\t\t"work": "res://assets/spritesheets/factory_work.png",
\t\t\t}
\tif sheets.is_empty():
\t\treturn
\tsprite.sprite_frames = create_sprite_frames(sheets, 8.0)
\tsprite.play("idle")
'''


def gen_camera_fx():
    """Camera effects: screen shake, smooth zoom, edge scrolling."""
    return '''## CameraFX
## Enhanced camera with screen shake, smooth zoom, and edge scrolling.
## Attach to a Camera2D node (or replace CameraController).
extends Camera2D

# =============== Shake ===============
var shake_intensity: float = 0.0
var shake_decay: float = 5.0

# =============== Smooth Zoom ===============
var target_zoom: Vector2 = Vector2.ONE
var zoom_lerp_speed: float = 8.0
@export var zoom_step: float = 0.1
@export var zoom_min: float = 0.3
@export var zoom_max: float = 2.0

# =============== Edge Scrolling ===============
@export var edge_scroll_enabled: bool = true
@export var edge_margin: float = 30.0
@export var pan_speed: float = 600.0


func _ready() -> void:
\ttarget_zoom = zoom


func _process(delta: float) -> void:
\t_process_shake(delta)
\t_process_smooth_zoom(delta)
\t_process_edge_scroll(delta)
\t_process_wasd(delta)
\t_process_zoom_input()


func _process_shake(delta: float) -> void:
\tif shake_intensity > 0.01:
\t\tvar rand_offset := Vector2(
\t\t\trandf_range(-shake_intensity, shake_intensity),
\t\t\trandf_range(-shake_intensity, shake_intensity)
\t\t)
\t\toffset = rand_offset
\t\tshake_intensity = lerpf(shake_intensity, 0.0, shake_decay * delta)
\telse:
\t\toffset = Vector2.ZERO
\t\tshake_intensity = 0.0


func _process_smooth_zoom(delta: float) -> void:
\tzoom = zoom.lerp(target_zoom, zoom_lerp_speed * delta)


func _process_edge_scroll(delta: float) -> void:
\tif not edge_scroll_enabled:
\t\treturn
\tvar vp_size := get_viewport_rect().size
\tvar mouse := get_viewport().get_mouse_position()
\tvar dir := Vector2.ZERO
\tif mouse.x < edge_margin:          dir.x -= 1.0
\tif mouse.x > vp_size.x - edge_margin: dir.x += 1.0
\tif mouse.y < edge_margin:          dir.y -= 1.0
\tif mouse.y > vp_size.y - edge_margin: dir.y += 1.0
\tif dir != Vector2.ZERO:
\t\tposition += dir.normalized() * pan_speed * delta


func _process_wasd(delta: float) -> void:
\tvar dir := Vector2.ZERO
\tif Input.is_action_pressed("camera_up"):    dir.y -= 1.0
\tif Input.is_action_pressed("camera_down"):  dir.y += 1.0
\tif Input.is_action_pressed("camera_left"):  dir.x -= 1.0
\tif Input.is_action_pressed("camera_right"): dir.x += 1.0
\tif dir != Vector2.ZERO:
\t\tposition += dir.normalized() * pan_speed * delta


func _process_zoom_input() -> void:
\tif Input.is_action_just_pressed("camera_zoom_in"):
\t\ttarget_zoom = (target_zoom + Vector2.ONE * zoom_step).clampf(zoom_min, zoom_max)
\tif Input.is_action_just_pressed("camera_zoom_out"):
\t\ttarget_zoom = (target_zoom - Vector2.ONE * zoom_step).clampf(zoom_min, zoom_max)


# =============== Public API ===============

func shake(intensity: float = 8.0) -> void:
\t## Trigger screen shake (e.g. on explosion).
\tshake_intensity = maxf(shake_intensity, intensity)


func zoom_to(level: float) -> void:
\ttarget_zoom = Vector2.ONE * clampf(level, zoom_min, zoom_max)
'''


def gen_ui_animator():
    """Tween-based UI animation helpers."""
    return '''## UIAnimator
## Provides static helper functions for juicy UI effects.
extends Node


static func pulse(node: Control, scale: float = 1.15, duration: float = 0.2) -> void:
\t## Quick scale-up then back to normal.
\tvar tween := node.create_tween()
\tnode.pivot_offset = node.size / 2.0
\ttween.tween_property(node, "scale", Vector2.ONE * scale, duration * 0.4)
\ttween.tween_property(node, "scale", Vector2.ONE, duration * 0.6)


static func slide_in(node: Control, from_offset: Vector2 = Vector2(-200, 0),
\t\t\t\t\t\t duration: float = 0.3) -> void:
\t## Slide node in from an offset position.
\tvar target_pos := node.position
\tnode.position = target_pos + from_offset
\tnode.modulate.a = 0.0
\tvar tween := node.create_tween().set_parallel(true)
\ttween.tween_property(node, "position", target_pos, duration).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
\ttween.tween_property(node, "modulate:a", 1.0, duration * 0.5)


static func fade_in(node: Control, duration: float = 0.25) -> void:
\tnode.modulate.a = 0.0
\tvar tween := node.create_tween()
\ttween.tween_property(node, "modulate:a", 1.0, duration)


static func fade_out(node: Control, duration: float = 0.25, free_after: bool = false) -> void:
\tvar tween := node.create_tween()
\ttween.tween_property(node, "modulate:a", 0.0, duration)
\tif free_after:
\t\ttween.tween_callback(node.queue_free)


static func bounce_spawn(node: Node2D, duration: float = 0.25) -> void:
\t## Scale bounce when a unit/structure spawns.
\tnode.scale = Vector2.ONE * 1.4
\tvar tween := node.create_tween()
\ttween.tween_property(node, "scale", Vector2.ONE, duration).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_ELASTIC)


static func damage_flash(node: Node2D, duration: float = 0.1) -> void:
\t## Flash white on damage.
\tnode.modulate = Color.WHITE * 3.0
\tvar tween := node.create_tween()
\ttween.tween_property(node, "modulate", Color.WHITE, duration)


static func float_text(parent: Node, text: String, pos: Vector2,
\t\t\t\t\t\t  color: Color = Color.YELLOW, duration: float = 0.8) -> void:
\t## Floating damage/healing number.
\tvar lbl := Label.new()
\tlbl.text = text
\tlbl.global_position = pos
\tlbl.add_theme_color_override("font_color", color)
\tlbl.z_index = 100
\tparent.add_child(lbl)
\tvar tween := lbl.create_tween().set_parallel(true)
\ttween.tween_property(lbl, "position:y", pos.y - 40, duration)
\ttween.tween_property(lbl, "modulate:a", 0.0, duration)
\ttween.chain().tween_callback(lbl.queue_free)
'''


def gen_ui_tooltips():
    """Tooltip overlay system that follows the mouse."""
    return '''## UITooltips
## Shows contextual tooltips when hovering over game elements.
extends CanvasLayer

var _panel: PanelContainer = null
var _label: Label = null
var _visible: bool = false
var _follow_mouse: bool = true


func _ready() -> void:
\tlayer = 90
\t_build_tooltip()


func _build_tooltip() -> void:
\t_panel = PanelContainer.new()
\t_panel.visible = false
\t_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
\t_panel.z_index = 200

\t_label = Label.new()
\t_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
\t_label.custom_minimum_size = Vector2(160, 0)
\t_panel.add_child(_label)
\tadd_child(_panel)


func _process(_delta: float) -> void:
\tif _visible and _follow_mouse:
\t\tvar mp := get_viewport().get_mouse_position()
\t\t_panel.global_position = mp + Vector2(16, 16)


func show_tooltip(text: String, follow: bool = true) -> void:
\t_label.text = text
\t_follow_mouse = follow
\t_panel.visible = true
\t_visible = true


func hide_tooltip() -> void:
\t_panel.visible = false
\t_visible = false


## Convenience: connect hover signals to show/hide.
func register_hover(control: Control, text: String) -> void:
\tcontrol.mouse_entered.connect(func(): show_tooltip(text))
\tcontrol.mouse_exited.connect(func(): hide_tooltip())
'''


# ============================================================
#  PARTICLE EFFECT GENERATORS (.tscn)
# ============================================================

def gen_muzzle_flash():
    """Short yellow-white burst for weapon fire."""
    return '''[gd_scene format=3 uid="uid://fx_muzzle"]

[node name="MuzzleFlash" type="CPUParticles2D"]
emitting = false
one_shot = true
amount = 10
lifetime = 0.15
speed_scale = 2.0
explosiveness = 0.95
randomness = 0.3
direction = Vector2(1, 0)
spread = 25.0
gravity = Vector2(0, 0)
initial_velocity_min = 150.0
initial_velocity_max = 280.0
scale_amount_min = 1.5
scale_amount_max = 3.0
scale_amount_curve = null
color = Color(1, 0.92, 0.35, 1)
'''


def gen_explosion():
    """Orange-red burst for destruction effects."""
    return '''[gd_scene format=3 uid="uid://fx_explosion"]

[node name="Explosion" type="Node2D"]

[node name="Fire" type="CPUParticles2D" parent="."]
emitting = false
one_shot = true
amount = 20
lifetime = 0.4
speed_scale = 1.5
explosiveness = 0.9
randomness = 0.5
direction = Vector2(0, -1)
spread = 180.0
gravity = Vector2(0, 40)
initial_velocity_min = 60.0
initial_velocity_max = 160.0
scale_amount_min = 2.0
scale_amount_max = 5.0
color = Color(1, 0.45, 0.1, 1)

[node name="Smoke" type="CPUParticles2D" parent="."]
emitting = false
one_shot = true
amount = 12
lifetime = 0.7
speed_scale = 1.0
explosiveness = 0.7
randomness = 0.6
direction = Vector2(0, -1)
spread = 120.0
gravity = Vector2(0, -20)
initial_velocity_min = 20.0
initial_velocity_max = 60.0
scale_amount_min = 3.0
scale_amount_max = 8.0
color = Color(0.35, 0.3, 0.28, 0.6)
'''


def gen_build_sparks():
    """Yellow sparks that fall with gravity during construction."""
    return '''[gd_scene format=3 uid="uid://fx_sparks"]

[node name="BuildSparks" type="CPUParticles2D"]
emitting = false
one_shot = false
amount = 8
lifetime = 0.5
speed_scale = 1.0
explosiveness = 0.3
randomness = 0.4
direction = Vector2(0, -1)
spread = 60.0
gravity = Vector2(0, 200)
initial_velocity_min = 50.0
initial_velocity_max = 120.0
scale_amount_min = 1.0
scale_amount_max = 2.0
color = Color(1, 0.85, 0.2, 1)
'''


def gen_teleport_flash():
    """Cyan-blue vertical column for stargate travel."""
    return '''[gd_scene format=3 uid="uid://fx_teleport"]

[node name="TeleportFlash" type="Node2D"]

[node name="Column" type="CPUParticles2D" parent="."]
emitting = false
one_shot = true
amount = 30
lifetime = 0.6
speed_scale = 1.2
explosiveness = 0.8
randomness = 0.3
direction = Vector2(0, -1)
spread = 10.0
gravity = Vector2(0, 0)
initial_velocity_min = 80.0
initial_velocity_max = 200.0
scale_amount_min = 1.5
scale_amount_max = 3.0
color = Color(0.2, 0.8, 1.0, 0.9)

[node name="Ring" type="CPUParticles2D" parent="."]
emitting = false
one_shot = true
amount = 16
lifetime = 0.4
speed_scale = 1.5
explosiveness = 0.95
randomness = 0.2
direction = Vector2(1, 0)
spread = 180.0
gravity = Vector2(0, 0)
initial_velocity_min = 40.0
initial_velocity_max = 100.0
scale_amount_min = 1.0
scale_amount_max = 2.5
color = Color(0.4, 0.9, 1.0, 0.7)
'''


# ============================================================
#  THEME GENERATOR (ui/theme.tres)
# ============================================================

def gen_theme():
    """Godot 4 UI theme: rounded panels, glow borders, sci-fi style."""
    return '''[gd_resource type="Theme" load_steps=6 format=3]

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_panel"]
bg_color = Color(0.08, 0.1, 0.18, 0.92)
border_width_left = 1
border_width_top = 1
border_width_right = 1
border_width_bottom = 1
border_color = Color(0.25, 0.45, 0.85, 0.55)
corner_radius_top_left = 6
corner_radius_top_right = 6
corner_radius_bottom_right = 6
corner_radius_bottom_left = 6
content_margin_left = 10.0
content_margin_top = 8.0
content_margin_right = 10.0
content_margin_bottom = 8.0
shadow_color = Color(0.0, 0.15, 0.4, 0.3)
shadow_size = 4

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_btn_normal"]
bg_color = Color(0.12, 0.15, 0.26, 0.9)
border_width_left = 1
border_width_top = 1
border_width_right = 1
border_width_bottom = 1
border_color = Color(0.3, 0.5, 0.9, 0.5)
corner_radius_top_left = 4
corner_radius_top_right = 4
corner_radius_bottom_right = 4
corner_radius_bottom_left = 4
content_margin_left = 12.0
content_margin_top = 6.0
content_margin_right = 12.0
content_margin_bottom = 6.0

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_btn_hover"]
bg_color = Color(0.16, 0.2, 0.35, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.4, 0.65, 1.0, 0.75)
corner_radius_top_left = 4
corner_radius_top_right = 4
corner_radius_bottom_right = 4
corner_radius_bottom_left = 4
content_margin_left = 12.0
content_margin_top = 6.0
content_margin_right = 12.0
content_margin_bottom = 6.0

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_btn_pressed"]
bg_color = Color(0.1, 0.25, 0.5, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.5, 0.8, 1.0, 0.9)
corner_radius_top_left = 4
corner_radius_top_right = 4
corner_radius_bottom_right = 4
corner_radius_bottom_left = 4
content_margin_left = 12.0
content_margin_top = 6.0
content_margin_right = 12.0
content_margin_bottom = 6.0

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_btn_disabled"]
bg_color = Color(0.08, 0.08, 0.12, 0.6)
border_width_left = 1
border_width_top = 1
border_width_right = 1
border_width_bottom = 1
border_color = Color(0.2, 0.2, 0.3, 0.3)
corner_radius_top_left = 4
corner_radius_top_right = 4
corner_radius_bottom_right = 4
corner_radius_bottom_left = 4
content_margin_left = 12.0
content_margin_top = 6.0
content_margin_right = 12.0
content_margin_bottom = 6.0

[resource]
PanelContainer/styles/panel = SubResource("StyleBoxFlat_panel")
Button/styles/normal = SubResource("StyleBoxFlat_btn_normal")
Button/styles/hover = SubResource("StyleBoxFlat_btn_hover")
Button/styles/pressed = SubResource("StyleBoxFlat_btn_pressed")
Button/styles/disabled = SubResource("StyleBoxFlat_btn_disabled")
Button/colors/font_color = Color(0.78, 0.85, 1.0, 1)
Button/colors/font_hover_color = Color(0.9, 0.95, 1.0, 1)
Button/colors/font_pressed_color = Color(1, 1, 1, 1)
Button/colors/font_disabled_color = Color(0.4, 0.4, 0.5, 1)
Label/colors/font_color = Color(0.8, 0.87, 1.0, 1)
'''


# ============================================================
#  PROJECT.GODOT PATCHER — add theme
# ============================================================

def patch_project_godot(project_dir):
    """Set the custom theme in project.godot."""
    godot_path = os.path.join(project_dir, "project.godot")
    if not os.path.exists(godot_path):
        print("  WARNING: project.godot not found — skipping theme patch.")
        return

    with open(godot_path, "r", encoding="utf-8") as f:
        content = f.read()

    theme_line = 'theme/custom="res://ui/theme.tres"'
    if theme_line in content:
        print("  [OK] project.godot already has custom theme.")
        return

    # Insert [gui] section before [rendering] if not present
    if "[gui]" not in content:
        if "[rendering]" in content:
            content = content.replace(
                "[rendering]",
                "[gui]\n\n" + theme_line + "\n\n[rendering]"
            )
        else:
            content += "\n[gui]\n\n" + theme_line + "\n"
    else:
        content = content.replace("[gui]", "[gui]\n\n" + theme_line)

    with open(godot_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  [OK] project.godot patched — custom theme set.")


# ============================================================
#  FILE WRITERS
# ============================================================

def write_binary(project_dir, rel_path, data):
    full = os.path.join(project_dir, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb") as f:
        f.write(data)
    return full


def write_text(project_dir, rel_path, content):
    full = os.path.join(project_dir, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return full


# ============================================================
#  MAIN
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_polish.py <project_dir>")
        sys.exit(1)

    project_dir = os.path.abspath(sys.argv[1])
    print(f"  Project directory: {project_dir}")
    print(f"  Game: {GAME_NAME}")
    print()

    # --- Generator maps ---
    spr_gens = {
        "spr_builder_idle":    spr_builder_idle,
        "spr_builder_walk":    spr_builder_walk,
        "spr_builder_build":   spr_builder_build,
        "spr_soldier_idle":    spr_soldier_idle,
        "spr_soldier_walk":    spr_soldier_walk,
        "spr_soldier_attack":  spr_soldier_attack,
        "spr_soldier_die":     spr_soldier_die,
        "spr_powerplant_idle": spr_powerplant_idle,
        "spr_powerplant_work": spr_powerplant_work,
        "spr_factory_idle":    spr_factory_idle,
        "spr_factory_work":    spr_factory_work,
    }

    script_gens = {
        "gen_balance_data":     gen_balance_data,
        "gen_ai_tuning":        gen_ai_tuning,
        "gen_object_pool":      gen_object_pool,
        "gen_animation_setup":  gen_animation_setup,
        "gen_camera_fx":        gen_camera_fx,
        "gen_ui_animator":      gen_ui_animator,
        "gen_ui_tooltips":      gen_ui_tooltips,
    }

    effect_gens = {
        "gen_muzzle_flash":   gen_muzzle_flash,
        "gen_explosion":      gen_explosion,
        "gen_build_sparks":   gen_build_sparks,
        "gen_teleport_flash": gen_teleport_flash,
    }

    generated = []

    # === 1. Animated sprite sheets ===
    print("  Generating animated sprite sheets (4x4, 64x64 per frame)...")
    for rel_path, gen_name in SPRITESHEET_FILES:
        gen_func = spr_gens.get(gen_name)
        if not gen_func:
            print(f"  WARNING: No generator '{gen_name}', skipping {rel_path}")
            continue
        data = gen_func()
        write_binary(project_dir, rel_path, data)
        generated.append(rel_path)
        print(f"  [OK] {rel_path}")

    print()

    # === 2. Polish GDScripts ===
    print("  Generating polish scripts...")
    for rel_path, gen_name in SCRIPT_FILES:
        gen_func = script_gens.get(gen_name)
        if not gen_func:
            print(f"  WARNING: No generator '{gen_name}', skipping {rel_path}")
            continue
        content = gen_func()
        write_text(project_dir, rel_path, content)
        generated.append(rel_path)
        print(f"  [OK] {rel_path}")

    print()

    # === 3. Particle effects ===
    print("  Generating particle effect scenes...")
    for rel_path, gen_name in EFFECT_FILES:
        gen_func = effect_gens.get(gen_name)
        if not gen_func:
            print(f"  WARNING: No generator '{gen_name}', skipping {rel_path}")
            continue
        content = gen_func()
        write_text(project_dir, rel_path, content)
        generated.append(rel_path)
        print(f"  [OK] {rel_path}")

    print()

    # === 4. UI Theme ===
    print("  Generating UI theme...")
    theme_path, theme_gen_name = THEME_FILE
    content = gen_theme()
    write_text(project_dir, theme_path, content)
    generated.append(theme_path)
    print(f"  [OK] {theme_path}")

    print()

    # === 5. Patch project.godot ===
    print("  Patching project.godot for custom theme...")
    patch_project_godot(project_dir)

    # --- Summary ---
    print()
    print("  ========================================")
    print(f"  POLISH PASS COMPLETE: {GAME_NAME}")
    print(f"  Sprite sheets: {len(SPRITESHEET_FILES)}")
    print(f"  Scripts:       {len(SCRIPT_FILES)}")
    print(f"  Effects:       {len(EFFECT_FILES)}")
    print(f"  Theme:         1")
    print(f"  Total:         {len(generated)} files")
    print("  + project.godot patched (custom theme)")
    print("  ========================================")
    print()
    print("  Generated files:")
    for f in generated:
        print(f"    - {f}")
    print()
    print("  Art style: top-down 2D, clean shapes, sci-fi minimalism.")
    print("  All polish systems ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
