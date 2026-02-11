"""
GATE DOMINION - Scene & Integration Generator
===============================================
AI Role: AI_SCENE_ARCHITECT + AI_INTEGRATOR

This script is the GLUE of the pipeline.  It generates every
remaining .tscn scene file and the integration scripts that
connect all existing systems into a fully playable game.

Runs AFTER  : generate_code.py, generate_assets.py
Runs BEFORE : generate_ui.py

What it creates
---------------
SCENES
  scenes/victory.tscn          — Victory screen
  scenes/defeat.tscn           — Defeat screen
  scenes/units/builder.tscn    — Builder unit template (with texture)
  scenes/units/soldier.tscn    — Soldier unit template (with texture)
  scenes/structures/power_plant.tscn
  scenes/structures/factory.tscn
  scenes/structures/base.tscn
  scenes/stargate/stargate.tscn

SCRIPTS
  scripts/core/victory_screen.gd
  scripts/core/defeat_screen.gd
  scripts/core/game_flow.gd     — Autoload that wires victory/defeat
                                   scene transitions + first-launch tutorial
  scripts/stargate/stargate_node.gd

INTEGRATION
  Patches project.godot to register the GameFlow autoload.

Usage:
    python generate_scenes.py <project_dir>
"""

import sys
import os


# ============================================================
#  CONFIGURATION
# ============================================================

GAME_NAME = "Gate Dominion"

# --- Scene files ---
SCENE_FILES = [
    ("scenes/victory.tscn",                "gen_victory_scene"),
    ("scenes/defeat.tscn",                 "gen_defeat_scene"),
    ("scenes/units/builder.tscn",          "gen_builder_scene"),
    ("scenes/units/soldier.tscn",          "gen_soldier_scene"),
    ("scenes/structures/power_plant.tscn", "gen_power_plant_scene"),
    ("scenes/structures/factory.tscn",     "gen_factory_scene"),
    ("scenes/structures/base.tscn",        "gen_base_scene"),
    ("scenes/stargate/stargate.tscn",      "gen_stargate_scene"),
]

# --- Script files ---
SCRIPT_FILES = [
    ("scripts/core/victory_screen.gd",    "gen_victory_script"),
    ("scripts/core/defeat_screen.gd",     "gen_defeat_script"),
    ("scripts/core/game_flow.gd",         "gen_game_flow_script"),
    ("scripts/stargate/stargate_node.gd", "gen_stargate_node_script"),
]


# ============================================================
#  SCENE GENERATORS — VICTORY / DEFEAT
# ============================================================

def gen_victory_scene():
    """Victory screen — big VICTORY text, Back to Menu, Play Again."""
    return '''[gd_scene load_steps=2 format=3 uid="uid://victory"]

[ext_resource type="Script" path="res://scripts/core/victory_screen.gd" id="1"]

[node name="VictoryScreen" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
script = ExtResource("1")

[node name="Background" type="ColorRect" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
color = Color(0.0, 0.08, 0.04, 1)

[node name="VBox" type="VBoxContainer" parent="."]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -200.0
offset_top = -130.0
offset_right = 200.0
offset_bottom = 130.0
grow_horizontal = 2
grow_vertical = 2

[node name="Title" type="Label" parent="VBox"]
layout_mode = 2
text = "VICTORY!"
horizontal_alignment = 1
vertical_alignment = 1

[node name="Subtitle" type="Label" parent="VBox"]
layout_mode = 2
text = "The enemy base has been destroyed."
horizontal_alignment = 1

[node name="Spacer" type="Control" parent="VBox"]
layout_mode = 2
custom_minimum_size = Vector2(0, 40)

[node name="ContinueBtn" type="Button" parent="VBox"]
layout_mode = 2
custom_minimum_size = Vector2(220, 40)
text = "Continue (Galaxy Map)"

[node name="MainMenuBtn" type="Button" parent="VBox"]
layout_mode = 2
custom_minimum_size = Vector2(220, 40)
text = "Main Menu"
'''


