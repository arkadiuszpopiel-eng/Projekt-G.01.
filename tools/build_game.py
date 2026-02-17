"""
GATE DOMINION - Build & Launch Script
=======================================
AI Role: AI_BUILD_ENGINEER

Final pipeline step. Validates the project, optionally exports
a build, and prepares for launch.

Usage:
    python build_game.py <project_dir> <godot_exe> <build_dir>
"""

import sys
import os
import subprocess


# ============================================================
#  CONFIGURATION
# ============================================================

GAME_NAME = "Gate Dominion"

# Critical files that must exist for the game to run
REQUIRED_FILES = [
    "project.godot",
    "scenes/main_menu.tscn",
    "scenes/galaxy/galaxy_map.tscn",
    "scenes/planet/planet_map.tscn",
    "scripts/core/game_manager.gd",
    "scripts/core/main_menu.gd",
    "scripts/economy/economy_manager.gd",
    "scripts/stargate/stargate_manager.gd",
    "scripts/core/save_manager.gd",
    "scripts/core/game_flow.gd",
    "scripts/planet/planet_map.gd",
    "scripts/galaxy/galaxy_map.gd",
    "scripts/units/builder_unit.gd",
    "scripts/units/soldier_unit.gd",
    "scripts/structures/power_plant.gd",
    "scripts/structures/factory.gd",
    "scripts/ai_enemy/enemy_ai.gd",
]


# ============================================================
#  VALIDATION
# ============================================================

def validate_project(project_dir):
    """Check that all critical files exist."""
    print("  Validating project integrity...")
    missing = []
    for rel_path in REQUIRED_FILES:
        full = os.path.join(project_dir, rel_path)
        if not os.path.exists(full):
            missing.append(rel_path)

    if missing:
        print(f"  WARNING: {len(missing)} required file(s) missing:")
        for m in missing:
            print(f"    MISSING: {m}")
        return False

    print(f"  All {len(REQUIRED_FILES)} critical files verified.")
    return True


def count_project_files(project_dir):
    """Count total generated files for summary."""
    counts = {"gd": 0, "tscn": 0, "json": 0, "png": 0, "wav": 0, "tres": 0, "other": 0}
    total = 0
    for root, _dirs, files in os.walk(project_dir):
        for f in files:
            total += 1
            ext = os.path.splitext(f)[1].lower().lstrip(".")
            if ext in counts:
                counts[ext] += 1
            else:
                counts["other"] += 1
    return total, counts


# ============================================================
#  EXPORT (optional)
# ============================================================

def try_export(project_dir, godot_exe, build_dir):
    """Attempt to export the project using Godot CLI. Non-fatal if it fails."""
    if not godot_exe or not os.path.exists(godot_exe):
        print("  Godot executable not found — skipping export.")
        return False

    os.makedirs(build_dir, exist_ok=True)
    export_path = os.path.join(build_dir, "GateDominion.exe")

    print(f"  Attempting export to: {export_path}")
    try:
        result = subprocess.run(
            [godot_exe, "--headless", "--path", project_dir,
             "--export-release", "Windows Desktop", export_path],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and os.path.exists(export_path):
            size_mb = os.path.getsize(export_path) / (1024 * 1024)
            print(f"  Export successful: {export_path} ({size_mb:.1f} MB)")
            return True
        else:
            print("  Export returned non-zero or no output file.")
            if result.stderr:
                # Show only first 5 lines of error
                lines = result.stderr.strip().split("\n")[:5]
                for line in lines:
                    print(f"    {line}")
            return False
    except subprocess.TimeoutExpired:
        print("  Export timed out (120s). Skipping.")
        return False
    except Exception as e:
        print(f"  Export failed: {e}")
        return False


# ============================================================
#  IMPORT SCAN (warm up .godot cache)
# ============================================================

def try_import(project_dir, godot_exe):
    """Run Godot --import to generate .import files. Non-fatal."""
    if not godot_exe or not os.path.exists(godot_exe):
        return False

    print("  Running Godot import scan (generating .import cache)...")
    try:
        result = subprocess.run(
            [godot_exe, "--headless", "--path", project_dir, "--import"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            print("  Import scan complete.")
            return True
        else:
            print("  Import scan returned non-zero (non-fatal).")
            return False
    except subprocess.TimeoutExpired:
        print("  Import scan timed out (non-fatal).")
        return False
    except Exception:
        print("  Import scan failed (non-fatal).")
        return False


# ============================================================
#  MAIN
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python build_game.py <project_dir> [godot_exe] [build_dir]")
        sys.exit(1)

    project_dir = os.path.abspath(sys.argv[1])
    godot_exe   = sys.argv[2] if len(sys.argv) > 2 else None
    build_dir   = sys.argv[3] if len(sys.argv) > 3 else os.path.join(
                      os.path.dirname(project_dir), "build")

    print(f"  Project directory: {project_dir}")
    print(f"  Godot executable:  {godot_exe or '(not provided)'}")
    print(f"  Build directory:   {build_dir}")
    print()

    # === 1. Validate ===
    valid = validate_project(project_dir)
    print()

    # === 2. File summary ===
    total, counts = count_project_files(project_dir)
    print(f"  Project file summary:")
    print(f"    GDScript (.gd):   {counts['gd']}")
    print(f"    Scenes (.tscn):   {counts['tscn']}")
    print(f"    Data (.json):     {counts['json']}")
    print(f"    Textures (.png):  {counts['png']}")
    print(f"    Audio (.wav):     {counts['wav']}")
    print(f"    Resources (.tres):{counts['tres']}")
    print(f"    Other:            {counts['other']}")
    print(f"    TOTAL:            {total}")
    print()

    # === 3. Import scan ===
    if godot_exe:
        try_import(project_dir, godot_exe)
        print()

    # === 4. Try export ===
    exported = False
    if godot_exe:
        exported = try_export(project_dir, godot_exe, build_dir)
        print()

    # === 5. Final summary ===
    print("  ========================================")
    print(f"  BUILD COMPLETE: {GAME_NAME}")
    print(f"  Validation:  {'PASSED' if valid else 'WARNINGS'}")
    print(f"  Total files: {total}")
    print(f"  Export:      {'SUCCESS' if exported else 'SKIPPED (run from editor)'}")
    print("  ========================================")
    print()

    if not exported:
        print("  The game can be launched directly with Godot:")
        print(f"    godot --path \"{project_dir}\"")
        print()

    print("  Build pipeline complete. Ready to play!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
