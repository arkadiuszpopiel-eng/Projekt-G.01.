"""
GATE DOMINION - Game Data Generator
=====================================
AI Role: AI_DATA_DESIGNER

Generates all JSON configuration and balance data files that the game
reads at runtime: game settings, unit stats, structure stats, economy
balance, wave definitions, and difficulty presets.

Usage:
    python generate_data.py <project_dir>
"""

import sys
import os
import json


# ============================================================
#  CONFIGURATION
# ============================================================

GAME_NAME = "Gate Dominion"


# ============================================================
#  DATA DEFINITIONS
# ============================================================

def data_game_settings():
    """Master game settings — read by GameManager at startup."""
    return {
        "_comment": "Gate Dominion — master runtime settings",
        "game": {
            "name": "Gate Dominion",
            "version": "0.1.0-prototype",
            "default_faction": "tauri",
            "max_players": 2,
            "autosave_interval_seconds": 120,
            "victory_condition": "destroy_enemy_base",
            "defeat_condition": "lose_own_base"
        },
        "camera": {
            "pan_speed": 600,
            "zoom_min": 0.3,
            "zoom_max": 2.0,
            "zoom_step": 0.1,
            "edge_scroll_margin": 30,
            "shake_decay": 5.0
        },
        "display": {
            "window_width": 1280,
            "window_height": 720,
            "fullscreen": False,
            "vsync": True
        }
    }


def data_unit_stats():
    """Centralized unit stats — single source of truth for balance."""
    return {
        "_comment": "Unit stats — all values tunable here",
        "builder": {
            "hp": 80,
            "speed": 120,
            "damage": 0,
            "range": 0,
            "attack_speed": 0,
            "cost_energy": 0,
            "production_time": 0,
            "description": "Construction unit. Builds PowerPlants and Factories."
        },
        "soldier": {
            "hp": 120,
            "speed": 160,
            "damage": 15,
            "range": 80,
            "attack_speed": 1.0,
            "cost_energy": 30,
            "production_time": 5.0,
            "description": "Combat unit. Attacks enemy units and structures."
        }
    }


def data_structure_stats():
    """Centralized structure stats."""
    return {
        "_comment": "Structure stats — all values tunable here",
        "player_base": {
            "hp": 500,
            "cost_energy": 0,
            "cost_minerals": 0,
            "build_time": 0,
            "description": "Player starting base. Losing it means defeat."
        },
        "power_plant": {
            "hp": 300,
            "cost_energy": 50,
            "cost_minerals": 0,
            "build_time": 3.0,
            "energy_per_second": 5.0,
            "description": "Generates energy over time."
        },
        "factory": {
            "hp": 400,
            "cost_energy": 100,
            "cost_minerals": 0,
            "build_time": 5.0,
            "soldier_cost": 30,
            "production_time": 5.0,
            "description": "Produces Soldier units. Costs energy per unit."
        },
        "enemy_base": {
            "hp": 600,
            "description": "Enemy base. Destroying it wins the game."
        },
        "enemy_factory": {
            "hp": 400,
            "description": "Enemy factory. Produces enemy soldiers."
        }
    }


def data_economy_balance():
    """Economy tuning values."""
    return {
        "_comment": "Economy balance — starting resources and rates",
        "starting_resources": {
            "energy": 100,
            "minerals": 50
        },
        "costs": {
            "power_plant": 50,
            "factory": 100,
            "soldier": 30
        },
        "rates": {
            "power_plant_energy_per_sec": 5.0
        },
        "multipliers": {
            "easy":   {"cost_mult": 0.75, "income_mult": 1.25},
            "normal": {"cost_mult": 1.00, "income_mult": 1.00},
            "hard":   {"cost_mult": 1.25, "income_mult": 0.80}
        }
    }


