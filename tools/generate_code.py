"""
GATE DOMINION - Code Generator
===============================
AI Role: AI_GAMEPLAY_PROGRAMMER

This script generates ALL core gameplay GDScript files for the
Gate Dominion prototype. After running this step the game has
complete logic for: galaxy map, planet RTS, units, structures,
economy, stargate travel, enemy AI, and save/load.

Usage:
    python generate_code.py <project_dir>
"""

import sys
import os


# ============================================================
#  CONFIGURATION
# ============================================================

GAME_NAME = "Gate Dominion"

# All script files to generate: (relative_path, generator_function_name)
# Paths are relative to the project directory.
SCRIPT_FILES = [
    # --- CORE ---
    ("scripts/core/game_manager.gd",        "gen_game_manager"),
    ("scripts/core/input_manager.gd",       "gen_input_manager"),
    ("scripts/core/save_manager.gd",        "gen_save_manager"),
    # --- CAMERA ---
    ("scripts/camera/camera_controller.gd", "gen_camera_controller"),
    # --- GALAXY ---
    ("scripts/galaxy/galaxy_map.gd",        "gen_galaxy_map"),
    ("scripts/galaxy/planet_node.gd",       "gen_planet_node"),
    # --- PLANET RTS ---
    ("scripts/planet/planet_map.gd",        "gen_planet_map"),
    ("scripts/planet/rts_controller.gd",    "gen_rts_controller"),
    # --- UNITS ---
    ("scripts/units/unit_base.gd",          "gen_unit_base"),
    ("scripts/units/builder_unit.gd",       "gen_builder_unit"),
    ("scripts/units/soldier_unit.gd",       "gen_soldier_unit"),
    # --- STRUCTURES ---
    ("scripts/structures/structure_base.gd","gen_structure_base"),
    ("scripts/structures/power_plant.gd",   "gen_power_plant"),
    ("scripts/structures/factory.gd",       "gen_factory"),
    # --- ECONOMY ---
    ("scripts/economy/economy_manager.gd",  "gen_economy_manager"),
    # --- STARGATE ---
    ("scripts/stargate/stargate_manager.gd","gen_stargate_manager"),
    # --- AI ---
    ("scripts/ai_enemy/enemy_ai.gd",       "gen_enemy_ai"),
]


# ============================================================
#  GDSCRIPT GENERATORS — CORE
# ============================================================

def gen_game_manager():
    """GameManager autoload — central game state controller."""
    return '''## GameManager (Autoload)
## Controls global game state: current scene, win/lose, transitions.
extends Node

# --------------- Enums ---------------
enum GameState { MAIN_MENU, GALAXY_MAP, PLANET_MAP, VICTORY, DEFEAT }

# --------------- State ---------------
var current_state: int = GameState.MAIN_MENU
var current_planet_id: int = -1
var planets_data: Array = []

# --------------- Signals ---------------
signal state_changed(new_state: int)
signal planet_entered(planet_id: int)
signal victory()
signal defeat()


func _ready() -> void:
\tprint("[GameManager] Initialized.")
\t_init_planets()


# --------------- Planet data ---------------

func _init_planets() -> void:
\t## Create default galaxy with a few planets.
\tplanets_data = [
\t\t{"id": 0, "name": "Terra Prime",  "pos": Vector2(200, 300), "owner": "player"},
\t\t{"id": 1, "name": "Kesh\\'ra",     "pos": Vector2(500, 200), "owner": "enemy"},
\t\t{"id": 2, "name": "Novalith",     "pos": Vector2(800, 350), "owner": "neutral"},
\t]


# --------------- State transitions ---------------

func change_state(new_state: int) -> void:
\tcurrent_state = new_state
\tstate_changed.emit(new_state)
\tprint("[GameManager] State -> ", GameState.keys()[new_state])


func enter_planet(planet_id: int) -> void:
\t## Transition from galaxy map to planet RTS.
\tcurrent_planet_id = planet_id
\tplanet_entered.emit(planet_id)
\tchange_state(GameState.PLANET_MAP)
\tget_tree().change_scene_to_file("res://scenes/planet/planet_map.tscn")


func return_to_galaxy() -> void:
\tcurrent_planet_id = -1
\tchange_state(GameState.GALAXY_MAP)
\tget_tree().change_scene_to_file("res://scenes/galaxy/galaxy_map.tscn")


func trigger_victory() -> void:
\tchange_state(GameState.VICTORY)
\tvictory.emit()
\tprint("[GameManager] === VICTORY ===")


func trigger_defeat() -> void:
\tchange_state(GameState.DEFEAT)
\tdefeat.emit()
\tprint("[GameManager] === DEFEAT ===")


func go_to_main_menu() -> void:
\tchange_state(GameState.MAIN_MENU)
\tget_tree().change_scene_to_file("res://scenes/main_menu.tscn")
'''


def gen_input_manager():
    """InputManager — thin wrapper that translates raw input to game actions."""
    return '''## InputManager
## Provides helper functions for querying game-specific input.
## Attach to any node that needs input or use as a static reference.
extends Node

# --------------- Signals ---------------
signal select_pressed(position: Vector2)
signal command_pressed(position: Vector2)


func _unhandled_input(event: InputEvent) -> void:
\tif event.is_action_pressed("select"):
\t\tselect_pressed.emit(get_viewport().get_mouse_position())
\tif event.is_action_pressed("command"):
\t\tcommand_pressed.emit(get_viewport().get_mouse_position())


# --------------- Camera direction helpers ---------------

static func get_camera_direction() -> Vector2:
\t## Returns normalized WASD direction vector.
\tvar dir := Vector2.ZERO
\tif Input.is_action_pressed("camera_up"):    dir.y -= 1.0
\tif Input.is_action_pressed("camera_down"):  dir.y += 1.0
\tif Input.is_action_pressed("camera_left"):  dir.x -= 1.0
\tif Input.is_action_pressed("camera_right"): dir.x += 1.0
\treturn dir.normalized()


static func get_zoom_input() -> float:
\t## Returns +1 for zoom in, -1 for zoom out, 0 for none.
\tif Input.is_action_just_pressed("camera_zoom_in"):  return 1.0
\tif Input.is_action_just_pressed("camera_zoom_out"): return -1.0
\treturn 0.0
'''


def gen_save_manager():
    """SaveManager autoload — simple JSON save/load."""
    return '''## SaveManager (Autoload)
## Handles saving and loading game state to a JSON file.
extends Node

const SAVE_PATH := "user://gate_dominion_save.json"


func _ready() -> void:
\tprint("[SaveManager] Initialized.")


# --------------- Save ---------------

func save_game() -> void:
\tvar data := {
\t\t"current_planet": GameManager.current_planet_id,
\t\t"energy": EconomyManager.energy,
\t\t"minerals": EconomyManager.minerals,
\t\t"planets": GameManager.planets_data,
\t}
\tvar file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
\tif file:
\t\tfile.store_string(JSON.stringify(data, "\\t"))
\t\tfile.close()
\t\tprint("[SaveManager] Game saved.")


# --------------- Load ---------------

func load_game() -> bool:
\tif not FileAccess.file_exists(SAVE_PATH):
\t\tprint("[SaveManager] No save file found.")
\t\treturn false
\tvar file := FileAccess.open(SAVE_PATH, FileAccess.READ)
\tif not file:
\t\treturn false
\tvar json := JSON.new()
\tvar err := json.parse(file.get_as_text())
\tfile.close()
\tif err != OK:
\t\tprint("[SaveManager] Failed to parse save file.")
\t\treturn false
\tvar data: Dictionary = json.data
\tGameManager.current_planet_id = int(data.get("current_planet", -1))
\tEconomyManager.energy   = float(data.get("energy", 0.0))
\tEconomyManager.minerals = float(data.get("minerals", 0.0))
\tif data.has("planets"):
\t\tGameManager.planets_data = data["planets"]
\tprint("[SaveManager] Game loaded.")
\treturn true


# --------------- Delete ---------------

func delete_save() -> void:
\tif FileAccess.file_exists(SAVE_PATH):
\t\tDirAccess.remove_absolute(SAVE_PATH)
\t\tprint("[SaveManager] Save deleted.")
'''


# ============================================================
#  GDSCRIPT GENERATORS — CAMERA
# ============================================================

