"""
GATE DOMINION - UI Scene Generator
====================================
AI Role: AI_UI_DESIGNER

Generates all UI-related Godot .tscn scene files:
  - MainMenu.tscn   (New Game / Load Game / Quit)
  - HUD.tscn         (energy, minerals, selected unit info)
  - BuildMenu.tscn   (build PowerPlant / Factory / train Soldier)

Usage:
    python generate_ui.py <project_dir>
"""

import sys
import os


# ============================================================
#  CONFIGURATION
# ============================================================

GAME_NAME = "Gate Dominion"

# All UI scene files: (relative_path, generator_function_name)
UI_FILES = [
    ("scenes/main_menu.tscn",      "gen_main_menu"),
    ("scenes/galaxy/galaxy_map.tscn", "gen_galaxy_map_scene"),
    ("scenes/planet/planet_map.tscn", "gen_planet_map_scene"),
    ("ui/hud/hud.tscn",            "gen_hud"),
    ("ui/menus/build_menu.tscn",   "gen_build_menu"),
]


# ============================================================
#  TSCN GENERATORS
# ============================================================

def gen_main_menu():
    """Main menu scene — New Game, Load Game, Quit buttons."""
    return '''[gd_scene load_steps=2 format=3 uid="uid://main_menu"]

[ext_resource type="Script" path="res://scripts/core/main_menu.gd" id="1"]

[node name="MainMenu" type="Control"]
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
color = Color(0.05, 0.05, 0.12, 1)

[node name="VBox" type="VBoxContainer" parent="."]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -150.0
offset_top = -120.0
offset_right = 150.0
offset_bottom = 120.0
grow_horizontal = 2
grow_vertical = 2

[node name="Title" type="Label" parent="VBox"]
layout_mode = 2
text = "GATE DOMINION"
horizontal_alignment = 1
vertical_alignment = 1

[node name="Subtitle" type="Label" parent="VBox"]
layout_mode = 2
text = "Hybrid RTS + 4X Strategy"
horizontal_alignment = 1

[node name="Spacer" type="Control" parent="VBox"]
layout_mode = 2
custom_minimum_size = Vector2(0, 30)

[node name="NewGameBtn" type="Button" parent="VBox"]
layout_mode = 2
custom_minimum_size = Vector2(200, 40)
text = "New Game"

[node name="LoadGameBtn" type="Button" parent="VBox"]
layout_mode = 2
custom_minimum_size = Vector2(200, 40)
text = "Load Game"

[node name="QuitBtn" type="Button" parent="VBox"]
layout_mode = 2
custom_minimum_size = Vector2(200, 40)
text = "Quit"
'''


def gen_galaxy_map_scene():
    """Galaxy map scene — simple Control root with script."""
    return '''[gd_scene load_steps=2 format=3 uid="uid://galaxy_map"]

[ext_resource type="Script" path="res://scripts/galaxy/galaxy_map.gd" id="1"]

[node name="GalaxyMap" type="Control"]
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
color = Color(0.02, 0.02, 0.08, 1)

[node name="Title" type="Label" parent="."]
layout_mode = 1
offset_left = 500.0
offset_top = 20.0
offset_right = 780.0
offset_bottom = 50.0
text = "GALAXY MAP"
horizontal_alignment = 1
'''


def gen_planet_map_scene():
    """Planet map scene — Node2D root with PlanetMap script."""
    return '''[gd_scene load_steps=2 format=3 uid="uid://planet_map"]

[ext_resource type="Script" path="res://scripts/planet/planet_map.gd" id="1"]

[node name="PlanetMap" type="Node2D"]
script = ExtResource("1")

'''