def data_enemy_waves():
    """Enemy AI wave definitions — spawn timing and composition."""
    return {
        "_comment": "Enemy AI wave configuration",
        "ai_config": {
            "initial_spawn_delay": 3.0,
            "spawn_interval": 8.0,
            "attack_interval": 15.0,
            "max_soldiers": 20
        },
        "difficulty_scaling": {
            "easy": {
                "spawn_interval_mult": 1.5,
                "attack_interval_mult": 1.5,
                "enemy_hp_mult": 0.75,
                "enemy_damage_mult": 0.75
            },
            "normal": {
                "spawn_interval_mult": 1.0,
                "attack_interval_mult": 1.0,
                "enemy_hp_mult": 1.0,
                "enemy_damage_mult": 1.0
            },
            "hard": {
                "spawn_interval_mult": 0.7,
                "attack_interval_mult": 0.7,
                "enemy_hp_mult": 1.3,
                "enemy_damage_mult": 1.3
            }
        },
        "wave_templates": [
            {"wave": 1, "soldiers": 2,  "delay": 15.0},
            {"wave": 2, "soldiers": 3,  "delay": 30.0},
            {"wave": 3, "soldiers": 5,  "delay": 50.0},
            {"wave": 4, "soldiers": 7,  "delay": 75.0},
            {"wave": 5, "soldiers": 10, "delay": 100.0}
        ]
    }


def data_galaxy():
    """Default galaxy layout — planet positions, names, ownership."""
    return {
        "_comment": "Galaxy map layout — default planet configuration",
        "planets": [
            {
                "id": 0,
                "name": "Terra Prime",
                "position": [200, 300],
                "owner": "player",
                "description": "Humanity's first offworld colony. Rich in Naquadah."
            },
            {
                "id": 1,
                "name": "Kesh'ra",
                "position": [500, 200],
                "owner": "enemy",
                "description": "Goa'uld-occupied world. Fortified and hostile."
            },
            {
                "id": 2,
                "name": "Novalith",
                "position": [800, 350],
                "owner": "neutral",
                "description": "Uncharted planet. Ancient ruins detected."
            }
        ],
        "stargate_connections": [
            [0, 1],
            [1, 2]
        ]
    }


def data_input_map():
    """Input action reference — documents the input map from project.godot."""
    return {
        "_comment": "Input action reference — matches project.godot [input] section",
        "actions": {
            "select":          {"key": "Left Mouse Button", "description": "Select unit or place building"},
            "command":         {"key": "Right Mouse Button", "description": "Move/attack command"},
            "camera_up":       {"key": "W",                  "description": "Pan camera up"},
            "camera_down":     {"key": "S",                  "description": "Pan camera down"},
            "camera_left":     {"key": "A",                  "description": "Pan camera left"},
            "camera_right":    {"key": "D",                  "description": "Pan camera right"},
            "camera_zoom_in":  {"key": "Mouse Wheel Up",     "description": "Zoom in"},
            "camera_zoom_out": {"key": "Mouse Wheel Down",   "description": "Zoom out"}
        }
    }


# ============================================================
#  FILE TABLE
# ============================================================

DATA_FILES = [
    ("data/game_settings.json",     data_game_settings),
    ("data/unit_stats.json",        data_unit_stats),
    ("data/structure_stats.json",   data_structure_stats),
    ("data/economy_balance.json",   data_economy_balance),
    ("data/enemy_waves.json",       data_enemy_waves),
    ("data/galaxy.json",            data_galaxy),
    ("data/input_map.json",         data_input_map),
]


# ============================================================
#  FILE WRITER
# ============================================================

def write_json(project_dir, relative_path, data):
    """Write a JSON file with pretty-printing."""
    full_path = os.path.join(project_dir, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return full_path


# ============================================================
#  MAIN
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_data.py <project_dir>")
        sys.exit(1)

    project_dir = os.path.abspath(sys.argv[1])
    print(f"  Project directory: {project_dir}")
    print(f"  Game: {GAME_NAME}")
    print()
    print("  Generating game data files...")

    generated = []

    for rel_path, gen_func in DATA_FILES:
        data = gen_func()
        write_json(project_dir, rel_path, data)
        generated.append(rel_path)
        print(f"  [OK] {rel_path}")

    # --- Summary ---
    print()
    print("  ========================================")
    print(f"  DATA GENERATION COMPLETE: {GAME_NAME}")
    print(f"  Files: {len(generated)}")
    print("  ========================================")
    print()
    print("  Generated files:")
    for f in generated:
        print(f"    - {f}")
    print()
    print("  All game data ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