def gen_camera_controller():
    """CameraController — WASD pan + mouse-wheel zoom for 2D."""
    return '''## CameraController
## Handles WASD panning and mouse-wheel zoom on the Planet Map.
extends Camera2D

# --------------- Settings ---------------
@export var pan_speed: float = 600.0
@export var zoom_speed: float = 0.1
@export var zoom_min: float = 0.3
@export var zoom_max: float = 2.0


func _process(delta: float) -> void:
\t_handle_pan(delta)
\t_handle_zoom()


func _handle_pan(delta: float) -> void:
\tvar dir := Vector2.ZERO
\tif Input.is_action_pressed("camera_up"):    dir.y -= 1.0
\tif Input.is_action_pressed("camera_down"):  dir.y += 1.0
\tif Input.is_action_pressed("camera_left"):  dir.x -= 1.0
\tif Input.is_action_pressed("camera_right"): dir.x += 1.0
\tposition += dir.normalized() * pan_speed * delta


func _handle_zoom() -> void:
\tif Input.is_action_just_pressed("camera_zoom_in"):
\t\tzoom = (zoom + Vector2.ONE * zoom_speed).clampf(zoom_min, zoom_max)
\tif Input.is_action_just_pressed("camera_zoom_out"):
\t\tzoom = (zoom - Vector2.ONE * zoom_speed).clampf(zoom_min, zoom_max)


## Helper — clamp both x and y of a Vector2 to (lo, hi).
func _clamp_vec2(v: Vector2, lo: float, hi: float) -> Vector2:
\treturn Vector2(clampf(v.x, lo, hi), clampf(v.y, lo, hi))
'''


# ============================================================
#  GDSCRIPT GENERATORS — GALAXY
# ============================================================

def gen_galaxy_map():
    """GalaxyMap — shows planets as buttons; clicking enters planet."""
    return '''## GalaxyMap
## Displays the galaxy view with clickable planet buttons.
extends Control


func _ready() -> void:
\tGameManager.change_state(GameManager.GameState.GALAXY_MAP)
\t_build_galaxy_ui()


func _build_galaxy_ui() -> void:
\t## Dynamically create a button for each planet.
\tfor planet in GameManager.planets_data:
\t\tvar btn := Button.new()
\t\tbtn.text = planet["name"]
\t\tbtn.position = planet["pos"]
\t\tbtn.custom_minimum_size = Vector2(120, 40)

\t\t# Color-code by owner
\t\tvar owner: String = planet.get("owner", "neutral")
\t\tif owner == "player":
\t\t\tbtn.modulate = Color(0.3, 0.8, 1.0)   # Cyan
\t\telif owner == "enemy":
\t\t\tbtn.modulate = Color(1.0, 0.3, 0.3)    # Red
\t\telse:
\t\t\tbtn.modulate = Color(0.7, 0.7, 0.7)    # Gray

\t\tvar pid: int = planet["id"]
\t\tbtn.pressed.connect(_on_planet_pressed.bind(pid))
\t\tadd_child(btn)

\t# Back to menu button
\tvar back_btn := Button.new()
\tback_btn.text = "Menu"
\tback_btn.position = Vector2(20, 20)
\tback_btn.pressed.connect(func(): GameManager.go_to_main_menu())
\tadd_child(back_btn)


func _on_planet_pressed(planet_id: int) -> void:
\tprint("[GalaxyMap] Entering planet ", planet_id)
\tGameManager.enter_planet(planet_id)
'''


def gen_planet_node():
    """PlanetNode — data container for a single planet (used by galaxy)."""
    return '''## PlanetNode
## Lightweight data wrapper for a planet shown in the galaxy.
extends Node2D

var planet_id: int = -1
var planet_name: String = ""
var owner: String = "neutral"  # "player", "enemy", "neutral"


func setup(data: Dictionary) -> void:
\tplanet_id   = data.get("id", -1)
\tplanet_name = data.get("name", "Unknown")
\towner       = data.get("owner", "neutral")
\tif data.has("pos"):
\t\tposition = data["pos"]
'''


# ============================================================
#  GDSCRIPT GENERATORS — PLANET RTS
# ============================================================