def gen_defeat_scene():
    """Defeat screen — DEFEAT text, Retry, Main Menu."""
    return '''[gd_scene load_steps=2 format=3 uid="uid://defeat"]

[ext_resource type="Script" path="res://scripts/core/defeat_screen.gd" id="1"]

[node name="DefeatScreen" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
script = ExtResource("1")

[node name="Background" type="ColorRect" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
color = Color(0.1, 0.02, 0.02, 1)

[node name="VBox" type="VBoxContainer" parent="."]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -200.0
offset_top = -130.0
offset_right = 200.0
offset_bottom = 130.0
grow_horizontal = 2
grow_vertical = 2

[node name="Title" type="Label" parent="VBox"]
layout_mode = 2
text = "DEFEAT"
horizontal_alignment = 1
vertical_alignment = 1

[node name="Subtitle" type="Label" parent="VBox"]
layout_mode = 2
text = "Your base has been destroyed."
horizontal_alignment = 1

[node name="Spacer" type="Control" parent="VBox"]
layout_mode = 2
custom_minimum_size = Vector2(0, 40)

[node name="RetryBtn" type="Button" parent="VBox"]
layout_mode = 2
custom_minimum_size = Vector2(220, 40)
text = "Retry Planet"

[node name="MainMenuBtn" type="Button" parent="VBox"]
layout_mode = 2
custom_minimum_size = Vector2(220, 40)
text = "Main Menu"
'''


# ============================================================
#  SCENE GENERATORS — UNIT TEMPLATES
# ============================================================

def gen_builder_scene():
    """Builder unit .tscn — Node2D with Sprite2D + script."""
    return '''[gd_scene load_steps=3 format=3 uid="uid://unit_builder"]

[ext_resource type="Script" path="res://scripts/units/builder_unit.gd" id="1"]
[ext_resource type="Texture2D" path="res://assets/textures/units/builder.png" id="2"]

[node name="Builder" type="Node2D"]
script = ExtResource("1")

[node name="Sprite" type="Sprite2D" parent="."]
texture = ExtResource("2")

[node name="CollisionShape" type="Area2D" parent="."]
collision_layer = 2
collision_mask = 0

[node name="Shape" type="CollisionShape2D" parent="CollisionShape"]
shape = SubResource("RectangleShape2D_builder")

[sub_resource type="RectangleShape2D" id="RectangleShape2D_builder"]
size = Vector2(20, 20)
'''


def gen_soldier_scene():
    """Soldier unit .tscn — Node2D with Sprite2D + script."""
    return '''[gd_scene load_steps=3 format=3 uid="uid://unit_soldier"]

[ext_resource type="Script" path="res://scripts/units/soldier_unit.gd" id="1"]
[ext_resource type="Texture2D" path="res://assets/textures/units/soldier.png" id="2"]

[node name="Soldier" type="Node2D"]
script = ExtResource("1")

[node name="Sprite" type="Sprite2D" parent="."]
texture = ExtResource("2")

[node name="CollisionShape" type="Area2D" parent="."]
collision_layer = 2
collision_mask = 0

[node name="Shape" type="CollisionShape2D" parent="CollisionShape"]
shape = SubResource("RectangleShape2D_soldier")

[sub_resource type="RectangleShape2D" id="RectangleShape2D_soldier"]
size = Vector2(18, 18)
'''


# ============================================================
#  SCENE GENERATORS — STRUCTURE TEMPLATES
# ============================================================

def gen_power_plant_scene():
    """PowerPlant .tscn template."""
    return '''[gd_scene load_steps=3 format=3 uid="uid://struct_powerplant"]

[ext_resource type="Script" path="res://scripts/structures/power_plant.gd" id="1"]
[ext_resource type="Texture2D" path="res://assets/textures/structures/powerplant.png" id="2"]

[node name="PowerPlant" type="Node2D"]
script = ExtResource("1")

[node name="Sprite" type="Sprite2D" parent="."]
texture = ExtResource("2")

[node name="CollisionShape" type="Area2D" parent="."]
collision_layer = 4
collision_mask = 0

[node name="Shape" type="CollisionShape2D" parent="CollisionShape"]
shape = SubResource("RectangleShape2D_pp")

[sub_resource type="RectangleShape2D" id="RectangleShape2D_pp"]
size = Vector2(36, 36)
'''


def gen_factory_scene():
    """Factory .tscn template."""
    return '''[gd_scene load_steps=3 format=3 uid="uid://struct_factory"]

[ext_resource type="Script" path="res://scripts/structures/factory.gd" id="1"]
[ext_resource type="Texture2D" path="res://assets/textures/structures/factory.png" id="2"]

[node name="Factory" type="Node2D"]
script = ExtResource("1")

[node name="Sprite" type="Sprite2D" parent="."]
texture = ExtResource("2")

[node name="CollisionShape" type="Area2D" parent="."]
collision_layer = 4
collision_mask = 0

[node name="Shape" type="CollisionShape2D" parent="CollisionShape"]
shape = SubResource("RectangleShape2D_fac")

[sub_resource type="RectangleShape2D" id="RectangleShape2D_fac"]
size = Vector2(44, 44)
'''