def gen_hud():
    """HUD overlay — energy, minerals, selected unit info."""
    return '''[gd_scene load_steps=2 format=3 uid="uid://hud"]

[ext_resource type="Script" path="res://scripts/core/hud.gd" id="1"]

[node name="HUD" type="CanvasLayer"]
script = ExtResource("1")

[node name="TopBar" type="HBoxContainer" parent="."]
offset_left = 10.0
offset_top = 10.0
offset_right = 500.0
offset_bottom = 40.0

[node name="EnergyIcon" type="TextureRect" parent="TopBar"]
layout_mode = 2
custom_minimum_size = Vector2(24, 24)

[node name="EnergyLabel" type="Label" parent="TopBar"]
layout_mode = 2
text = "Energy: 100"

[node name="Spacer1" type="Control" parent="TopBar"]
layout_mode = 2
custom_minimum_size = Vector2(30, 0)

[node name="MineralIcon" type="TextureRect" parent="TopBar"]
layout_mode = 2
custom_minimum_size = Vector2(24, 24)

[node name="MineralsLabel" type="Label" parent="TopBar"]
layout_mode = 2
text = "Minerals: 50"

[node name="SelectionInfo" type="Label" parent="."]
offset_left = 10.0
offset_top = 50.0
offset_right = 300.0
offset_bottom = 70.0
text = "No unit selected"

[node name="ResultLabel" type="Label" parent="."]
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -100.0
offset_top = -30.0
offset_right = 100.0
offset_bottom = 30.0
horizontal_alignment = 1
vertical_alignment = 1
visible = false
'''


def gen_build_menu():
    """Build menu panel — buttons for PowerPlant, Factory, Soldier."""
    return '''[gd_scene load_steps=2 format=3 uid="uid://build_menu"]

[ext_resource type="Script" path="res://scripts/core/build_menu.gd" id="1"]

[node name="BuildMenu" type="PanelContainer"]
offset_left = 10.0
offset_top = 500.0
offset_right = 220.0
offset_bottom = 700.0
script = ExtResource("1")

[node name="VBox" type="VBoxContainer" parent="."]
layout_mode = 2

[node name="Title" type="Label" parent="VBox"]
layout_mode = 2
text = "BUILD MENU"
horizontal_alignment = 1

[node name="BuildPowerPlantBtn" type="Button" parent="VBox"]
layout_mode = 2
text = "Power Plant (50E)"

[node name="BuildFactoryBtn" type="Button" parent="VBox"]
layout_mode = 2
text = "Factory (100E)"

[node name="TrainSoldierBtn" type="Button" parent="VBox"]
layout_mode = 2
text = "Train Soldier (30E)"

[node name="Separator" type="HSeparator" parent="VBox"]
layout_mode = 2

[node name="BackToGalaxyBtn" type="Button" parent="VBox"]
layout_mode = 2
text = "Galaxy Map"
'''


# ============================================================
#  SUPPORTING SCRIPTS (scripts referenced by UI scenes)
# ============================================================

SUPPORT_SCRIPTS = [
    ("scripts/core/main_menu.gd",  "gen_main_menu_script"),
    ("scripts/core/hud.gd",        "gen_hud_script"),
    ("scripts/core/build_menu.gd", "gen_build_menu_script"),
]


def gen_main_menu_script():
    """GDScript for MainMenu scene."""
    return '''## MainMenu
## Handles main menu button presses.
extends Control


func _ready() -> void:
\tGameManager.change_state(GameManager.GameState.MAIN_MENU)
\t$VBox/NewGameBtn.pressed.connect(_on_new_game)
\t$VBox/LoadGameBtn.pressed.connect(_on_load_game)
\t$VBox/QuitBtn.pressed.connect(_on_quit)


func _on_new_game() -> void:
\tprint("[MainMenu] New Game")
\tEconomyManager.reset()
\tGameManager.change_state(GameManager.GameState.GALAXY_MAP)
\tget_tree().change_scene_to_file("res://scenes/galaxy/galaxy_map.tscn")


func _on_load_game() -> void:
\tprint("[MainMenu] Load Game")
\tif SaveManager.load_game():
\t\tGameManager.change_state(GameManager.GameState.GALAXY_MAP)
\t\tget_tree().change_scene_to_file("res://scenes/galaxy/galaxy_map.tscn")
\telse:
\t\tprint("[MainMenu] No save found.")


func _on_quit() -> void:
\tget_tree().quit()
'''