def gen_planet_map():
    """PlanetMap — root node for the RTS battlefield on a planet."""
    return '''## PlanetMap
## Root scene script for the planet-level RTS gameplay.
extends Node2D

# References (assigned in _ready or by scene tree)
var rts_controller: Node = null
var enemy_ai: Node = null

# Planet context
var planet_id: int = -1

# Base references
var player_base: Node2D = null
var enemy_base: Node2D = null


func _ready() -> void:
\tplanet_id = GameManager.current_planet_id
\tprint("[PlanetMap] Loaded planet ", planet_id)

\t# --- Fullscreen background (CanvasLayer behind everything) ---
\tvar bg_layer = CanvasLayer.new()
\tbg_layer.layer = -10
\tadd_child(bg_layer)
\tvar bg_rect = ColorRect.new()
\tbg_rect.color = Color(0.04, 0.06, 0.1, 1)
\tbg_rect.set_anchors_preset(Control.PRESET_FULL_RECT)
\tbg_layer.add_child(bg_rect)

\t# --- Camera ---
\tvar cam = Camera2D.new()
\tcam.set_script(load("res://scripts/camera/camera_controller.gd"))
\tcam.position = Vector2(550, 400)
\tcam.make_current()
\tadd_child(cam)

\t# --- RTS Controller ---
\trts_controller = Node.new()
\trts_controller.name = "RTSController"
\trts_controller.set_script(load("res://scripts/planet/rts_controller.gd"))
\tadd_child(rts_controller)

\t# --- Economy tick ---
\t# EconomyManager is autoload, it ticks automatically.

\t# --- Spawn player base ---
\t_spawn_player_base()

\t# --- Enemy AI ---
\tenemy_ai = Node.new()
\tenemy_ai.name = "EnemyAI"
\tenemy_ai.set_script(load("res://scripts/ai_enemy/enemy_ai.gd"))
\tadd_child(enemy_ai)

\t# --- HUD overlay ---
\t_create_hud()


# --------------- Spawning ---------------

func _spawn_player_base() -> void:
\t## Create the player starting base (a simple structure).
\tvar base_scene = _create_structure("PlayerBase", Vector2(200, 400), true)
\tplayer_base = base_scene
\t# Give the player a builder unit
\tvar builder = _create_unit("builder", Vector2(260, 420), true)
\tif rts_controller:
\t\trts_controller.register_unit(builder)


func _create_structure(struct_name: String, pos: Vector2, is_player: bool) -> Node2D:
\t## Quickly instantiate a structure node with StructureBase script.
\tvar node := Node2D.new()
\tnode.name = struct_name
\tnode.position = pos
\tnode.set_script(load("res://scripts/structures/structure_base.gd"))
\tadd_child(node)
\tnode.call("setup", struct_name, 500, is_player)
\treturn node


func _create_unit(unit_type: String, pos: Vector2, is_player: bool) -> Node2D:
\t## Create a unit node by type.
\tvar node := Node2D.new()
\tnode.position = pos

\tvar script_path := ""
\tmatch unit_type:
\t\t"builder":
\t\t\tscript_path = "res://scripts/units/builder_unit.gd"
\t\t\tnode.name = "Builder"
\t\t"soldier":
\t\t\tscript_path = "res://scripts/units/soldier_unit.gd"
\t\t\tnode.name = "Soldier"
\t\t_:
\t\t\tscript_path = "res://scripts/units/unit_base.gd"
\t\t\tnode.name = "Unit"

\tnode.set_script(load(script_path))
\tadd_child(node)
\tnode.call("setup", is_player)
\treturn node


# --------------- HUD ---------------

func _create_hud() -> void:
\tvar canvas := CanvasLayer.new()
\tcanvas.name = "HUD"
\tadd_child(canvas)

\t# === DUNE 2000 STYLE RIGHT SIDEBAR ===
\tvar sidebar := PanelContainer.new()
\tsidebar.name = "Sidebar"
\tvar sb := StyleBoxFlat.new()
\tsb.bg_color = Color(0.04, 0.05, 0.1, 0.92)
\tsb.border_color = Color(0.12, 0.28, 0.5, 0.7)
\tsb.border_width_left = 2
\tsb.border_width_right = 0
\tsb.border_width_top = 0
\tsb.border_width_bottom = 0
\tsb.set_content_margin_all(8)
\tsidebar.add_theme_stylebox_override("panel", sb)
\tsidebar.set_anchors_preset(Control.PRESET_RIGHT_WIDE)
\tsidebar.offset_left = -210.0
\tcanvas.add_child(sidebar)

\tvar main_vbox := VBoxContainer.new()
\tmain_vbox.add_theme_constant_override("separation", 6)
\tsidebar.add_child(main_vbox)

\t# --- STARGATE COMMAND Header ---
\tvar header := Label.new()
\theader.text = "SGC COMMAND"
\theader.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
\theader.add_theme_color_override("font_color", Color(0.4, 0.7, 0.95))
\theader.add_theme_font_size_override("font_size", 14)
\tmain_vbox.add_child(header)

\tvar sep0 := HSeparator.new()
\tmain_vbox.add_child(sep0)

\t# --- Resources ---
\tvar res_lbl := Label.new()
\tres_lbl.text = "RESOURCES"
\tres_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
\tres_lbl.add_theme_color_override("font_color", Color(0.5, 0.55, 0.65))
\tres_lbl.add_theme_font_size_override("font_size", 10)
\tmain_vbox.add_child(res_lbl)

\tvar e_row := HBoxContainer.new()
\tmain_vbox.add_child(e_row)
\tvar e_icon := ColorRect.new()
\te_icon.custom_minimum_size = Vector2(12, 12)
\te_icon.color = Color(0.0, 0.85, 0.6)
\te_row.add_child(e_icon)
\tvar lbl := Label.new()
\tlbl.name = "EnergyLabel"
\tlbl.text = " Energy: 100"
\tlbl.add_theme_color_override("font_color", Color(0.0, 0.9, 0.65))
\te_row.add_child(lbl)

\tvar m_row := HBoxContainer.new()
\tmain_vbox.add_child(m_row)
\tvar m_icon := ColorRect.new()
\tm_icon.custom_minimum_size = Vector2(12, 12)
\tm_icon.color = Color(0.3, 0.65, 0.95)
\tm_row.add_child(m_icon)
\tvar mlbl := Label.new()
\tmlbl.name = "MineralsLabel"
\tmlbl.text = " Minerals: 50"
\tmlbl.add_theme_color_override("font_color", Color(0.35, 0.7, 1.0))
\tm_row.add_child(mlbl)

\tvar sep1 := HSeparator.new()
\tmain_vbox.add_child(sep1)

\t# --- Build Section ---
\tvar build_lbl := Label.new()
\tbuild_lbl.text = "CONSTRUCTION"
\tbuild_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
\tbuild_lbl.add_theme_color_override("font_color", Color(0.5, 0.55, 0.65))
\tbuild_lbl.add_theme_font_size_override("font_size", 10)
\tmain_vbox.add_child(build_lbl)

\t_add_styled_btn(main_vbox, "Naquadah Reactor", func(): _start_build("power_plant"))
\t_add_styled_btn(main_vbox, "Assembly Bay", func(): _start_build("factory"))
\t_add_styled_btn(main_vbox, "Train Marine", func(): _train_soldier())

\tvar sep2 := HSeparator.new()
\tmain_vbox.add_child(sep2)

\t# --- Navigation ---
\tvar nav_lbl := Label.new()
\tnav_lbl.text = "NAVIGATION"
\tnav_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
\tnav_lbl.add_theme_color_override("font_color", Color(0.5, 0.55, 0.65))
\tnav_lbl.add_theme_font_size_override("font_size", 10)
\tmain_vbox.add_child(nav_lbl)

\t_add_styled_btn(main_vbox, "Stargate (Galaxy)", func(): GameManager.return_to_galaxy())

\t# --- Build Menu ---
\tvar build_lbl := Label.new()
\tbuild_lbl.text = "== BUILD =="
\tbuild_lbl.position = Vector2(10, 110)
\tcanvas.add_child(build_lbl)

\tvar pp_btn := Button.new()
\tpp_btn.text = "Power Plant (50E)"
\tpp_btn.position = Vector2(10, 135)
\tpp_btn.pressed.connect(func(): _start_build("power_plant"))
\tcanvas.add_child(pp_btn)

\tvar fac_btn := Button.new()
\tfac_btn.text = "Factory (100E)"
\tfac_btn.position = Vector2(10, 170)
\tfac_btn.pressed.connect(func(): _start_build("factory"))
\tcanvas.add_child(fac_btn)

\tvar sol_btn := Button.new()
\tsol_btn.text = "Train Soldier (30E)"
\tsol_btn.position = Vector2(10, 205)
\tsol_btn.pressed.connect(func(): _train_soldier())
\tcanvas.add_child(sol_btn)

\t# Victory / Defeat label (hidden by default)
\tvar result_lbl := Label.new()
\tresult_lbl.name = "ResultLabel"
\tresult_lbl.position = Vector2(500, 300)
\tresult_lbl.visible = false
\tcanvas.add_child(result_lbl)

\tGameManager.victory.connect(func(): _show_result("VICTORY!"))
\tGameManager.defeat.connect(func(): _show_result("DEFEAT!"))



func _add_styled_btn(parent: Node, text: String, callback: Callable) -> void:
\tvar btn := Button.new()
\tbtn.text = text
\tbtn.custom_minimum_size = Vector2(180, 30)
\tvar sb := StyleBoxFlat.new()
\tsb.bg_color = Color(0.08, 0.12, 0.22)
\tsb.border_color = Color(0.25, 0.5, 0.85, 0.5)
\tsb.set_border_width_all(1)
\tsb.set_corner_radius_all(4)
\tbtn.add_theme_stylebox_override("normal", sb)
\tvar sbh := StyleBoxFlat.new()
\tsbh.bg_color = Color(0.12, 0.2, 0.35)
\tsbh.border_color = Color(0.35, 0.65, 1.0, 0.8)
\tsbh.set_border_width_all(1)
\tsbh.set_corner_radius_all(4)
\tbtn.add_theme_stylebox_override("hover", sbh)
\tbtn.pressed.connect(callback)
\tparent.add_child(btn)


func _show_result(text: String) -> void:
\tvar lbl = get_node_or_null("HUD/ResultLabel")
\tif lbl:
\t\tlbl.text = text
\t\tlbl.visible = true


func _start_build(type: String) -> void:
\tvar rts = get_node_or_null("RTSController")
\tif rts:
\t\trts.call("start_build", type)
\t\tprint("[PlanetMap] Build mode: ", type)


func _train_soldier() -> void:
\tvar factories = get_tree().get_nodes_in_group("player_structures")
\tfor f in factories:
\t\tif f.name.begins_with("Factory") and f.has_method("_on_produce_pressed"):
\t\t\tf.call("_on_produce_pressed")
\t\t\treturn
\tprint("[PlanetMap] No factory available!")


func _draw() -> void:
\t# Alien desert floor
\tdraw_rect(Rect2(Vector2(-400, -300), Vector2(2000, 1400)), Color(0.1, 0.08, 0.06, 0.5))
\t# Tech grid (Stargate-style subtle)
\tvar gc = Color(0.08, 0.15, 0.25, 0.18)
\tfor x in range(-200, 1400, 80):
\t\tdraw_line(Vector2(x, -200), Vector2(x, 1000), gc, 1.0)
\tfor y in range(-200, 1000, 80):
\t\tdraw_line(Vector2(-200, y), Vector2(1400, y), gc, 1.0)
\t# Naquadah deposits (teal glow)
\t_draw_naquadah(Vector2(400, 280), 22)
\t_draw_naquadah(Vector2(680, 520), 18)
\t_draw_naquadah(Vector2(280, 560), 15)
\t# Rock formations
\t_draw_rock(Vector2(100, 180), 32)
\t_draw_rock(Vector2(780, 130), 28)
\t_draw_rock(Vector2(520, 680), 22)
\t_draw_rock(Vector2(1020, 320), 38)
\t_draw_rock(Vector2(950, 550), 25)
\t# Stargate ring marker
\tvar sg_c = Color(0.18, 0.45, 0.75, 0.12)
\tdraw_arc(Vector2(550, 400), 45, 0, TAU, 32, sg_c, 2.5, true)
\tdraw_arc(Vector2(550, 400), 38, 0, TAU, 32, Color(0.12, 0.35, 0.65, 0.08), 1.5, true)
\t# Chevron dots on stargate marker
\tfor i in range(9):
\t\tvar a = i * TAU / 9.0 - PI / 2.0
\t\tvar cp = Vector2(550, 400) + Vector2(cos(a), sin(a)) * 42
\t\tdraw_circle(cp, 2.5, Color(0.3, 0.6, 0.9, 0.2))


func _draw_naquadah(pos: Vector2, radius: float) -> void:
\tdraw_circle(pos, radius, Color(0.0, 0.55, 0.4, 0.22))
\tdraw_circle(pos, radius * 0.55, Color(0.0, 0.7, 0.5, 0.25))
\tdraw_arc(pos, radius, 0, TAU, 16, Color(0.0, 0.8, 0.55, 0.18), 1.5, true)


func _draw_rock(pos: Vector2, size: float) -> void:
\tdraw_circle(pos, size, Color(0.12, 0.1, 0.08, 0.45))
\tdraw_circle(pos + Vector2(-size * 0.15, -size * 0.15), size * 0.65, Color(0.16, 0.13, 0.1, 0.35))
\tdraw_arc(pos, size, 0.3, 2.5, 8, Color(0.2, 0.16, 0.12, 0.2), 1.5, true)


func _process(_delta: float) -> void:
\t# Update HUD labels
\tvar hud_node = get_node_or_null("HUD")
\tif hud_node:
\t\tvar elbl = hud_node.find_child("EnergyLabel", true, false)
\t\tif elbl:
\t\t\telbl.text = " Energy: " + str(int(EconomyManager.energy))
\t\tvar mlbl = hud_node.find_child("MineralsLabel", true, false)
\t\tif mlbl:
\t\t\tmlbl.text = " Minerals: " + str(int(EconomyManager.minerals))

\t# Check win/lose
\t_check_victory_conditions()
\tqueue_redraw()


func _check_victory_conditions() -> void:
\tif GameManager.current_state == GameManager.GameState.VICTORY:
\t\treturn
\tif GameManager.current_state == GameManager.GameState.DEFEAT:
\t\treturn
\tif enemy_base and not is_instance_valid(enemy_base):
\t\tGameManager.trigger_victory()
\tif player_base and not is_instance_valid(player_base):
\t\tGameManager.trigger_defeat()
'''