def gen_base_scene():
    """Generic base structure .tscn template."""
    return '''[gd_scene load_steps=2 format=3 uid="uid://struct_base"]

[ext_resource type="Script" path="res://scripts/structures/structure_base.gd" id="1"]

[node name="Base" type="Node2D"]
script = ExtResource("1")

[node name="Visual" type="ColorRect" parent="."]
offset_left = -24.0
offset_top = -24.0
offset_right = 24.0
offset_bottom = 24.0
color = Color(0.2, 0.6, 0.8, 1)

[node name="Label" type="Label" parent="."]
offset_left = -20.0
offset_top = -34.0
offset_right = 20.0
offset_bottom = -18.0
text = "BASE"
horizontal_alignment = 1

[node name="CollisionShape" type="Area2D" parent="."]
collision_layer = 4
collision_mask = 0

[node name="Shape" type="CollisionShape2D" parent="CollisionShape"]
shape = SubResource("RectangleShape2D_base")

[sub_resource type="RectangleShape2D" id="RectangleShape2D_base"]
size = Vector2(48, 48)
'''


# ============================================================
#  SCENE GENERATORS — STARGATE
# ============================================================

def gen_stargate_scene():
    """Stargate portal — visual ring node for the galaxy map."""
    return '''[gd_scene load_steps=2 format=3 uid="uid://stargate"]

[ext_resource type="Script" path="res://scripts/stargate/stargate_node.gd" id="1"]

[node name="Stargate" type="Node2D"]
script = ExtResource("1")

[node name="OuterRing" type="ColorRect" parent="."]
offset_left = -20.0
offset_top = -20.0
offset_right = 20.0
offset_bottom = 20.0
color = Color(0.0, 0.7, 1.0, 0.7)

[node name="InnerRing" type="ColorRect" parent="."]
offset_left = -12.0
offset_top = -12.0
offset_right = 12.0
offset_bottom = 12.0
color = Color(0.0, 0.2, 0.4, 0.9)

[node name="Label" type="Label" parent="."]
offset_left = -30.0
offset_top = 22.0
offset_right = 30.0
offset_bottom = 38.0
text = "Stargate"
horizontal_alignment = 1
'''


# ============================================================
#  SCRIPT GENERATORS
# ============================================================

def gen_victory_script():
    """VictoryScreen — handles buttons on the victory scene."""
    return '''## VictoryScreen
## Displayed when the player destroys the enemy base.
extends Control


func _ready() -> void:
\tprint("[VictoryScreen] Victory!")
\t$VBox/ContinueBtn.pressed.connect(_on_continue)
\t$VBox/MainMenuBtn.pressed.connect(_on_main_menu)


func _on_continue() -> void:
\t## Return to galaxy map to continue conquering.
\tGameManager.return_to_galaxy()


func _on_main_menu() -> void:
\tGameManager.go_to_main_menu()
'''


def gen_defeat_script():
    """DefeatScreen — handles buttons on the defeat scene."""
    return '''## DefeatScreen
## Displayed when the player's base is destroyed.
extends Control


func _ready() -> void:
\tprint("[DefeatScreen] Defeat.")
\t$VBox/RetryBtn.pressed.connect(_on_retry)
\t$VBox/MainMenuBtn.pressed.connect(_on_main_menu)


func _on_retry() -> void:
\t## Re-enter the same planet to try again.
\tvar pid := GameManager.current_planet_id
\tEconomyManager.reset()
\tGameManager.enter_planet(pid)


func _on_main_menu() -> void:
\tGameManager.go_to_main_menu()
'''