def gen_hud_script():
    """GDScript for HUD overlay."""
    return '''## HUD
## Updates resource displays and selection info each frame.
extends CanvasLayer


func _process(_delta: float) -> void:
\t# Update energy display
\tvar elbl = get_node_or_null("TopBar/EnergyLabel")
\tif elbl:
\t\telbl.text = "Energy: " + str(int(EconomyManager.energy))

\t# Update minerals display
\tvar mlbl = get_node_or_null("TopBar/MineralsLabel")
\tif mlbl:
\t\tmlbl.text = "Minerals: " + str(int(EconomyManager.minerals))
'''


def gen_build_menu_script():
    """GDScript for BuildMenu panel."""
    return '''## BuildMenu
## Connects build/train buttons to gameplay actions.
extends PanelContainer


func _ready() -> void:
\t$VBox/BuildPowerPlantBtn.pressed.connect(_on_build_power_plant)
\t$VBox/BuildFactoryBtn.pressed.connect(_on_build_factory)
\t$VBox/TrainSoldierBtn.pressed.connect(_on_train_soldier)
\t$VBox/BackToGalaxyBtn.pressed.connect(_on_back_to_galaxy)


func _on_build_power_plant() -> void:
\tvar rts = get_node_or_null("/root/PlanetMap/RTSController")
\tif rts:
\t\trts.call("start_build", "power_plant")
\t\tprint("[BuildMenu] Select location for Power Plant")


func _on_build_factory() -> void:
\tvar rts = get_node_or_null("/root/PlanetMap/RTSController")
\tif rts:
\t\trts.call("start_build", "factory")
\t\tprint("[BuildMenu] Select location for Factory")


func _on_train_soldier() -> void:
\t## Find first player factory and train a soldier.
\tvar factories = get_tree().get_nodes_in_group("player_structures")
\tfor f in factories:
\t\tif f.name.begins_with("Factory") and f.has_method("_on_produce_pressed"):
\t\t\tf.call("_on_produce_pressed")
\t\t\treturn
\tprint("[BuildMenu] No factory available!")


func _on_back_to_galaxy() -> void:
\tGameManager.return_to_galaxy()
'''


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
        print("Usage: python generate_ui.py <project_dir>")
        sys.exit(1)

    project_dir = os.path.abspath(sys.argv[1])
    print(f"  Project directory: {project_dir}")
    print(f"  Game: {GAME_NAME}")
    print()

    # --- Map generator names to functions ---
    scene_generators = {
        "gen_main_menu":        gen_main_menu,
        "gen_galaxy_map_scene": gen_galaxy_map_scene,
        "gen_planet_map_scene": gen_planet_map_scene,
        "gen_hud":              gen_hud,
        "gen_build_menu":       gen_build_menu,
    }

    script_generators = {
        "gen_main_menu_script":  gen_main_menu_script,
        "gen_hud_script":        gen_hud_script,
        "gen_build_menu_script": gen_build_menu_script,
    }

    generated = []

    # --- UI Scenes (.tscn) ---
    print("  Generating UI scenes...")
    for rel_path, gen_name in UI_FILES:
        gen_func = scene_generators.get(gen_name)
        if not gen_func:
            print(f"  WARNING: No generator '{gen_name}', skipping {rel_path}")
            continue
        content = gen_func()
        write_text(project_dir, rel_path, content)
        generated.append(rel_path)
        print(f"  [OK] {rel_path}")

    print()

    # --- Supporting GDScript files ---
    print("  Generating UI support scripts...")
    for rel_path, gen_name in SUPPORT_SCRIPTS:
        gen_func = script_generators.get(gen_name)
        if not gen_func:
            print(f"  WARNING: No generator '{gen_name}', skipping {rel_path}")
            continue
        content = gen_func()
        write_text(project_dir, rel_path, content)
        generated.append(rel_path)
        print(f"  [OK] {rel_path}")

    # --- Summary ---
    print()
    print("  ========================================")
    print(f"  UI GENERATION COMPLETE: {GAME_NAME}")
    print(f"  Scenes:  {len(UI_FILES)}")
    print(f"  Scripts: {len(SUPPORT_SCRIPTS)}")
    print(f"  Total:   {len(generated)} files")
    print("  ========================================")
    print()
    print("  Generated files:")
    for f in generated:
        print(f"    - {f}")
    print()
    print("  All UI ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