def gen_rts_controller():
    """RTSController — handles unit selection and right-click commands."""
    return '''## RTSController
## Manages player unit selection and issuing commands (move/attack).
extends Node

var selected_unit: Node2D = null
var units: Array[Node2D] = []

# Build ghost state
var build_mode: bool = false
var build_type: String = ""


func _ready() -> void:
\tprint("[RTSController] Ready.")


func register_unit(unit: Node2D) -> void:
\tunits.append(unit)


func _unhandled_input(event: InputEvent) -> void:
\t# --- Left click: select unit ---
\tif event.is_action_pressed("select"):
\t\tif build_mode:
\t\t\t_place_building(get_viewport().get_mouse_position())
\t\telse:
\t\t\t_try_select(get_viewport().get_mouse_position())

\t# --- Right click: command (move or attack) ---
\tif event.is_action_pressed("command"):
\t\tif build_mode:
\t\t\t_cancel_build()
\t\telif selected_unit and is_instance_valid(selected_unit):
\t\t\tvar target_pos = _screen_to_world(get_viewport().get_mouse_position())
\t\t\t_issue_command(target_pos)


# --------------- Selection ---------------

func _try_select(screen_pos: Vector2) -> void:
\tvar world_pos = _screen_to_world(screen_pos)
\tvar best: Node2D = null
\tvar best_dist: float = 60.0  # selection radius in world pixels

\tfor unit in units:
\t\tif not is_instance_valid(unit):
\t\t\tcontinue
\t\tvar d: float = unit.global_position.distance_to(world_pos)
\t\tif d < best_dist:
\t\t\tbest_dist = d
\t\t\tbest = unit

\tif best:
\t\tselected_unit = best
\t\tprint("[RTS] Selected: ", best.name)
\telse:
\t\tselected_unit = null


# --------------- Commands ---------------

func _issue_command(world_pos: Vector2) -> void:
\tif not selected_unit or not is_instance_valid(selected_unit):
\t\treturn

\t# Check if there is an enemy near the target position
\tvar enemy = _find_enemy_near(world_pos, 50.0)
\tif enemy and selected_unit.has_method("attack_target"):
\t\tselected_unit.call("attack_target", enemy)
\t\tprint("[RTS] Attack order on ", enemy.name)
\telif selected_unit.has_method("move_to"):
\t\tselected_unit.call("move_to", world_pos)
\t\tprint("[RTS] Move order to ", world_pos)


func _find_enemy_near(pos: Vector2, radius: float) -> Node2D:
\t## Simple proximity check against all nodes in 'enemies' group.
\tvar enemies = get_tree().get_nodes_in_group("enemies")
\tfor e in enemies:
\t\tif is_instance_valid(e) and e.global_position.distance_to(pos) < radius:
\t\t\treturn e
\treturn null


# --------------- Building ---------------

func start_build(type: String) -> void:
\t## Called by BuilderUnit when player wants to build.
\tbuild_mode = true
\tbuild_type = type
\tprint("[RTS] Build mode: ", type, " — click to place.")


func _cancel_build() -> void:
\tbuild_mode = false
\tbuild_type = ""
\tprint("[RTS] Build cancelled.")


func _place_building(screen_pos: Vector2) -> void:
\tvar world_pos = _screen_to_world(screen_pos)
\tif not selected_unit or not is_instance_valid(selected_unit):
\t\t_cancel_build()
\t\treturn
\tif selected_unit.has_method("build_structure"):
\t\tselected_unit.call("build_structure", build_type, world_pos)
\tbuild_mode = false
\tbuild_type = ""


# --------------- Coordinate helpers ---------------

func _screen_to_world(screen_pos: Vector2) -> Vector2:
\tvar camera := get_viewport().get_camera_2d()
\tif camera:
\t\t# Convert screen position to world position using camera transform
\t\tvar canvas_transform = get_viewport().get_canvas_transform()
\t\treturn canvas_transform.affine_inverse() * screen_pos
\treturn screen_pos
'''


# ============================================================
#  GDSCRIPT GENERATORS — UNITS
# ============================================================

def gen_unit_base():
    """UnitBase — base class for all units (movement, health, teams)."""
    return '''## UnitBase — Tau'ri / Goa'uld ground unit
extends Node2D

@export var max_hp: float = 100.0
@export var move_speed: float = 150.0

var hp: float = 100.0
var is_player: bool = true
var target_position: Vector2 = Vector2.ZERO
var is_moving: bool = false
var unit_radius: float = 14.0


func setup(player: bool) -> void:
\tis_player = player
\thp = max_hp
\ttarget_position = position
\tif is_player:
\t\tadd_to_group("player_units")
\telse:
\t\tadd_to_group("enemies")


func _draw() -> void:
\t# Shadow
\tdraw_circle(Vector2(2, 2), unit_radius, Color(0, 0, 0, 0.45))
\t# Outer armor ring
\tvar armor = Color(0.18, 0.3, 0.45) if is_player else Color(0.5, 0.38, 0.12)
\tdraw_circle(Vector2.ZERO, unit_radius, armor)
\t# Inner core
\tvar core = Color(0.22, 0.4, 0.58) if is_player else Color(0.7, 0.52, 0.18)
\tdraw_circle(Vector2.ZERO, unit_radius * 0.65, core)
\t# Team accent stripe
\tvar accent = Color(0.15, 0.55, 0.85) if is_player else Color(0.85, 0.6, 0.12)
\tdraw_line(Vector2(-unit_radius * 0.6, 0), Vector2(unit_radius * 0.6, 0), accent, 2.0, true)
\t# Tech border
\tvar border_c = Color(0.3, 0.5, 0.7, 0.5) if is_player else Color(0.8, 0.6, 0.2, 0.5)
\tdraw_arc(Vector2.ZERO, unit_radius + 0.5, 0, TAU, 24, border_c, 1.5, true)
\t_draw_hp_bar()


func _draw_hp_bar() -> void:
\tvar w := 26.0
\tvar h := 3.0
\tvar p := Vector2(-w / 2.0, -unit_radius - 8.0)
\tdraw_rect(Rect2(p, Vector2(w, h)), Color(0.02, 0.03, 0.06, 0.9))
\tvar r := clampf(hp / max_hp, 0.0, 1.0)
\tvar c: Color
\tif r > 0.6:
\t\tc = Color(0.1, 0.8, 0.25)
\telif r > 0.3:
\t\tc = Color(0.85, 0.75, 0.1)
\telse:
\t\tc = Color(0.9, 0.12, 0.08)
\tdraw_rect(Rect2(p, Vector2(w * r, h)), c)
\tdraw_rect(Rect2(p, Vector2(w, h)), Color(0.35, 0.45, 0.55, 0.35), false)


func move_to(target: Vector2) -> void:
\ttarget_position = target
\tis_moving = true


func _process(delta: float) -> void:
\tif is_moving:
\t\tvar direction = (target_position - position).normalized()
\t\tvar distance = position.distance_to(target_position)
\t\tif distance < 5.0:
\t\t\tis_moving = false
\t\telse:
\t\t\tposition += direction * move_speed * delta
\tqueue_redraw()


func take_damage(amount: float) -> void:
\thp -= amount
\tif hp <= 0.0:
\t\tprint("[Unit] ", name, " destroyed.")
\t\tqueue_free()
'''