def gen_game_flow_script():
    """GameFlow autoload — the GLUE that connects all systems.

    Responsibilities:
      1. Listens to GameManager.victory / .defeat signals.
      2. After a short delay, transitions to the Victory / Defeat scene.
      3. Shows a one-time tutorial hint on first planet entry.
    """
    return '''## GameFlow (Autoload)
## The integration glue that connects all game systems.
##
## Responsibilities:
##   - Auto-transition to Victory/Defeat scenes after a delay.
##   - Show a first-launch tutorial hint.
##   - Provide helper functions for scene management.
extends Node

# --------------- Config ---------------
const TRANSITION_DELAY := 2.5  # seconds before switching scene
const VICTORY_SCENE := "res://scenes/victory.tscn"
const DEFEAT_SCENE  := "res://scenes/defeat.tscn"
const TUTORIAL_SAVE_KEY := "user://gate_dominion_tutorial_done.cfg"

var transition_pending: bool = false


func _ready() -> void:
\tprint("[GameFlow] Initialized — connecting signals.")
\tGameManager.victory.connect(_on_victory)
\tGameManager.defeat.connect(_on_defeat)
\tGameManager.planet_entered.connect(_on_planet_entered)


# =============== Victory / Defeat transitions ===============

func _on_victory() -> void:
\tif transition_pending:
\t\treturn
\ttransition_pending = true
\tprint("[GameFlow] Victory detected — transitioning in ", TRANSITION_DELAY, "s")
\tawait get_tree().create_timer(TRANSITION_DELAY).timeout
\ttransition_pending = false
\tget_tree().change_scene_to_file(VICTORY_SCENE)


func _on_defeat() -> void:
\tif transition_pending:
\t\treturn
\ttransition_pending = true
\tprint("[GameFlow] Defeat detected — transitioning in ", TRANSITION_DELAY, "s")
\tawait get_tree().create_timer(TRANSITION_DELAY).timeout
\ttransition_pending = false
\tget_tree().change_scene_to_file(DEFEAT_SCENE)


# =============== First-launch tutorial ===============

func _on_planet_entered(_planet_id: int) -> void:
\tif _has_seen_tutorial():
\t\treturn
\t# Wait for the planet scene to fully load
\tawait get_tree().process_frame
\tawait get_tree().process_frame
\t_show_tutorial()
\t_mark_tutorial_done()


func _has_seen_tutorial() -> bool:
\treturn FileAccess.file_exists(TUTORIAL_SAVE_KEY)


func _mark_tutorial_done() -> void:
\tvar f := FileAccess.open(TUTORIAL_SAVE_KEY, FileAccess.WRITE)
\tif f:
\t\tf.store_string("done")
\t\tf.close()


func _show_tutorial() -> void:
\t## Create a simple popup overlay with instructions.
\tvar overlay := ColorRect.new()
\toverlay.name = "TutorialOverlay"
\toverlay.set_anchors_preset(Control.PRESET_FULL_RECT)
\toverlay.color = Color(0, 0, 0, 0.7)

\tvar vbox := VBoxContainer.new()
\tvbox.set_anchors_preset(Control.PRESET_CENTER)
\tvbox.offset_left = -250
\tvbox.offset_top = -180
\tvbox.offset_right = 250
\tvbox.offset_bottom = 180

\tvar title := Label.new()
\ttitle.text = "HOW TO PLAY"
\ttitle.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
\tvbox.add_child(title)

\tvar spacer := Control.new()
\tspacer.custom_minimum_size = Vector2(0, 10)
\tvbox.add_child(spacer)

\tvar instructions := Label.new()
\tinstructions.text = """WASD — Move camera
Left Click — Select unit
Right Click — Move / Attack

Your Builder can build:
  • Power Plant (generates energy)
  • Factory (trains soldiers)

Destroy the enemy base to WIN!
Protect your base or you LOSE!

Use the Build Menu (bottom-left)
to construct buildings."""
\tinstructions.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
\tvbox.add_child(instructions)

\tvar spacer2 := Control.new()
\tspacer2.custom_minimum_size = Vector2(0, 15)
\tvbox.add_child(spacer2)

\tvar btn := Button.new()
\tbtn.text = "Got it!"
\tbtn.custom_minimum_size = Vector2(140, 36)
\tbtn.pressed.connect(func(): overlay.queue_free())
\tvbox.add_child(btn)

\toverlay.add_child(vbox)

\t# Add to scene tree via CanvasLayer so it renders on top
\tvar canvas := CanvasLayer.new()
\tcanvas.layer = 100
\tcanvas.add_child(overlay)
\tget_tree().current_scene.add_child(canvas)
'''