def gen_builder_unit():
    """BuilderUnit — can build PowerPlant and Factory structures."""
    return '''## BuilderUnit — Tau'ri Combat Engineer
extends Node2D

@export var max_hp: float = 80.0
@export var move_speed: float = 120.0

var hp: float = 80.0
var is_player: bool = true
var target_position: Vector2 = Vector2.ZERO
var is_moving: bool = false
var unit_radius: float = 16.0

const BUILD_COSTS := {
\t"power_plant": 50.0,
\t"factory": 100.0,
}


func setup(player: bool) -> void:
\tis_player = player
\thp = max_hp
\ttarget_position = position
\tif is_player:
\t\tadd_to_group("player_units")
\telse:
\t\tadd_to_group("enemies")


func _draw() -> void:
\tdraw_circle(Vector2(2, 2), unit_radius, Color(0, 0, 0, 0.45))
\t# Green-tinted military
\tvar armor = Color(0.12, 0.35, 0.22) if is_player else Color(0.45, 0.32, 0.1)
\tdraw_circle(Vector2.ZERO, unit_radius, armor)
\tvar core = Color(0.18, 0.5, 0.32) if is_player else Color(0.6, 0.42, 0.15)
\tdraw_circle(Vector2.ZERO, unit_radius * 0.6, core)
\t# Wrench cross
\tvar tc = Color(0.75, 0.8, 0.65, 0.9)
\tdraw_line(Vector2(-5, -5), Vector2(5, 5), tc, 2.5, true)
\tdraw_line(Vector2(-5, 5), Vector2(5, -5), tc, 2.5, true)
\tdraw_circle(Vector2.ZERO, 2.5, Color(0.85, 0.9, 0.75, 0.5))
\tvar border_c = Color(0.25, 0.55, 0.35, 0.5) if is_player else Color(0.7, 0.5, 0.2, 0.5)
\tdraw_arc(Vector2.ZERO, unit_radius + 0.5, 0, TAU, 24, border_c, 1.5, true)
\t_draw_hp_bar()


func _draw_hp_bar() -> void:
\tvar w := 30.0
\tvar h := 3.0
\tvar p := Vector2(-w / 2.0, -unit_radius - 8.0)
\tdraw_rect(Rect2(p, Vector2(w, h)), Color(0.02, 0.03, 0.06, 0.9))
\tvar r := clampf(hp / max_hp, 0.0, 1.0)
\tvar c := Color(0.1, 0.8, 0.25) if r > 0.6 else (Color(0.85, 0.75, 0.1) if r > 0.3 else Color(0.9, 0.12, 0.08))
\tdraw_rect(Rect2(p, Vector2(w * r, h)), c)
\tdraw_rect(Rect2(p, Vector2(w, h)), Color(0.35, 0.45, 0.55, 0.35), false)


func move_to(target: Vector2) -> void:
\ttarget_position = target
\tis_moving = true


func _process(delta: float) -> void:
\tif is_moving:
\t\tvar direction = (target_position - position).normalized()
\t\tvar distance = position.distance_to(target_position)
\t\tif distance < 5.0:
\t\t\tis_moving = false
\t\telse:
\t\t\tposition += direction * move_speed * delta
\tqueue_redraw()


func request_build(build_type: String) -> void:
\tvar rts = get_node_or_null("/root/PlanetMap/RTSController")
\tif rts:
\t\trts.call("start_build", build_type)


func build_structure(build_type: String, world_pos: Vector2) -> void:
\tvar cost: float = BUILD_COSTS.get(build_type, 999.0)
\tif EconomyManager.energy < cost:
\t\tprint("[Builder] Not enough energy! Need ", cost)
\t\treturn
\tEconomyManager.spend_energy(cost)
\tvar node := Node2D.new()
\tnode.position = world_pos
\tmatch build_type:
\t\t"power_plant":
\t\t\tnode.name = "PowerPlant"
\t\t\tnode.set_script(load("res://scripts/structures/power_plant.gd"))
\t\t"factory":
\t\t\tnode.name = "Factory"
\t\t\tnode.set_script(load("res://scripts/structures/factory.gd"))
\t\t_:
\t\t\tnode.name = "Structure"
\t\t\tnode.set_script(load("res://scripts/structures/structure_base.gd"))
\tget_parent().add_child(node)
\tnode.call("setup", node.name, 300, is_player)
\tprint("[Builder] Built ", build_type, " at ", world_pos)


func take_damage(amount: float) -> void:
\thp -= amount
\tif hp <= 0.0:
\t\tprint("[Builder] Destroyed.")
\t\tqueue_free()
'''


def gen_soldier_unit():
    """SoldierUnit — can move and attack enemy units/structures."""
    return '''## SoldierUnit — Tau'ri Marine / Jaffa Warrior
extends Node2D

@export var max_hp: float = 120.0
@export var move_speed: float = 160.0
@export var attack_damage: float = 15.0
@export var attack_range: float = 80.0
@export var attack_cooldown: float = 1.0

var hp: float = 120.0
var is_player: bool = true
var target_position: Vector2 = Vector2.ZERO
var is_moving: bool = false
var unit_radius: float = 13.0
var attack_target_node: Node2D = null
var attack_timer: float = 0.0


func setup(player: bool) -> void:
\tis_player = player
\thp = max_hp
\ttarget_position = position
\tif is_player:
\t\tadd_to_group("player_units")
\telse:
\t\tadd_to_group("enemies")


func _draw() -> void:
\tdraw_circle(Vector2(2, 2), unit_radius, Color(0, 0, 0, 0.45))
\tvar armor = Color(0.15, 0.28, 0.5) if is_player else Color(0.6, 0.18, 0.1)
\tdraw_circle(Vector2.ZERO, unit_radius, armor)
\tvar core = Color(0.2, 0.38, 0.62) if is_player else Color(0.78, 0.25, 0.12)
\tdraw_circle(Vector2.ZERO, unit_radius * 0.55, core)
\t# P90 / Staff weapon barrel
\tvar wc = Color(0.55, 0.58, 0.5, 0.9) if is_player else Color(0.8, 0.6, 0.2, 0.9)
\tdraw_line(Vector2(0, -unit_radius * 0.3), Vector2(0, -unit_radius - 4), wc, 2.5, true)
\t# Crosshair
\tdraw_line(Vector2(-4, -2), Vector2(4, -2), Color(0.9, 0.9, 0.8, 0.7), 1.5, true)
\tvar border_c = Color(0.3, 0.45, 0.7, 0.5) if is_player else Color(0.8, 0.35, 0.15, 0.5)
\tdraw_arc(Vector2.ZERO, unit_radius + 0.5, 0, TAU, 24, border_c, 1.5, true)
\t_draw_hp_bar()


func _draw_hp_bar() -> void:
\tvar w := 24.0
\tvar h := 3.0
\tvar p := Vector2(-w / 2.0, -unit_radius - 12.0)
\tdraw_rect(Rect2(p, Vector2(w, h)), Color(0.02, 0.03, 0.06, 0.9))
\tvar r := clampf(hp / max_hp, 0.0, 1.0)
\tvar c := Color(0.1, 0.8, 0.25) if r > 0.6 else (Color(0.85, 0.75, 0.1) if r > 0.3 else Color(0.9, 0.12, 0.08))
\tdraw_rect(Rect2(p, Vector2(w * r, h)), c)
\tdraw_rect(Rect2(p, Vector2(w, h)), Color(0.35, 0.45, 0.55, 0.35), false)


func move_to(target: Vector2) -> void:
\ttarget_position = target
\tis_moving = true
\tattack_target_node = null


func _process(delta: float) -> void:
\tattack_timer -= delta
\tif attack_target_node and is_instance_valid(attack_target_node):
\t\tvar dist = position.distance_to(attack_target_node.global_position)
\t\tif dist <= attack_range:
\t\t\tis_moving = false
\t\t\t_do_attack()
\t\telse:
\t\t\ttarget_position = attack_target_node.global_position
\t\t\tis_moving = true
\telse:
\t\tattack_target_node = null
\tif is_moving:
\t\tvar direction = (target_position - position).normalized()
\t\tvar distance = position.distance_to(target_position)
\t\tif distance < 5.0:
\t\t\tis_moving = false
\t\telse:
\t\t\tposition += direction * move_speed * delta
\tqueue_redraw()


func attack_target(target: Node2D) -> void:
\tattack_target_node = target


func _do_attack() -> void:
\tif attack_timer > 0.0:
\t\treturn
\tif not attack_target_node or not is_instance_valid(attack_target_node):
\t\treturn
\tattack_timer = attack_cooldown
\tif attack_target_node.has_method("take_damage"):
\t\tattack_target_node.call("take_damage", attack_damage)


func take_damage(amount: float) -> void:
\thp -= amount
\tif hp <= 0.0:
\t\tprint("[Soldier] ", name, " destroyed.")
\t\tqueue_free()
'''


# ============================================================
#  GDSCRIPT GENERATORS — STRUCTURES
# ============================================================

def gen_structure_base():
    """StructureBase — base class for all buildings."""
    return '''## StructureBase — SGC / Goa'uld base structure
extends Node2D

var structure_name: String = "Structure"
var max_hp: float = 500.0
var hp: float = 500.0
var is_player: bool = true
var struct_size: Vector2 = Vector2(56, 56)


func setup(sname: String, health: float, player: bool) -> void:
\tstructure_name = sname
\tmax_hp = health
\thp = health
\tis_player = player
\tname = sname
\tif is_player:
\t\tadd_to_group("player_structures")
\telse:
\t\tadd_to_group("enemies")
\t\tadd_to_group("enemy_structures")


func _draw() -> void:
\tvar half = struct_size / 2.0
\t# Shadow
\tdraw_rect(Rect2(-half + Vector2(3, 3), struct_size), Color(0, 0, 0, 0.45))
\t# Base plate
\tvar base_c = Color(0.1, 0.18, 0.3) if is_player else Color(0.32, 0.22, 0.08)
\tdraw_rect(Rect2(-half, struct_size), base_c)
\t# Roof section (lighter)
\tvar roof_c = Color(0.14, 0.25, 0.38) if is_player else Color(0.45, 0.33, 0.12)
\tdraw_rect(Rect2(-half, Vector2(struct_size.x, struct_size.y * 0.35)), roof_c)
\t# Team accent stripe
\tvar accent = Color(0.12, 0.5, 0.78) if is_player else Color(0.82, 0.58, 0.1)
\tdraw_rect(Rect2(Vector2(-half.x, half.y - 4), Vector2(struct_size.x, 4)), accent)
\t# Windows
\tvar wc = Color(0.45, 0.68, 0.88, 0.45) if is_player else Color(0.82, 0.62, 0.18, 0.45)
\tdraw_rect(Rect2(Vector2(-half.x + 6, -half.y + 5), Vector2(9, 7)), wc)
\tdraw_rect(Rect2(Vector2(half.x - 15, -half.y + 5), Vector2(9, 7)), wc)
\t# Door
\tdraw_rect(Rect2(Vector2(-4, half.y - 14), Vector2(8, 14)), Color(0.06, 0.08, 0.15))
\t# Antenna
\tdraw_line(Vector2(half.x - 8, -half.y), Vector2(half.x - 8, -half.y - 10), Color(0.4, 0.45, 0.5, 0.7), 1.5, true)
\tdraw_circle(Vector2(half.x - 8, -half.y - 10), 2, Color(0.9, 0.2, 0.1, 0.7))
\t# Border
\tvar bc = Color(0.22, 0.38, 0.55, 0.6) if is_player else Color(0.65, 0.48, 0.18, 0.6)
\tdraw_rect(Rect2(-half, struct_size), bc, false, 2.0)
\t# Name
\tdraw_string(ThemeDB.fallback_font, Vector2(-half.x, -half.y - 14), structure_name, HORIZONTAL_ALIGNMENT_LEFT, -1, 10, Color(0.65, 0.75, 0.85, 0.8))
\t_draw_hp_bar()


func _draw_hp_bar() -> void:
\tvar w := struct_size.x + 4.0
\tvar h := 4.0
\tvar p := Vector2(-w / 2.0, struct_size.y / 2.0 + 5.0)
\tdraw_rect(Rect2(p, Vector2(w, h)), Color(0.02, 0.03, 0.06, 0.9))
\tvar r := clampf(hp / max_hp, 0.0, 1.0)
\tvar c := Color(0.1, 0.8, 0.25) if r > 0.6 else (Color(0.85, 0.75, 0.1) if r > 0.3 else Color(0.9, 0.12, 0.08))
\tdraw_rect(Rect2(p, Vector2(w * r, h)), c)
\tdraw_rect(Rect2(p, Vector2(w, h)), Color(0.35, 0.45, 0.55, 0.3), false)


func _process(_d: float) -> void:
\tqueue_redraw()


func take_damage(amount: float) -> void:
\thp -= amount
\tif hp <= 0.0:
\t\tprint("[Structure] ", structure_name, " destroyed!")
\t\tqueue_free()
'''


def gen_power_plant():
    """PowerPlant — generates energy over time."""
    return '''## PowerPlant — Naquadah Reactor (Stargate-tech power source)
extends Node2D

var structure_name: String = "PowerPlant"
var max_hp: float = 300.0
var hp: float = 300.0
var is_player: bool = true
var struct_size: Vector2 = Vector2(48, 48)

@export var energy_per_second: float = 5.0
var pulse_time: float = 0.0


func setup(sname: String, health: float, player: bool) -> void:
\tstructure_name = sname
\tmax_hp = health
\thp = health
\tis_player = player
\tif is_player:
\t\tadd_to_group("player_structures")
\t\tEconomyManager.register_power_plant(self)
\telse:
\t\tadd_to_group("enemies")
\t\tadd_to_group("enemy_structures")


func _draw() -> void:
\tvar half = struct_size / 2.0
\tdraw_rect(Rect2(-half + Vector2(3, 3), struct_size), Color(0, 0, 0, 0.45))
\t# Base
\tvar base_c = Color(0.08, 0.15, 0.25) if is_player else Color(0.3, 0.2, 0.06)
\tdraw_rect(Rect2(-half, struct_size), base_c)
\t# Naquadah reactor core (pulsating teal / gold glow)
\tvar glow = 0.35 + 0.2 * sin(pulse_time * 2.5)
\tvar rc = Color(0.0, 0.75, 0.55, glow) if is_player else Color(0.85, 0.6, 0.1, glow)
\tdraw_circle(Vector2.ZERO, 14.0, rc)
\tdraw_circle(Vector2.ZERO, 8.0, Color(rc.r * 1.2, rc.g * 1.2, rc.b * 1.2, glow * 1.8))
\tdraw_circle(Vector2.ZERO, 3.0, Color(1, 1, 1, glow * 0.6))
\t# Containment ring
\tvar ring_c = Color(0.0, 0.6, 0.45, 0.4 + glow * 0.3) if is_player else Color(0.8, 0.55, 0.15, 0.4 + glow * 0.3)
\tdraw_arc(Vector2.ZERO, 16.0, 0, TAU, 20, ring_c, 2.0, true)
\t# Lightning bolt icon
\tvar lc = Color(1, 1, 0.75, 0.85)
\tdraw_line(Vector2(-2, -18), Vector2(3, -5), lc, 2.0, true)
\tdraw_line(Vector2(3, -5), Vector2(-1, -2), lc, 2.0, true)
\tdraw_line(Vector2(-1, -2), Vector2(4, 16), lc, 2.0, true)
\t# Border with energy glow
\tvar bc = Color(0.0, 0.55, 0.42, 0.4 + glow * 0.2) if is_player else Color(0.75, 0.5, 0.1, 0.4 + glow * 0.2)
\tdraw_rect(Rect2(-half, struct_size), bc, false, 2.5)
\t# Label
\tvar lbl_c = Color(0.0, 0.85, 0.65, 0.85) if is_player else Color(0.9, 0.7, 0.2, 0.85)
\tdraw_string(ThemeDB.fallback_font, Vector2(-half.x, -half.y - 8), "NAQUADAH", HORIZONTAL_ALIGNMENT_LEFT, -1, 9, lbl_c)
\t_draw_hp_bar()


func _draw_hp_bar() -> void:
\tvar w := struct_size.x + 4.0
\tvar h := 4.0
\tvar p := Vector2(-w / 2.0, struct_size.y / 2.0 + 5.0)
\tdraw_rect(Rect2(p, Vector2(w, h)), Color(0.02, 0.03, 0.06, 0.9))
\tvar r := clampf(hp / max_hp, 0.0, 1.0)
\tvar c := Color(0.1, 0.8, 0.25) if r > 0.6 else (Color(0.85, 0.75, 0.1) if r > 0.3 else Color(0.9, 0.12, 0.08))
\tdraw_rect(Rect2(p, Vector2(w * r, h)), c)


func _process(delta: float) -> void:
\tpulse_time += delta
\tqueue_redraw()


func take_damage(amount: float) -> void:
\thp -= amount
\tif hp <= 0.0:
\t\tif is_player:
\t\t\tEconomyManager.unregister_power_plant(self)
\t\tprint("[PowerPlant] Destroyed!")
\t\tqueue_free()
'''