def gen_stargate_node_script():
    """StargateNode — visual / interactive stargate on galaxy map."""
    return '''## StargateNode
## A visual stargate that can be placed on the galaxy map.
## Clicking it triggers travel to the connected planet.
extends Node2D

@export var target_planet_id: int = -1
var pulse_time: float = 0.0


func _process(delta: float) -> void:
\t## Simple pulsing animation.
\tpulse_time += delta * 2.0
\tvar s := 1.0 + sin(pulse_time) * 0.1
\tscale = Vector2(s, s)


func travel() -> void:
\t## Initiate travel through this stargate.
\tif target_planet_id < 0:
\t\tprint("[Stargate] No target planet set.")
\t\treturn
\tvar current_planet := GameManager.current_planet_id
\tif StargateManager.can_travel(current_planet, target_planet_id):
\t\tStargateManager.travel(current_planet, target_planet_id)
\telse:
\t\tprint("[Stargate] No connection to planet ", target_planet_id)
'''


# ============================================================
#  PROJECT.GODOT PATCHER — add GameFlow autoload
# ============================================================

def patch_project_godot(project_dir):
    """Add the GameFlow autoload entry to the existing project.godot.

    This runs after generate_project.py has already created the file.
    We insert one line into the [autoload] section.
    """
    godot_path = os.path.join(project_dir, "project.godot")

    if not os.path.exists(godot_path):
        print("  WARNING: project.godot not found — skipping patch.")
        return False

    with open(godot_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_autoload = 'GameFlow="*res://scripts/core/game_flow.gd"'

    # Already patched?
    if new_autoload in content:
        print("  [OK] project.godot already has GameFlow autoload.")
        return True

    # Insert after the last existing autoload line in [autoload] section
    marker = 'SaveManager="*res://scripts/core/save_manager.gd"'
    if marker in content:
        content = content.replace(
            marker,
            marker + "\n" + new_autoload
        )
    else:
        # Fallback: insert after [autoload] header
        content = content.replace(
            "[autoload]\n",
            "[autoload]\n" + new_autoload + "\n"
        )

    with open(godot_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("  [OK] project.godot patched — GameFlow autoload added.")
    return True


# ============================================================
#  FILE WRITER
# ============================================================

def write_text(project_dir, relative_path, content):
    """Write a text file, creating directories as needed."""
    full_path = os.path.join(project_dir, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return full_path


# ============================================================
#  MAIN
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_scenes.py <project_dir>")
        sys.exit(1)

    project_dir = os.path.abspath(sys.argv[1])
    print(f"  Project directory: {project_dir}")
    print(f"  Game: {GAME_NAME}")
    print()

    # --- Map names to generator functions ---
    scene_gens = {
        "gen_victory_scene":      gen_victory_scene,
        "gen_defeat_scene":       gen_defeat_scene,
        "gen_builder_scene":      gen_builder_scene,
        "gen_soldier_scene":      gen_soldier_scene,
        "gen_power_plant_scene":  gen_power_plant_scene,
        "gen_factory_scene":      gen_factory_scene,
        "gen_base_scene":         gen_base_scene,
        "gen_stargate_scene":     gen_stargate_scene,
    }

    script_gens = {
        "gen_victory_script":       gen_victory_script,
        "gen_defeat_script":        gen_defeat_script,
        "gen_game_flow_script":     gen_game_flow_script,
        "gen_stargate_node_script": gen_stargate_node_script,
    }

    generated = []

    # === 1. Scene files (.tscn) ===
    print("  Generating scene files...")
    for rel_path, gen_name in SCENE_FILES:
        gen_func = scene_gens.get(gen_name)
        if not gen_func:
            print(f"  WARNING: No generator '{gen_name}', skipping {rel_path}")
            continue
        content = gen_func()
        write_text(project_dir, rel_path, content)
        generated.append(rel_path)
        print(f"  [OK] {rel_path}")

    print()

    # === 2. Script files (.gd) ===
    print("  Generating integration scripts...")
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

    # === 3. Patch project.godot ===
    print("  Patching project.godot for GameFlow autoload...")
    patch_project_godot(project_dir)

    # --- Summary ---
    print()
    print("  ========================================")
    print(f"  SCENE GENERATION COMPLETE: {GAME_NAME}")
    print(f"  Scenes:  {len(SCENE_FILES)}")
    print(f"  Scripts: {len(SCRIPT_FILES)}")
    print(f"  Total:   {len(generated)} files")
    print("  + project.godot patched (GameFlow autoload)")
    print("  ========================================")
    print()
    print("  Generated files:")
    for f in generated:
        print(f"    - {f}")
    print()
    print("  Game flow:")
    print("    MainMenu -> GalaxyMap -> PlanetMap -> Victory/Defeat")
    print("    GameFlow autoload handles transitions automatically.")
    print("    First-launch tutorial shown on first planet entry.")
    print()
    print("  All scenes ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