def gen_factory():
    """Factory — produces Soldier units; consumes energy."""
    return '''## Factory — Vehicle Assembly Bay / Ha'tak Construction
extends Node2D

var structure_name: String = "Factory"
var max_hp: float = 400.0
var hp: float = 400.0
var is_player: bool = true
var struct_size: Vector2 = Vector2(60, 60)

@export var soldier_cost: float = 30.0
@export var production_time: float = 5.0

var production_timer: float = 0.0
var is_producing: bool = false
var gear_angle: float = 0.0


func setup(sname: String, health: float, player: bool) -> void:
\tstructure_name = sname
\tmax_hp = health
\thp = health
\tis_player = player
\tif is_player:
\t\tadd_to_group("player_structures")
\telse:
\t\tadd_to_group("enemies")
\t\tadd_to_group("enemy_structures")


func _draw() -> void:
\tvar half = struct_size / 2.0
\tdraw_rect(Rect2(-half + Vector2(3, 3), struct_size), Color(0, 0, 0, 0.45))
\t# Base
\tvar base_c = Color(0.1, 0.13, 0.24) if is_player else Color(0.28, 0.15, 0.06)
\tdraw_rect(Rect2(-half, struct_size), base_c)
\t# Hangar door (dark recess)
\tvar door_c = Color(0.05, 0.06, 0.12) if is_player else Color(0.15, 0.1, 0.04)
\tdraw_rect(Rect2(Vector2(-14, -half.y + 4), Vector2(28, struct_size.y - 8)), door_c)
\t# Door horizontal stripes
\tvar stripe_c = Color(0.22, 0.28, 0.38, 0.25) if is_player else Color(0.4, 0.28, 0.12, 0.25)
\tfor i in range(4):
\t\tvar y = -half.y + 10 + i * 12
\t\tdraw_line(Vector2(-12, y), Vector2(12, y), stripe_c, 1.0)
\t# Rotating gear (top-right corner)
\tvar gc = Color(0.5, 0.55, 0.62, 0.65) if is_player else Color(0.65, 0.45, 0.18, 0.65)
\tvar gear_pos = Vector2(half.x - 12, -half.y + 12)
\tfor i in range(6):
\t\tvar a = gear_angle + i * PI / 3.0
\t\tdraw_line(gear_pos + Vector2(cos(a), sin(a)) * 3.0, gear_pos + Vector2(cos(a), sin(a)) * 9.0, gc, 2.5, true)
\tdraw_arc(gear_pos, 5.5, 0, TAU, 12, gc, 1.5, true)
\tdraw_circle(gear_pos, 2.5, Color(0.15, 0.18, 0.28))
\t# Team accent stripe at bottom
\tvar accent = Color(0.12, 0.45, 0.72) if is_player else Color(0.72, 0.42, 0.08)
\tdraw_rect(Rect2(Vector2(-half.x, half.y - 4), Vector2(struct_size.x, 4)), accent)
\t# Border
\tvar bc = Color(0.2, 0.3, 0.48, 0.55) if is_player else Color(0.58, 0.35, 0.12, 0.55)
\tdraw_rect(Rect2(-half, struct_size), bc, false, 2.0)
\t# Label
\tvar lbl_c = Color(0.55, 0.65, 0.8, 0.8) if is_player else Color(0.8, 0.6, 0.25, 0.8)
\tdraw_string(ThemeDB.fallback_font, Vector2(-half.x, -half.y - 8), "FACTORY", HORIZONTAL_ALIGNMENT_LEFT, -1, 9, lbl_c)
\t# Production progress bar
\tif is_producing:
\t\tvar pw := struct_size.x
\t\tvar pp := Vector2(-pw / 2.0, half.y + 8)
\t\tdraw_rect(Rect2(pp, Vector2(pw, 5)), Color(0.03, 0.04, 0.08, 0.85))
\t\tvar prog = 1.0 - (production_timer / production_time)
\t\tvar pc = Color(0.1, 0.65, 0.9) if is_player else Color(0.85, 0.55, 0.1)
\t\tdraw_rect(Rect2(pp, Vector2(pw * prog, 5)), pc)
\t\tdraw_rect(Rect2(pp, Vector2(pw, 5)), Color(0.25, 0.4, 0.6, 0.35), false)
\t_draw_hp_bar()


func _draw_hp_bar() -> void:
\tvar w := struct_size.x + 4.0
\tvar h := 4.0
\tvar p := Vector2(-w / 2.0, struct_size.y / 2.0 + 5.0)
\tdraw_rect(Rect2(p, Vector2(w, h)), Color(0.02, 0.03, 0.06, 0.9))
\tvar r := clampf(hp / max_hp, 0.0, 1.0)
\tvar c := Color(0.1, 0.8, 0.25) if r > 0.6 else (Color(0.85, 0.75, 0.1) if r > 0.3 else Color(0.9, 0.12, 0.08))
\tdraw_rect(Rect2(p, Vector2(w * r, h)), c)


func _on_produce_pressed() -> void:
\tif is_producing:
\t\treturn
\tif EconomyManager.energy < soldier_cost:
\t\tprint("[Factory] Not enough energy! Need ", soldier_cost)
\t\treturn
\tEconomyManager.spend_energy(soldier_cost)
\tis_producing = true
\tproduction_timer = production_time
\tprint("[Factory] Producing soldier... (", production_time, "s)")


func produce_soldier_ai() -> void:
\tif is_producing:
\t\treturn
\tis_producing = true
\tproduction_timer = production_time


func _process(delta: float) -> void:
\tif is_producing:
\t\tgear_angle += delta * 3.0
\t\tproduction_timer -= delta
\t\tif production_timer <= 0.0:
\t\t\tis_producing = false
\t\t\t_spawn_soldier()
\tqueue_redraw()


func _spawn_soldier() -> void:
\tvar soldier := Node2D.new()
\tsoldier.name = "Soldier"
\tsoldier.position = position + Vector2(50, 0)
\tsoldier.set_script(load("res://scripts/units/soldier_unit.gd"))
\tget_parent().add_child(soldier)
\tsoldier.call("setup", is_player)
\tif is_player:
\t\tvar rts = get_node_or_null("/root/PlanetMap/RTSController")
\t\tif rts:
\t\t\trts.call("register_unit", soldier)
\tprint("[Factory] Soldier produced!")


func take_damage(amount: float) -> void:
\thp -= amount
\tif hp <= 0.0:
\t\tprint("[Factory] Destroyed!")
\t\tqueue_free()
'''


# ============================================================
#  GDSCRIPT GENERATORS — ECONOMY
# ============================================================

def gen_economy_manager():
    """EconomyManager autoload — tracks energy and minerals."""
    return '''## EconomyManager (Autoload)
## Tracks global resources: energy and minerals.
extends Node

# --------------- Resources ---------------
var energy: float = 100.0
var minerals: float = 50.0

# Power plants registered for energy generation
var power_plants: Array = []

# --------------- Signals ---------------
signal energy_changed(new_value: float)
signal minerals_changed(new_value: float)


func _ready() -> void:
\tprint("[EconomyManager] Initialized. Starting energy: ", energy)


func _process(delta: float) -> void:
\t## Tick energy generation from all registered power plants.
\tfor plant in power_plants:
\t\tif is_instance_valid(plant):
\t\t\tenergy += plant.energy_per_second * delta
\t# Clean up dead plants
\tpower_plants = power_plants.filter(func(p): return is_instance_valid(p))


# --------------- Registration ---------------

func register_power_plant(plant: Node) -> void:
\tif plant not in power_plants:
\t\tpower_plants.append(plant)
\t\tprint("[Economy] Power plant registered. Total: ", power_plants.size())


func unregister_power_plant(plant: Node) -> void:
\tpower_plants.erase(plant)
\tprint("[Economy] Power plant unregistered. Total: ", power_plants.size())


# --------------- Spending ---------------

func spend_energy(amount: float) -> bool:
\tif energy >= amount:
\t\tenergy -= amount
\t\tenergy_changed.emit(energy)
\t\treturn true
\tprint("[Economy] Not enough energy!")
\treturn false


func spend_minerals(amount: float) -> bool:
\tif minerals >= amount:
\t\tminerals -= amount
\t\tminerals_changed.emit(minerals)
\t\treturn true
\tprint("[Economy] Not enough minerals!")
\treturn false


func add_energy(amount: float) -> void:
\tenergy += amount
\tenergy_changed.emit(energy)


func add_minerals(amount: float) -> void:
\tminerals += amount
\tminerals_changed.emit(minerals)


# --------------- Reset ---------------

func reset() -> void:
\tenergy = 100.0
\tminerals = 50.0
\tpower_plants.clear()
'''


# ============================================================
#  GDSCRIPT GENERATORS — STARGATE
# ============================================================

def gen_stargate_manager():
    """StargateManager autoload — simple teleport between planets."""
    return '''## StargateManager (Autoload)
## Handles stargate travel between planets.
extends Node

# Stargate connections: array of [planet_a_id, planet_b_id]
var connections: Array = []

# --------------- Signals ---------------
signal teleport_started(from_planet: int, to_planet: int)
signal teleport_completed(to_planet: int)


func _ready() -> void:
\tprint("[StargateManager] Initialized.")
\t_init_connections()


func _init_connections() -> void:
\t## Default stargate network.
\tconnections = [
\t\t[0, 1],  # Terra Prime <-> Kesh'ra
\t\t[1, 2],  # Kesh'ra <-> Novalith
\t]


func get_connected_planets(planet_id: int) -> Array:
\t## Returns list of planet IDs reachable from given planet.
\tvar result: Array = []
\tfor conn in connections:
\t\tif conn[0] == planet_id:
\t\t\tresult.append(conn[1])
\t\telif conn[1] == planet_id:
\t\t\tresult.append(conn[0])
\treturn result


func can_travel(from_id: int, to_id: int) -> bool:
\t## Check if direct stargate connection exists.
\tfor conn in connections:
\t\tif (conn[0] == from_id and conn[1] == to_id) or \\
\t\t   (conn[1] == from_id and conn[0] == to_id):
\t\t\treturn true
\treturn false


func travel(from_id: int, to_id: int) -> void:
\t## Execute stargate travel.
\tif not can_travel(from_id, to_id):
\t\tprint("[Stargate] No connection between ", from_id, " and ", to_id)
\t\treturn
\tteleport_started.emit(from_id, to_id)
\tprint("[Stargate] Traveling from planet ", from_id, " to ", to_id)
\tGameManager.enter_planet(to_id)
\tteleport_completed.emit(to_id)
'''


# ============================================================
#  GDSCRIPT GENERATORS — AI
# ============================================================

def gen_enemy_ai():
    """EnemyAI — spawns an enemy base, produces soldiers, attacks player."""
    return '''## EnemyAI
## Simple enemy AI: spawns a base, builds soldiers, attacks the player.
extends Node

# --------------- Config ---------------
@export var spawn_interval: float = 8.0
@export var attack_interval: float = 15.0

# State
var enemy_base: Node2D = null
var enemy_factory: Node2D = null
var soldiers: Array = []
var spawn_timer: float = 3.0  # Initial delay before first spawn
var attack_timer: float = 10.0


func _ready() -> void:
\tprint("[EnemyAI] Initialized.")
\t_spawn_enemy_base()


# --------------- Setup ---------------

func _spawn_enemy_base() -> void:
\t## Create the enemy base and factory on the right side of the map.
\t# Enemy base
\tenemy_base = Node2D.new()
\tenemy_base.name = "EnemyBase"
\tenemy_base.position = Vector2(900, 400)
\tenemy_base.set_script(load("res://scripts/structures/structure_base.gd"))
\tget_parent().add_child(enemy_base)
\tenemy_base.call("setup", "EnemyBase", 600, false)

\t# Store reference in PlanetMap for victory condition
\tvar planet_map = get_parent()
\tif planet_map and "enemy_base" in planet_map:
\t\tplanet_map.enemy_base = enemy_base

\t# Enemy factory
\tenemy_factory = Node2D.new()
\tenemy_factory.name = "EnemyFactory"
\tenemy_factory.position = Vector2(850, 430)
\tenemy_factory.set_script(load("res://scripts/structures/factory.gd"))
\tget_parent().add_child(enemy_factory)
\tenemy_factory.call("setup", "EnemyFactory", 400, false)


# --------------- AI Loop ---------------

func _process(delta: float) -> void:
\tif not is_instance_valid(enemy_base):
\t\treturn  # Base destroyed, AI stops

\t# --- Soldier production ---
\tspawn_timer -= delta
\tif spawn_timer <= 0.0:
\t\tspawn_timer = spawn_interval
\t\t_produce_soldier()

\t# --- Attack wave ---
\tattack_timer -= delta
\tif attack_timer <= 0.0:
\t\tattack_timer = attack_interval
\t\t_launch_attack()

\t# Clean dead soldiers
\tsoldiers = soldiers.filter(func(s): return is_instance_valid(s))


# --------------- Production ---------------

func _produce_soldier() -> void:
\tif not is_instance_valid(enemy_factory):
\t\treturn
\t# Directly spawn (AI doesn't use economy)
\tvar soldier := Node2D.new()
\tsoldier.name = "EnemySoldier"
\tsoldier.position = enemy_factory.position + Vector2(-50, 0)
\tsoldier.set_script(load("res://scripts/units/soldier_unit.gd"))
\tget_parent().add_child(soldier)
\tsoldier.call("setup", false)
\tsoldiers.append(soldier)
\tprint("[EnemyAI] Soldier spawned. Army: ", soldiers.size())


# --------------- Attack ---------------

func _launch_attack() -> void:
\tif soldiers.is_empty():
\t\treturn

\t# Find nearest player structure or base
\tvar target = _find_player_target()
\tif not target:
\t\treturn

\tprint("[EnemyAI] Attacking with ", soldiers.size(), " soldiers!")
\tfor soldier in soldiers:
\t\tif is_instance_valid(soldier) and soldier.has_method("attack_target"):
\t\t\tsoldier.call("attack_target", target)


func _find_player_target() -> Node2D:
\t## Find the nearest player structure to attack.
\tvar targets = get_tree().get_nodes_in_group("player_structures")
\tif targets.is_empty():
\t\t# Try player units
\t\ttargets = get_tree().get_nodes_in_group("player_units")
\tif targets.is_empty():
\t\treturn null

\t# Return closest to enemy base
\tvar best: Node2D = null
\tvar best_dist: float = INF
\tfor t in targets:
\t\tif not is_instance_valid(t):
\t\t\tcontinue
\t\tvar d = enemy_base.position.distance_to(t.global_position) if is_instance_valid(enemy_base) else 0.0
\t\tif d < best_dist:
\t\t\tbest_dist = d
\t\t\tbest = t
\treturn best
'''


# ============================================================
#  MAIN — FILE WRITER
# ============================================================

def write_file(project_dir, relative_path, content):
    """Write a single GDScript file, creating directories as needed."""
    full_path = os.path.join(project_dir, relative_path)
    dir_path = os.path.dirname(full_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(full_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return full_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_code.py <project_dir>")
        sys.exit(1)

    project_dir = os.path.abspath(sys.argv[1])
    print(f"  Project directory: {project_dir}")
    print(f"  Game: {GAME_NAME}")
    print()
    print("  Generating gameplay scripts...")
    print()

    # Map generator function names to actual functions in this module
    generators = {
        "gen_game_manager":      gen_game_manager,
        "gen_input_manager":     gen_input_manager,
        "gen_save_manager":      gen_save_manager,
        "gen_camera_controller": gen_camera_controller,
        "gen_galaxy_map":        gen_galaxy_map,
        "gen_planet_node":       gen_planet_node,
        "gen_planet_map":        gen_planet_map,
        "gen_rts_controller":    gen_rts_controller,
        "gen_unit_base":         gen_unit_base,
        "gen_builder_unit":      gen_builder_unit,
        "gen_soldier_unit":      gen_soldier_unit,
        "gen_structure_base":    gen_structure_base,
        "gen_power_plant":       gen_power_plant,
        "gen_factory":           gen_factory,
        "gen_economy_manager":   gen_economy_manager,
        "gen_stargate_manager":  gen_stargate_manager,
        "gen_enemy_ai":          gen_enemy_ai,
    }

    generated_files = []

    for relative_path, gen_name in SCRIPT_FILES:
        gen_func = generators.get(gen_name)
        if gen_func is None:
            print(f"  WARNING: No generator for {gen_name}, skipping {relative_path}")
            continue
        content = gen_func()
        full_path = write_file(project_dir, relative_path, content)
        generated_files.append(relative_path)
        print(f"  [OK] {relative_path}")

    # --- Summary ---
    print()
    print("  ========================================")
    print(f"  CODE GENERATION COMPLETE: {GAME_NAME}")
    print(f"  Files generated: {len(generated_files)}")
    print("  ========================================")
    print()
    print("  Generated files:")
    for f in generated_files:
        print(f"    - {f}")
    print()
    print("  All gameplay systems ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
