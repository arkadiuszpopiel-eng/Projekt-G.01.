"""
GATE DOMINION - Faction & Technology Generator
================================================
AI Role: AI_GAME_DESIGNER + AI_DATA_ARCHITECT

Generates complete faction definitions and technology trees for
6 playable factions.  Each faction has unique identity, economy
modifiers, unit roster, building roster, and a 5-tier tech tree.

Output (12 JSON files):
  data/factions/tauri.json        data/tech/tauri_tech.json
  data/factions/goauld.json       data/tech/goauld_tech.json
  data/factions/jaffa.json        data/tech/jaffa_tech.json
  data/factions/asgard.json       data/tech/asgard_tech.json
  data/factions/wraith.json       data/tech/wraith_tech.json
  data/factions/ancients.json     data/tech/ancients_tech.json

Usage:
    python generate_factions_and_tech.py <project_dir>
"""

import sys
import os
import json


# ============================================================
#  CONFIGURATION
# ============================================================

GAME_NAME = "Gate Dominion"

FACTION_IDS = ["tauri", "goauld", "jaffa", "asgard", "wraith", "ancients"]


# ============================================================
#  FACTION DEFINITIONS
# ============================================================

def def_tauri():
    """Tau'ri (Human Earth) — balanced, adaptable, tech-focused."""
    return {
        "id": "tauri",
        "name": "Tau'ri",
        "full_name": "Tau'ri — United Earth Command",
        "description": (
            "Humans of Earth. Resourceful, adaptable, and determined. "
            "They lack the raw power of alien races but compensate with "
            "ingenuity, teamwork, and rapidly advancing technology "
            "reverse-engineered from alien artifacts."
        ),
        "color_palette": {
            "primary":   "#3A7BDF",
            "secondary": "#1E4A8A",
            "accent":    "#7EB8FF",
            "ui_bg":     "#0D1B33"
        },
        "traits": [
            "Adaptive — research speed +15%",
            "Resourceful — all buildings cost -10%",
            "United — allied units gain +5% damage near base"
        ],
        "bonuses": {
            "research_speed_mult": 1.15,
            "building_cost_mult":  0.90,
            "ally_damage_aura":    0.05
        },
        "weaknesses": [
            "Low base unit HP compared to alien factions",
            "No innate energy generation — fully reliant on power plants",
            "Slow early game without tech investment"
        ],
        "starting_conditions": {
            "energy":   120,
            "minerals": 80,
            "units":    ["sg_team"],
            "buildings":["command_center"]
        },
        "lore_quote": "We don't back down. Not now. Not ever. — General O'Neill",

        # ---- Buildings ----
        "buildings": [
            {
                "id": "command_center",
                "name": "SGC Command Center",
                "description": "Central base of operations. Houses the Stargate and coordinates all planetary activity.",
                "hp": 800,
                "cost_energy": 0,
                "cost_minerals": 0,
                "build_time": 0,
                "provides": ["base", "stargate_node"],
                "unique": False
            },
            {
                "id": "naquadah_reactor",
                "name": "Naquadah Reactor",
                "description": "Compact reactor powered by refined Naquadah. Generates steady energy.",
                "hp": 300,
                "cost_energy": 0,
                "cost_minerals": 60,
                "build_time": 8.0,
                "provides": ["energy"],
                "energy_per_second": 6.0,
                "unique": False
            },
            {
                "id": "armory",
                "name": "Armory & Barracks",
                "description": "Trains infantry and stores equipment. Produces SG teams and Marines.",
                "hp": 400,
                "cost_energy": 80,
                "cost_minerals": 50,
                "build_time": 10.0,
                "provides": ["unit_production"],
                "produces": ["sg_team", "marine", "sniper", "hazmat_trooper"],
                "unique": False
            },
            {
                "id": "stargate_node",
                "name": "Stargate",
                "description": "Ancient ring allowing instantaneous travel between planets.",
                "hp": 1000,
                "cost_energy": 0,
                "cost_minerals": 0,
                "build_time": 0,
                "provides": ["stargate"],
                "unique": True
            },
            {
                "id": "area51_lab",
                "name": "Area 51 Research Lab",
                "description": "Top-secret facility for reverse-engineering alien technology. Greatly accelerates research.",
                "hp": 350,
                "cost_energy": 120,
                "cost_minerals": 100,
                "build_time": 15.0,
                "provides": ["research_boost"],
                "research_speed_bonus": 0.25,
                "unique": True
            },
            {
                "id": "f302_hangar",
                "name": "F-302 Hangar",
                "description": "Launch bay for F-302 interceptors. Required for air superiority.",
                "hp": 450,
                "cost_energy": 150,
                "cost_minerals": 120,
                "build_time": 18.0,
                "provides": ["air_production"],
                "produces": ["f302"],
                "unique": False
            }
        ],

        # ---- Units ----
        "units": [
            {
                "id": "sg_team",
                "name": "SG Team",
                "role": "light_infantry",
                "description": "Four-person reconnaissance and assault team. Versatile and fast.",
                "hp": 100,
                "damage": 12,
                "attack_speed": 1.0,
                "range": 90,
                "speed": 170,
                "cost_energy": 25,
                "production_time": 4.0,
                "abilities": ["stealth_recon"]
            },
            {
                "id": "marine",
                "name": "Marine Squad",
                "role": "heavy_infantry",
                "description": "Heavily armed USMC squad. Tough and reliable frontline fighters.",
                "hp": 160,
                "damage": 18,
                "attack_speed": 1.2,
                "range": 70,
                "speed": 130,
                "cost_energy": 40,
                "production_time": 6.0,
                "abilities": ["fortify"]
            },
            {
                "id": "sniper",
                "name": "Sniper Operative",
                "role": "ranged",
                "description": "Long-range specialist. High damage, fragile, excellent against key targets.",
                "hp": 60,
                "damage": 45,
                "attack_speed": 2.5,
                "range": 200,
                "speed": 140,
                "cost_energy": 50,
                "production_time": 7.0,
                "abilities": ["critical_shot"]
            },
            {
                "id": "f302",
                "name": "F-302 Interceptor",
                "role": "air",
                "description": "Hybrid-technology fighter craft. Fast, deadly against ground and air.",
                "hp": 120,
                "damage": 22,
                "attack_speed": 0.8,
                "range": 110,
                "speed": 280,
                "cost_energy": 80,
                "production_time": 12.0,
                "abilities": ["strafe_run"]
            },
            {
                "id": "hazmat_trooper",
                "name": "HAZMAT Trooper",
                "role": "elite",
                "description": "Specialist equipped with experimental alien-tech weapons. Area damage.",
                "hp": 140,
                "damage": 30,
                "attack_speed": 1.5,
                "range": 80,
                "speed": 120,
                "cost_energy": 70,
                "production_time": 10.0,
                "abilities": ["emp_grenade"]
            },
            {
                "id": "prometheus",
                "name": "Prometheus (BC-303)",
                "role": "super",
                "description": "Earth's first interstellar battlecruiser. Massive firepower and shields.",
                "hp": 800,
                "damage": 60,
                "attack_speed": 2.0,
                "range": 150,
                "speed": 80,
                "cost_energy": 300,
                "production_time": 40.0,
                "abilities": ["orbital_strike", "shield_generator"],
                "requires_tech": "tier5_earth_fleet"
            }
        ]
    }


def def_goauld():
    """Goa'uld Empire — aggressive, slave-driven economy, powerful but arrogant."""
    return {
        "id": "goauld",
        "name": "Goa'uld",
        "full_name": "Goa'uld Empire — System Lords",
        "description": (
            "Parasitic race posing as gods. The Goa'uld command vast armies "
            "of Jaffa slaves and wield devastating energy weapons. Their "
            "arrogance is matched only by their cruelty and ambition."
        ),
        "color_palette": {
            "primary":   "#D4A017",
            "secondary": "#8B6914",
            "accent":    "#FFD700",
            "ui_bg":     "#1A1200"
        },
        "traits": [
            "Slave Economy — units cost -20% but have -10% loyalty",
            "God Complex — morale aura around System Lord unit",
            "Naquadah Rich — energy generation +20%"
        ],
        "bonuses": {
            "unit_cost_mult":       0.80,
            "energy_gen_mult":      1.20,
            "morale_aura_range":    120
        },
        "weaknesses": [
            "Slow research — arrogance hinders innovation",
            "Slave rebellions possible if morale drops",
            "Over-reliance on Jaffa ground forces"
        ],
        "starting_conditions": {
            "energy":   150,
            "minerals": 60,
            "units":    ["jaffa_warrior"],
            "buildings":["pyramid_base"]
        },
        "lore_quote": "Kneel before your god! — Apophis",

        "buildings": [
            {
                "id": "pyramid_base",
                "name": "Pyramid Stronghold",
                "description": "Imposing pyramid serving as seat of power and Stargate hub.",
                "hp": 900,
                "cost_energy": 0, "cost_minerals": 0, "build_time": 0,
                "provides": ["base", "stargate_node"], "unique": False
            },
            {
                "id": "naquadah_mine",
                "name": "Naquadah Mine",
                "description": "Slave-operated mine extracting raw Naquadah for energy.",
                "hp": 280,
                "cost_energy": 0, "cost_minerals": 50, "build_time": 7.0,
                "provides": ["energy"], "energy_per_second": 7.0, "unique": False
            },
            {
                "id": "jaffa_barracks",
                "name": "Jaffa Barracks",
                "description": "Training grounds for Jaffa soldiers loyal to their god.",
                "hp": 420,
                "cost_energy": 70, "cost_minerals": 40, "build_time": 9.0,
                "provides": ["unit_production"],
                "produces": ["jaffa_warrior", "jaffa_elite", "ashrak"],
                "unique": False
            },
            {
                "id": "goauld_stargate",
                "name": "Chappa'ai",
                "description": "The sacred ring — gateway between worlds.",
                "hp": 1000,
                "cost_energy": 0, "cost_minerals": 0, "build_time": 0,
                "provides": ["stargate"], "unique": True
            },
            {
                "id": "sarcophagus_chamber",
                "name": "Sarcophagus Chamber",
                "description": "Ancient healing device. Resurrects fallen elite units and heals all nearby units.",
                "hp": 350,
                "cost_energy": 100, "cost_minerals": 80, "build_time": 14.0,
                "provides": ["healing", "resurrect"],
                "heal_per_second": 3.0,
                "unique": True
            },
            {
                "id": "hatak_shipyard",
                "name": "Ha'tak Shipyard",
                "description": "Orbital construction platform for Ha'tak motherships.",
                "hp": 500,
                "cost_energy": 200, "cost_minerals": 150, "build_time": 20.0,
                "provides": ["air_production"],
                "produces": ["death_glider", "hatak"],
                "unique": False
            }
        ],

        "units": [
            {
                "id": "jaffa_warrior",
                "name": "Jaffa Warrior",
                "role": "light_infantry",
                "description": "Staff-weapon-wielding foot soldier. Cheap and expendable.",
                "hp": 110,
                "damage": 14,
                "attack_speed": 1.1,
                "range": 80,
                "speed": 150,
                "cost_energy": 20,
                "production_time": 3.5,
                "abilities": []
            },
            {
                "id": "jaffa_elite",
                "name": "Jaffa First Prime",
                "role": "heavy_infantry",
                "description": "Veteran warrior with superior armor and a ceremonial staff cannon.",
                "hp": 200,
                "damage": 22,
                "attack_speed": 1.3,
                "range": 75,
                "speed": 120,
                "cost_energy": 50,
                "production_time": 7.0,
                "abilities": ["rally_cry"]
            },
            {
                "id": "ashrak",
                "name": "Ashrak Assassin",
                "role": "ranged",
                "description": "Invisible infiltrator. Devastating first strike, fragile in prolonged combat.",
                "hp": 70,
                "damage": 55,
                "attack_speed": 2.8,
                "range": 60,
                "speed": 190,
                "cost_energy": 60,
                "production_time": 9.0,
                "abilities": ["cloak", "assassinate"]
            },
            {
                "id": "death_glider",
                "name": "Death Glider",
                "role": "air",
                "description": "Twin-seat attack craft. Fast strafing runs against ground targets.",
                "hp": 100,
                "damage": 20,
                "attack_speed": 0.7,
                "range": 100,
                "speed": 300,
                "cost_energy": 70,
                "production_time": 10.0,
                "abilities": ["strafe_run"]
            },
            {
                "id": "kull_warrior",
                "name": "Kull Warrior",
                "role": "elite",
                "description": "Anubis-engineered super-soldier. Nearly indestructible, wrist blasters.",
                "hp": 300,
                "damage": 35,
                "attack_speed": 1.2,
                "range": 70,
                "speed": 100,
                "cost_energy": 100,
                "production_time": 14.0,
                "abilities": ["energy_absorb"]
            },
            {
                "id": "hatak",
                "name": "Ha'tak Mothership",
                "role": "super",
                "description": "Massive pyramidal warship. Orbital bombardment and troop deployment.",
                "hp": 1000,
                "damage": 80,
                "attack_speed": 2.5,
                "range": 180,
                "speed": 60,
                "cost_energy": 350,
                "production_time": 50.0,
                "abilities": ["orbital_bombardment", "deploy_troops"],
                "requires_tech": "tier5_fleet_dominion"
            }
        ]
    }


def def_jaffa():
    """Jaffa Nation — rebellion-born, honor-driven warriors."""
    return {
        "id": "jaffa",
        "name": "Free Jaffa",
        "full_name": "Free Jaffa Nation",
        "description": (
            "Former slaves of the Goa'uld who won their freedom through "
            "rebellion. The Jaffa are proud warriors with deep honor codes. "
            "They lack advanced technology but excel in raw combat prowess "
            "and unbreakable morale."
        ),
        "color_palette": {
            "primary":   "#C0392B",
            "secondary": "#7B241C",
            "accent":    "#F1948A",
            "ui_bg":     "#1C0B08"
        },
        "traits": [
            "Warriors Born — all infantry +15% melee damage",
            "Tretonin Supply — units slowly regenerate HP",
            "Free Will — immune to morale debuffs"
        ],
        "bonuses": {
            "melee_damage_mult":  1.15,
            "hp_regen_per_sec":   1.0,
            "morale_immunity":    True
        },
        "weaknesses": [
            "Very limited air units",
            "Research speed -20% (limited scientists)",
            "Expensive advanced buildings"
        ],
        "starting_conditions": {
            "energy":   100,
            "minerals": 100,
            "units":    ["jaffa_rebel"],
            "buildings":["rebel_camp"]
        },
        "lore_quote": "I die free. — Teal'c",

        "buildings": [
            {
                "id": "rebel_camp",
                "name": "Rebel Command Camp",
                "description": "Heart of the Free Jaffa movement. Rugged but effective.",
                "hp": 700,
                "cost_energy": 0, "cost_minerals": 0, "build_time": 0,
                "provides": ["base", "stargate_node"], "unique": False
            },
            {
                "id": "tretonin_lab",
                "name": "Tretonin Synthesizer",
                "description": "Produces Tretonin serum, freeing Jaffa from symbiote dependency and boosting regen.",
                "hp": 300,
                "cost_energy": 0, "cost_minerals": 70, "build_time": 10.0,
                "provides": ["energy"], "energy_per_second": 5.0, "unique": False
            },
            {
                "id": "warrior_hall",
                "name": "Warrior Hall",
                "description": "Sacred training grounds where young Jaffa earn their marks.",
                "hp": 450,
                "cost_energy": 60, "cost_minerals": 50, "build_time": 9.0,
                "provides": ["unit_production"],
                "produces": ["jaffa_rebel", "jaffa_veteran", "mastaba_guard"],
                "unique": False
            },
            {
                "id": "jaffa_stargate",
                "name": "Liberated Chappa'ai",
                "description": "A Stargate reclaimed from the Goa'uld. Symbol of freedom.",
                "hp": 1000,
                "cost_energy": 0, "cost_minerals": 0, "build_time": 0,
                "provides": ["stargate"], "unique": True
            },
            {
                "id": "rite_of_malshuraan",
                "name": "Rite of M'al Sharran",
                "description": "Sacred ritual site. Permanently boosts nearby warriors' combat stats.",
                "hp": 400,
                "cost_energy": 90, "cost_minerals": 110, "build_time": 16.0,
                "provides": ["combat_aura"],
                "combat_bonus": 0.10,
                "unique": True
            },
            {
                "id": "alkesh_pad",
                "name": "Al'kesh Landing Pad",
                "description": "Captured Goa'uld mid-range bomber platform.",
                "hp": 400,
                "cost_energy": 130, "cost_minerals": 100, "build_time": 16.0,
                "provides": ["air_production"],
                "produces": ["alkesh"],
                "unique": False
            }
        ],

        "units": [
            {
                "id": "jaffa_rebel",
                "name": "Jaffa Rebel",
                "role": "light_infantry",
                "description": "Freed warrior armed with a staff weapon. Fast and fierce.",
                "hp": 120,
                "damage": 15, "attack_speed": 1.0, "range": 75, "speed": 165,
                "cost_energy": 20, "production_time": 3.0,
                "abilities": ["battle_cry"]
            },
            {
                "id": "jaffa_veteran",
                "name": "Jaffa Veteran",
                "role": "heavy_infantry",
                "description": "Battle-hardened warrior with heavy staff cannon and ceremonial armor.",
                "hp": 220,
                "damage": 24, "attack_speed": 1.3, "range": 70, "speed": 115,
                "cost_energy": 50, "production_time": 7.0,
                "abilities": ["last_stand"]
            },
            {
                "id": "mastaba_guard",
                "name": "Mastaba Guard",
                "role": "ranged",
                "description": "Elite temple guard with modified long-range staff. Accurate and deadly.",
                "hp": 90,
                "damage": 38, "attack_speed": 2.0, "range": 170, "speed": 130,
                "cost_energy": 55, "production_time": 8.0,
                "abilities": ["overwatch"]
            },
            {
                "id": "alkesh",
                "name": "Al'kesh Bomber",
                "role": "air",
                "description": "Captured mid-range bomber. Slow but devastating area damage.",
                "hp": 150,
                "damage": 35, "attack_speed": 2.0, "range": 90, "speed": 180,
                "cost_energy": 90, "production_time": 14.0,
                "abilities": ["carpet_bomb"]
            },
            {
                "id": "sodan_warrior",
                "name": "Sodan Warrior",
                "role": "elite",
                "description": "Ancient order of invisible warriors. Masters of ambush tactics.",
                "hp": 160,
                "damage": 40, "attack_speed": 1.0, "range": 50, "speed": 200,
                "cost_energy": 80, "production_time": 12.0,
                "abilities": ["cloak", "ambush_strike"]
            },
            {
                "id": "hatak_captured",
                "name": "Captured Ha'tak",
                "role": "super",
                "description": "A stolen Goa'uld mothership. Less refined but still devastating.",
                "hp": 850,
                "damage": 65, "attack_speed": 2.5, "range": 160, "speed": 55,
                "cost_energy": 320, "production_time": 48.0,
                "abilities": ["orbital_bombardment"],
                "requires_tech": "tier5_liberation_fleet"
            }
        ]
    }


def def_asgard():
    """Asgard — advanced, few but powerful, energy-based economy."""
    return {
        "id": "asgard",
        "name": "Asgard",
        "full_name": "Asgard Confederation",
        "description": (
            "An ancient and highly advanced race of small grey beings. "
            "The Asgard possess technology millennia beyond most races "
            "but suffer from genetic degradation. Few in number, each "
            "unit is extraordinarily powerful."
        ),
        "color_palette": {
            "primary":   "#A0A0C0",
            "secondary": "#606080",
            "accent":    "#D0D0FF",
            "ui_bg":     "#0E0E1A"
        },
        "traits": [
            "Superior Technology — all units have energy shields",
            "Cloning — lost elite units can be re-cloned at half cost",
            "Beaming — instant unit teleportation within range"
        ],
        "bonuses": {
            "shield_hp_base":    50,
            "clone_cost_mult":   0.50,
            "beam_range":        200
        },
        "weaknesses": [
            "Very expensive units and buildings",
            "Slow production — small army size",
            "Vulnerable to EMP and anti-shield weapons"
        ],
        "starting_conditions": {
            "energy":   200,
            "minerals": 40,
            "units":    ["asgard_drone"],
            "buildings":["asgard_hub"]
        },
        "lore_quote": "We are the Asgard. — Thor",

        "buildings": [
            {
                "id": "asgard_hub",
                "name": "Asgard Science Hub",
                "description": "Pristine white facility serving as command center and research node.",
                "hp": 1000,
                "cost_energy": 0, "cost_minerals": 0, "build_time": 0,
                "provides": ["base", "stargate_node", "research_boost"],
                "research_speed_bonus": 0.15,
                "unique": False
            },
            {
                "id": "neutrino_core",
                "name": "Neutrino-Ion Generator",
                "description": "Advanced power source producing massive energy output.",
                "hp": 350,
                "cost_energy": 0, "cost_minerals": 80, "build_time": 10.0,
                "provides": ["energy"], "energy_per_second": 10.0, "unique": False
            },
            {
                "id": "replication_bay",
                "name": "Replication Bay",
                "description": "Constructs Asgard units via matter replication. Slow but precise.",
                "hp": 500,
                "cost_energy": 120, "cost_minerals": 80, "build_time": 14.0,
                "provides": ["unit_production"],
                "produces": ["asgard_drone", "asgard_guardian", "vanir_soldier"],
                "unique": False
            },
            {
                "id": "asgard_stargate",
                "name": "Asgard Transport Array",
                "description": "Enhanced Stargate with beaming technology overlay.",
                "hp": 1200,
                "cost_energy": 0, "cost_minerals": 0, "build_time": 0,
                "provides": ["stargate", "beam_transport"], "unique": True
            },
            {
                "id": "time_dilation_field",
                "name": "Time Dilation Device",
                "description": "Slows all enemy units within a wide radius. Immensely powerful defense.",
                "hp": 400,
                "cost_energy": 200, "cost_minerals": 150, "build_time": 22.0,
                "provides": ["area_slow"],
                "slow_factor": 0.50,
                "slow_radius": 200,
                "unique": True
            },
            {
                "id": "beliskner_dock",
                "name": "Beliskner-class Dock",
                "description": "Orbital dock for Asgard capital ships.",
                "hp": 600,
                "cost_energy": 250, "cost_minerals": 200, "build_time": 25.0,
                "provides": ["air_production"],
                "produces": ["asgard_fighter", "beliskner"],
                "unique": False
            }
        ],

        "units": [
            {
                "id": "asgard_drone",
                "name": "Asgard Drone",
                "role": "light_infantry",
                "description": "Autonomous combat drone with energy beam. Shielded.",
                "hp": 80, "shield": 60,
                "damage": 18, "attack_speed": 0.9, "range": 100, "speed": 160,
                "cost_energy": 40, "production_time": 5.0,
                "abilities": ["energy_shield"]
            },
            {
                "id": "asgard_guardian",
                "name": "Asgard Guardian",
                "role": "heavy_infantry",
                "description": "Heavy combat platform with twin plasma cannons and layered shields.",
                "hp": 150, "shield": 120,
                "damage": 28, "attack_speed": 1.4, "range": 85, "speed": 100,
                "cost_energy": 80, "production_time": 10.0,
                "abilities": ["energy_shield", "overcharge"]
            },
            {
                "id": "vanir_soldier",
                "name": "Vanir Battlesuit",
                "role": "ranged",
                "description": "Asgard in a powered exosuit. Long-range particle beam.",
                "hp": 100, "shield": 80,
                "damage": 42, "attack_speed": 2.2, "range": 180, "speed": 120,
                "cost_energy": 90, "production_time": 12.0,
                "abilities": ["energy_shield", "precision_beam"]
            },
            {
                "id": "asgard_fighter",
                "name": "Asgard Fighter Drone",
                "role": "air",
                "description": "Unmanned fighter with plasma weapons. Fast and shielded.",
                "hp": 90, "shield": 70,
                "damage": 24, "attack_speed": 0.8, "range": 120, "speed": 310,
                "cost_energy": 100, "production_time": 12.0,
                "abilities": ["energy_shield", "evasion"]
            },
            {
                "id": "thor_avatar",
                "name": "Thor's Avatar",
                "role": "elite",
                "description": "Holographic battle avatar of Supreme Commander Thor. Inspires and devastates.",
                "hp": 200, "shield": 200,
                "damage": 50, "attack_speed": 1.5, "range": 100, "speed": 140,
                "cost_energy": 150, "production_time": 18.0,
                "abilities": ["energy_shield", "inspire", "beam_teleport"]
            },
            {
                "id": "beliskner",
                "name": "Beliskner-class Warship",
                "role": "super",
                "description": "Asgard capital ship. Unmatched shields and the devastating Hammer weapon.",
                "hp": 600, "shield": 600,
                "damage": 90, "attack_speed": 2.0, "range": 200, "speed": 70,
                "cost_energy": 400, "production_time": 55.0,
                "abilities": ["hammer_weapon", "beam_transport", "energy_shield"],
                "requires_tech": "tier5_asgard_ascendancy"
            }
        ]
    }


def def_wraith():
    """Wraith — bio-organic, feeding-based economy, swarm tactics."""
    return {
        "id": "wraith",
        "name": "Wraith",
        "full_name": "Wraith Hive Collective",
        "description": (
            "Terrifying bio-organic predators from the Pegasus galaxy. "
            "The Wraith feed on the life force of other beings and grow "
            "their technology from living tissue. Overwhelming numbers "
            "and life-drain abilities make them a nightmare opponent."
        ),
        "color_palette": {
            "primary":   "#2ECC71",
            "secondary": "#1A7A42",
            "accent":    "#82E0AA",
            "ui_bg":     "#0A1F10"
        },
        "traits": [
            "Life Drain — melee attacks heal the attacker",
            "Hive Growth — structures regenerate HP slowly",
            "Swarm — unit production speed +25%"
        ],
        "bonuses": {
            "life_drain_percent":      0.30,
            "structure_regen_per_sec": 2.0,
            "production_speed_mult":   0.75
        },
        "weaknesses": [
            "Low individual unit quality",
            "Buildings are organic — vulnerable to fire damage",
            "No energy shields — pure HP only"
        ],
        "starting_conditions": {
            "energy":   80,
            "minerals": 60,
            "units":    ["wraith_drone_unit"],
            "buildings":["hive_core"]
        },
        "lore_quote": "We are your death. — Wraith Queen",

        "buildings": [
            {
                "id": "hive_core",
                "name": "Hive Core",
                "description": "Living central organism of the Wraith hive. Pulses with dark life.",
                "hp": 750,
                "cost_energy": 0, "cost_minerals": 0, "build_time": 0,
                "provides": ["base", "stargate_node"], "unique": False
            },
            {
                "id": "feeding_pit",
                "name": "Feeding Pit",
                "description": "Captures life energy from the planet itself. Generates resources.",
                "hp": 250,
                "cost_energy": 0, "cost_minerals": 40, "build_time": 6.0,
                "provides": ["energy"], "energy_per_second": 5.5, "unique": False
            },
            {
                "id": "spawning_pool",
                "name": "Spawning Pool",
                "description": "Organic vat that rapidly grows Wraith warriors from biomass.",
                "hp": 380,
                "cost_energy": 50, "cost_minerals": 35, "build_time": 7.0,
                "provides": ["unit_production"],
                "produces": ["wraith_drone_unit", "wraith_soldier", "wraith_tracker"],
                "unique": False
            },
            {
                "id": "wraith_stargate",
                "name": "Space Gate (Pegasus)",
                "description": "Pegasus-variant Stargate integrated into hive organic tissue.",
                "hp": 900,
                "cost_energy": 0, "cost_minerals": 0, "build_time": 0,
                "provides": ["stargate"], "unique": True
            },
            {
                "id": "cloning_facility",
                "name": "Cloning Facility",
                "description": "Mass-produces Wraith warriors at alarming speed. Quantity over quality.",
                "hp": 350,
                "cost_energy": 80, "cost_minerals": 60, "build_time": 12.0,
                "provides": ["mass_production"],
                "production_speed_bonus": 0.30,
                "unique": True
            },
            {
                "id": "dart_bay",
                "name": "Dart Bay",
                "description": "Launch cavern for Wraith Dart fighters.",
                "hp": 350,
                "cost_energy": 100, "cost_minerals": 70, "build_time": 12.0,
                "provides": ["air_production"],
                "produces": ["wraith_dart", "hive_ship"],
                "unique": False
            }
        ],

        "units": [
            {
                "id": "wraith_drone_unit",
                "name": "Wraith Drone",
                "role": "light_infantry",
                "description": "Mindless bio-soldier. Weak individually, terrifying in swarms.",
                "hp": 70,
                "damage": 10, "attack_speed": 0.7, "range": 40, "speed": 180,
                "cost_energy": 12, "production_time": 2.0,
                "abilities": ["life_drain"]
            },
            {
                "id": "wraith_soldier",
                "name": "Wraith Soldier",
                "role": "heavy_infantry",
                "description": "Sentient warrior with stunner rifle and feeding hand.",
                "hp": 150,
                "damage": 18, "attack_speed": 1.0, "range": 70, "speed": 145,
                "cost_energy": 35, "production_time": 4.5,
                "abilities": ["life_drain", "stun"]
            },
            {
                "id": "wraith_tracker",
                "name": "Wraith Tracker",
                "role": "ranged",
                "description": "Long-range hunter with bio-organic sniper growths.",
                "hp": 65,
                "damage": 35, "attack_speed": 2.0, "range": 160, "speed": 155,
                "cost_energy": 45, "production_time": 6.0,
                "abilities": ["mark_prey"]
            },
            {
                "id": "wraith_dart",
                "name": "Wraith Dart",
                "role": "air",
                "description": "Fast organic fighter. Can cull (capture) enemy infantry.",
                "hp": 80,
                "damage": 16, "attack_speed": 0.6, "range": 90, "speed": 320,
                "cost_energy": 55, "production_time": 6.0,
                "abilities": ["culling_beam"]
            },
            {
                "id": "wraith_queen",
                "name": "Wraith Queen",
                "role": "elite",
                "description": "Telepathic hive leader. Buffs all nearby Wraith and drains enemies.",
                "hp": 250,
                "damage": 30, "attack_speed": 1.5, "range": 60, "speed": 110,
                "cost_energy": 100, "production_time": 16.0,
                "abilities": ["life_drain", "telepathic_command", "psychic_scream"]
            },
            {
                "id": "hive_ship",
                "name": "Hive Ship",
                "role": "super",
                "description": "Colossal living warship. Self-healing, spawns darts in combat.",
                "hp": 1200,
                "damage": 55, "attack_speed": 2.0, "range": 170, "speed": 50,
                "cost_energy": 280, "production_time": 45.0,
                "abilities": ["regenerate", "spawn_darts", "life_drain"],
                "requires_tech": "tier5_hive_awakening"
            }
        ]
    }


def def_ancients():
    """Ancients (Lanteans) — ultimate technology, extremely expensive, ascension mechanics."""
    return {
        "id": "ancients",
        "name": "Ancients",
        "full_name": "Ancients — Lantean Legacy",
        "description": (
            "The original gate-builders and most advanced civilization "
            "ever to exist. The Ancients left behind technology of "
            "unimaginable power. Playing as their remnant means wielding "
            "god-like devices — at god-like costs."
        ),
        "color_palette": {
            "primary":   "#F0E68C",
            "secondary": "#B8A94E",
            "accent":    "#FFFFF0",
            "ui_bg":     "#1A1A0E"
        },
        "traits": [
            "Gate Builders — Stargates cost nothing and activate instantly",
            "Ascension — tier 5 unlocks transcendent abilities",
            "Zero Point Energy — power plants produce 2x energy"
        ],
        "bonuses": {
            "stargate_cost":       0,
            "energy_gen_mult":     2.0,
            "ascension_unlocked":  True
        },
        "weaknesses": [
            "All units and buildings cost 40% more",
            "Extremely slow production times",
            "Very few units — losing one is devastating"
        ],
        "starting_conditions": {
            "energy":   250,
            "minerals": 30,
            "units":    ["ancient_sentinel"],
            "buildings":["atlantis_outpost"]
        },
        "lore_quote": "The universe is vast, and we are so very small. — Merlin",

        "buildings": [
            {
                "id": "atlantis_outpost",
                "name": "Atlantis Outpost",
                "description": "A city-ship fragment. Immensely durable command center with built-in defenses.",
                "hp": 1500,
                "cost_energy": 0, "cost_minerals": 0, "build_time": 0,
                "provides": ["base", "stargate_node", "defense_turret"],
                "unique": False
            },
            {
                "id": "zpm_hub",
                "name": "Zero Point Module Hub",
                "description": "Extracts vacuum energy from subspace. Extraordinary power output.",
                "hp": 400,
                "cost_energy": 0, "cost_minerals": 120, "build_time": 14.0,
                "provides": ["energy"], "energy_per_second": 12.0, "unique": False
            },
            {
                "id": "construction_array",
                "name": "Nanite Construction Array",
                "description": "Molecular-level fabricator. Builds anything but very slowly.",
                "hp": 500,
                "cost_energy": 160, "cost_minerals": 100, "build_time": 18.0,
                "provides": ["unit_production"],
                "produces": ["ancient_sentinel", "ancient_knight", "ancient_seer"],
                "unique": False
            },
            {
                "id": "ancient_stargate",
                "name": "Ancestral Stargate",
                "description": "The original design. Can dial any address, including other galaxies.",
                "hp": 2000,
                "cost_energy": 0, "cost_minerals": 0, "build_time": 0,
                "provides": ["stargate", "intergalactic_dial"], "unique": True
            },
            {
                "id": "ascension_chamber",
                "name": "Ascension Chamber",
                "description": "Allows units to transcend physical form. Grants immense power at great cost.",
                "hp": 600,
                "cost_energy": 300, "cost_minerals": 250, "build_time": 30.0,
                "provides": ["ascension"],
                "unique": True
            },
            {
                "id": "aurora_drydock",
                "name": "Aurora-class Drydock",
                "description": "Construction facility for Ancient warships of legendary power.",
                "hp": 700,
                "cost_energy": 350, "cost_minerals": 300, "build_time": 35.0,
                "provides": ["air_production"],
                "produces": ["puddle_jumper", "aurora_warship"],
                "unique": False
            }
        ],

        "units": [
            {
                "id": "ancient_sentinel",
                "name": "Ancient Sentinel",
                "role": "light_infantry",
                "description": "Autonomous defense drone with directed energy weapon.",
                "hp": 100, "shield": 80,
                "damage": 22, "attack_speed": 1.0, "range": 110, "speed": 150,
                "cost_energy": 60, "production_time": 7.0,
                "abilities": ["energy_shield"]
            },
            {
                "id": "ancient_knight",
                "name": "Ancient Knight",
                "role": "heavy_infantry",
                "description": "Power-armored warrior wielding a molecular disruption lance.",
                "hp": 220, "shield": 150,
                "damage": 35, "attack_speed": 1.4, "range": 80, "speed": 110,
                "cost_energy": 100, "production_time": 12.0,
                "abilities": ["energy_shield", "disruption_field"]
            },
            {
                "id": "ancient_seer",
                "name": "Ancient Seer",
                "role": "ranged",
                "description": "Psionically gifted Ancient. Attacks with focused mental energy at extreme range.",
                "hp": 80, "shield": 100,
                "damage": 55, "attack_speed": 2.5, "range": 220, "speed": 120,
                "cost_energy": 110, "production_time": 14.0,
                "abilities": ["energy_shield", "foresight", "mind_blast"]
            },
            {
                "id": "puddle_jumper",
                "name": "Puddle Jumper",
                "role": "air",
                "description": "Small cloakable craft that fits through the Stargate. Drone weapons.",
                "hp": 110, "shield": 90,
                "damage": 28, "attack_speed": 0.9, "range": 130, "speed": 290,
                "cost_energy": 120, "production_time": 14.0,
                "abilities": ["cloak", "drone_volley", "gate_travel"]
            },
            {
                "id": "ascended_being",
                "name": "Ascended Being",
                "role": "elite",
                "description": "A being of pure energy. Nearly invincible but bound by non-interference rules.",
                "hp": 50, "shield": 500,
                "damage": 80, "attack_speed": 2.0, "range": 150, "speed": 200,
                "cost_energy": 250, "production_time": 30.0,
                "abilities": ["energy_shield", "phase_shift", "reality_warp"]
            },
            {
                "id": "aurora_warship",
                "name": "Aurora-class Warship",
                "role": "super",
                "description": "Legendary Ancient battleship. Drone weapons, impenetrable shields, hyperdrive.",
                "hp": 800, "shield": 800,
                "damage": 100, "attack_speed": 1.8, "range": 220, "speed": 75,
                "cost_energy": 500, "production_time": 65.0,
                "abilities": ["drone_swarm", "energy_shield", "hyperdrive"],
                "requires_tech": "tier5_legacy_of_the_ancients"
            }
        ]
    }


# ============================================================
#  TECHNOLOGY TREE DEFINITIONS
# ============================================================

def tech_tauri():
    """Tau'ri tech tree — reverse-engineering focus, tiers I-V."""
    return {
        "faction": "tauri",
        "tree_name": "SGC Research Program",
        "tiers": {
            "tier1": {
                "name": "Basic Operations",
                "nodes": [
                    {"id": "t1_field_training",   "name": "Field Training",           "cost": 50,   "time": 15, "prereqs": [],                     "unlocks": ["marine"],          "description": "Basic combat training protocols."},
                    {"id": "t1_naquadah_study",    "name": "Naquadah Analysis",        "cost": 60,   "time": 20, "prereqs": [],                     "unlocks": ["naquadah_reactor"],"description": "Study Naquadah crystal structures for energy use."},
                    {"id": "t1_recon_protocols",   "name": "Recon Protocols",          "cost": 40,   "time": 12, "prereqs": [],                     "unlocks": ["stealth_recon"],   "description": "Advanced reconnaissance tactics for SG teams."}
                ]
            },
            "tier2": {
                "name": "Alien Tech Integration",
                "nodes": [
                    {"id": "t2_reverse_eng",       "name": "Reverse Engineering",      "cost": 100,  "time": 30, "prereqs": ["t1_naquadah_study"],  "unlocks": ["area51_lab"],      "description": "Systematically decode alien technology."},
                    {"id": "t2_advanced_weapons",   "name": "Advanced Ballistics",      "cost": 80,   "time": 25, "prereqs": ["t1_field_training"],  "unlocks": ["sniper", "+10% damage"],     "description": "Improved projectile weapons using alien alloys."},
                    {"id": "t2_field_medic",        "name": "Field Medic Program",      "cost": 70,   "time": 20, "prereqs": ["t1_field_training"],  "unlocks": ["+2 hp_regen"],     "description": "Combat medic deployment in all squads."}
                ]
            },
            "tier3": {
                "name": "Hybrid Technology",
                "nodes": [
                    {"id": "t3_f302_program",      "name": "F-302 Program",            "cost": 150,  "time": 40, "prereqs": ["t2_reverse_eng"],     "unlocks": ["f302", "f302_hangar"],      "description": "Develop Earth's first hybrid-tech fighter."},
                    {"id": "t3_trinium_armor",     "name": "Trinium Armor Plating",    "cost": 120,  "time": 35, "prereqs": ["t2_reverse_eng"],     "unlocks": ["+20% unit HP"],    "description": "Reinforce all units with Trinium alloy."},
                    {"id": "t3_emp_tech",          "name": "EMP Weaponry",             "cost": 130,  "time": 35, "prereqs": ["t2_advanced_weapons"],"unlocks": ["hazmat_trooper", "emp_grenade"],  "description": "Electromagnetic pulse weapons against shielded foes."}
                ]
            },
            "tier4": {
                "name": "Interstellar Command",
                "nodes": [
                    {"id": "t4_bc303_project",     "name": "BC-303 Project",           "cost": 250,  "time": 60, "prereqs": ["t3_f302_program"],    "unlocks": ["prometheus"],      "description": "Earth's first interstellar battlecruiser."},
                    {"id": "t4_zpm_research",      "name": "ZPM Research",             "cost": 200,  "time": 50, "prereqs": ["t3_trinium_armor"],   "unlocks": ["+50% energy_gen"], "description": "Partial understanding of Zero Point Energy."},
                    {"id": "t4_asgard_alliance",   "name": "Asgard Alliance",          "cost": 180,  "time": 45, "prereqs": ["t3_f302_program"],    "unlocks": ["+beam_transport"],"description": "Formalize treaty with the Asgard for tech sharing."}
                ]
            },
            "tier5": {
                "name": "Earth's Legacy",
                "nodes": [
                    {"id": "tier5_earth_fleet",    "name": "Earth Defense Fleet",      "cost": 400,  "time": 90, "prereqs": ["t4_bc303_project", "t4_zpm_research"],  "unlocks": ["prometheus_upgrade", "+30% all stats"],  "description": "Full fleet deployment. Humanity's finest hour."}
                ]
            }
        }
    }


def tech_goauld():
    """Goa'uld tech tree — domination and stolen tech."""
    return {
        "faction": "goauld",
        "tree_name": "System Lord Decrees",
        "tiers": {
            "tier1": {
                "name": "Consolidation of Power",
                "nodes": [
                    {"id": "t1_slave_labor",       "name": "Slave Labor Optimization",  "cost": 40,  "time": 12, "prereqs": [],                      "unlocks": ["+15% mine_output"],    "description": "Increase Naquadah extraction through harsher quotas."},
                    {"id": "t1_staff_upgrade",     "name": "Staff Weapon Calibration",  "cost": 50,  "time": 15, "prereqs": [],                      "unlocks": ["+10% damage"],         "description": "Recalibrate staff weapons for improved lethality."},
                    {"id": "t1_jaffa_loyalty",     "name": "Jaffa Indoctrination",      "cost": 45,  "time": 14, "prereqs": [],                      "unlocks": ["jaffa_elite"],         "description": "Deeper religious programming for Jaffa loyalty."}
                ]
            },
            "tier2": {
                "name": "God's Arsenal",
                "nodes": [
                    {"id": "t2_sarcophagus",       "name": "Sarcophagus Mastery",       "cost": 90,  "time": 25, "prereqs": ["t1_jaffa_loyalty"],    "unlocks": ["sarcophagus_chamber"], "description": "Perfected resurrection technology."},
                    {"id": "t2_death_glider_mk2",  "name": "Death Glider Mk II",        "cost": 80,  "time": 22, "prereqs": ["t1_staff_upgrade"],    "unlocks": ["death_glider", "+15% air_speed"], "description": "Improved glider engines and weapons."},
                    {"id": "t2_ashrak_training",   "name": "Ashrak Training",           "cost": 100, "time": 28, "prereqs": ["t1_jaffa_loyalty"],    "unlocks": ["ashrak"],              "description": "Train the deadliest assassins in the galaxy."}
                ]
            },
            "tier3": {
                "name": "Anubis's Secrets",
                "nodes": [
                    {"id": "t3_kull_program",      "name": "Kull Warrior Program",      "cost": 160, "time": 40, "prereqs": ["t2_sarcophagus"],      "unlocks": ["kull_warrior"],        "description": "Create super-soldiers using Ancient knowledge."},
                    {"id": "t3_shield_tech",       "name": "Personal Shield Emitters",  "cost": 140, "time": 35, "prereqs": ["t2_death_glider_mk2"], "unlocks": ["+shield 40 elite"],    "description": "Equip elite units with personal energy shields."},
                    {"id": "t3_naquadria",         "name": "Naquadria Weapons",         "cost": 150, "time": 38, "prereqs": ["t1_slave_labor"],       "unlocks": ["+25% structure_damage"],"description": "Unstable but devastating explosive material."}
                ]
            },
            "tier4": {
                "name": "System Lord Ascendancy",
                "nodes": [
                    {"id": "t4_hatak_refit",       "name": "Ha'tak Refit",              "cost": 220, "time": 55, "prereqs": ["t3_shield_tech"],       "unlocks": ["hatak_shipyard"],      "description": "Upgrade shipyard for modern Ha'tak construction."},
                    {"id": "t4_mass_cloning",      "name": "Mass Jaffa Cloning",        "cost": 200, "time": 50, "prereqs": ["t3_kull_program"],      "unlocks": ["+30% production_speed"],"description": "Clone Jaffa warriors at industrial scale."},
                    {"id": "t4_eye_of_ra",         "name": "Eye of Ra",                 "cost": 250, "time": 60, "prereqs": ["t3_naquadria"],          "unlocks": ["+superweapon_charge"], "description": "Ancient weapon of devastating orbital power."}
                ]
            },
            "tier5": {
                "name": "Divine Dominion",
                "nodes": [
                    {"id": "tier5_fleet_dominion",  "name": "Fleet of the Gods",        "cost": 400, "time": 85, "prereqs": ["t4_hatak_refit", "t4_eye_of_ra"],  "unlocks": ["hatak", "+40% all stats"], "description": "Unleash the full armada of the System Lords."}
                ]
            }
        }
    }


def tech_jaffa():
    """Free Jaffa tech tree — honor, freedom, adapted alien tech."""
    return {
        "faction": "jaffa",
        "tree_name": "Path of Freedom",
        "tiers": {
            "tier1": {
                "name": "Breaking Chains",
                "nodes": [
                    {"id": "t1_tretonin_synth",    "name": "Tretonin Synthesis",       "cost": 50,  "time": 15, "prereqs": [],                      "unlocks": ["tretonin_lab", "+hp_regen"],  "description": "Free Jaffa from symbiote dependency."},
                    {"id": "t1_warrior_rites",     "name": "Warrior Rites",            "cost": 45,  "time": 14, "prereqs": [],                      "unlocks": ["+10% melee_damage"],          "description": "Ancient combat ceremonies that harden resolve."},
                    {"id": "t1_salvage_ops",       "name": "Salvage Operations",       "cost": 40,  "time": 12, "prereqs": [],                      "unlocks": ["+15% mineral_gather"],        "description": "Efficient scavenging of Goa'uld tech debris."}
                ]
            },
            "tier2": {
                "name": "Forging Identity",
                "nodes": [
                    {"id": "t2_veteran_training",  "name": "Veteran Training Grounds",  "cost": 80,  "time": 22, "prereqs": ["t1_warrior_rites"],    "unlocks": ["jaffa_veteran"],          "description": "Advanced combat training for experienced warriors."},
                    {"id": "t2_mastaba_order",     "name": "Mastaba Guard Order",       "cost": 90,  "time": 25, "prereqs": ["t1_warrior_rites"],    "unlocks": ["mastaba_guard"],          "description": "Establish the elite temple guard corps."},
                    {"id": "t2_staff_reforge",     "name": "Staff Weapon Reforging",    "cost": 70,  "time": 20, "prereqs": ["t1_salvage_ops"],      "unlocks": ["+15% range"],             "description": "Reforge captured staff weapons with improved focus crystals."}
                ]
            },
            "tier3": {
                "name": "Sodan Legacy",
                "nodes": [
                    {"id": "t3_sodan_secrets",     "name": "Sodan Ancient Secrets",     "cost": 130, "time": 35, "prereqs": ["t2_veteran_training"], "unlocks": ["sodan_warrior"],           "description": "Learn the cloaking arts of the Sodan."},
                    {"id": "t3_ritual_site",       "name": "M'al Sharran Ritual",       "cost": 120, "time": 32, "prereqs": ["t2_mastaba_order"],    "unlocks": ["rite_of_malshuraan"],      "description": "Sacred rite that permanently empowers warriors."},
                    {"id": "t3_alkesh_capture",    "name": "Al'kesh Capture Program",   "cost": 140, "time": 38, "prereqs": ["t2_staff_reforge"],    "unlocks": ["alkesh", "alkesh_pad"],    "description": "Board and seize Goa'uld bombers for the Free Jaffa."}
                ]
            },
            "tier4": {
                "name": "Nation Rising",
                "nodes": [
                    {"id": "t4_unified_council",   "name": "Jaffa High Council",        "cost": 200, "time": 50, "prereqs": ["t3_sodan_secrets"],    "unlocks": ["+20% all_unit_stats"],    "description": "Unite the Jaffa under a single ruling council."},
                    {"id": "t4_fleet_seizure",     "name": "Fleet Seizure Tactics",     "cost": 220, "time": 55, "prereqs": ["t3_alkesh_capture"],   "unlocks": ["+captured_hatak_access"], "description": "Coordinated operations to steal Ha'tak vessels."},
                    {"id": "t4_tretonin_mk2",     "name": "Tretonin MK II",            "cost": 180, "time": 45, "prereqs": ["t3_ritual_site"],      "unlocks": ["+3 hp_regen_per_sec"],    "description": "Enhanced serum providing superhuman regeneration."}
                ]
            },
            "tier5": {
                "name": "Liberation",
                "nodes": [
                    {"id": "tier5_liberation_fleet","name": "Liberation Armada",        "cost": 380, "time": 80, "prereqs": ["t4_fleet_seizure", "t4_unified_council"],  "unlocks": ["hatak_captured", "+35% all stats"], "description": "The Free Jaffa armada rises. Freedom for all."}
                ]
            }
        }
    }


def tech_asgard():
    """Asgard tech tree — pure science, shields, beaming."""
    return {
        "faction": "asgard",
        "tree_name": "Asgard Scientific Mandate",
        "tiers": {
            "tier1": {
                "name": "Core Systems Online",
                "nodes": [
                    {"id": "t1_shield_harmonics",  "name": "Shield Harmonics",          "cost": 60,  "time": 15, "prereqs": [],                      "unlocks": ["+20 shield_hp_all"],    "description": "Optimize energy shield frequency for all units."},
                    {"id": "t1_beam_calibration",  "name": "Beam Calibration",          "cost": 55,  "time": 14, "prereqs": [],                      "unlocks": ["+10% damage"],          "description": "Fine-tune directed energy weapon output."},
                    {"id": "t1_drone_production",  "name": "Automated Drone Lines",     "cost": 50,  "time": 12, "prereqs": [],                      "unlocks": ["+15% production_speed"],"description": "Optimize drone replication assembly lines."}
                ]
            },
            "tier2": {
                "name": "Advanced Systems",
                "nodes": [
                    {"id": "t2_guardian_program",   "name": "Guardian Program",          "cost": 100, "time": 28, "prereqs": ["t1_shield_harmonics"], "unlocks": ["asgard_guardian"],       "description": "Deploy heavy combat platforms."},
                    {"id": "t2_vanir_integration",  "name": "Vanir Integration",         "cost": 110, "time": 30, "prereqs": ["t1_beam_calibration"], "unlocks": ["vanir_soldier"],         "description": "Adapt Vanir battlesuit technology."},
                    {"id": "t2_neutrino_boost",     "name": "Neutrino Flux Amplifier",   "cost": 90,  "time": 25, "prereqs": ["t1_drone_production"], "unlocks": ["+30% energy_gen"],       "description": "Dramatically increase generator output."}
                ]
            },
            "tier3": {
                "name": "Pinnacle Engineering",
                "nodes": [
                    {"id": "t3_time_dilation",     "name": "Time Dilation Field",       "cost": 180, "time": 42, "prereqs": ["t2_guardian_program"],  "unlocks": ["time_dilation_field"],   "description": "Deploy localized temporal distortion."},
                    {"id": "t3_thor_avatar",       "name": "Thor Avatar Project",       "cost": 200, "time": 45, "prereqs": ["t2_vanir_integration"],"unlocks": ["thor_avatar"],           "description": "Create a combat-capable holographic avatar of Thor."},
                    {"id": "t3_replicator_defense","name": "Anti-Replicator Weapons",   "cost": 160, "time": 38, "prereqs": ["t2_neutrino_boost"],   "unlocks": ["+25% damage_vs_mech"],   "description": "Weapons specifically designed to disrupt mechanical threats."}
                ]
            },
            "tier4": {
                "name": "Fleet Mobilization",
                "nodes": [
                    {"id": "t4_beliskner_refit",   "name": "Beliskner Refit",           "cost": 280, "time": 60, "prereqs": ["t3_thor_avatar"],      "unlocks": ["beliskner_dock"],        "description": "Modernize the legendary warship class."},
                    {"id": "t4_mass_beaming",      "name": "Mass Beaming Array",        "cost": 220, "time": 50, "prereqs": ["t3_time_dilation"],    "unlocks": ["+beam_all_units"],       "description": "Teleport entire armies instantly."},
                    {"id": "t4_genetic_repair",    "name": "Genetic Repair Therapy",    "cost": 250, "time": 55, "prereqs": ["t3_replicator_defense"],"unlocks": ["+40% unit HP"],          "description": "Partially reverse Asgard genetic degradation."}
                ]
            },
            "tier5": {
                "name": "Asgard Legacy",
                "nodes": [
                    {"id": "tier5_asgard_ascendancy","name": "Asgard Ascendancy",       "cost": 450, "time": 100,"prereqs": ["t4_beliskner_refit", "t4_genetic_repair"],  "unlocks": ["beliskner", "+50% all stats"], "description": "The Asgard reach their ultimate potential."}
                ]
            }
        }
    }


def tech_wraith():
    """Wraith tech tree — bio-organic evolution, swarm, feeding."""
    return {
        "faction": "wraith",
        "tree_name": "Hive Evolution Protocols",
        "tiers": {
            "tier1": {
                "name": "Primal Instincts",
                "nodes": [
                    {"id": "t1_feeding_frenzy",    "name": "Feeding Frenzy",            "cost": 35,  "time": 10, "prereqs": [],                       "unlocks": ["+15% life_drain"],       "description": "Enhanced feeding enzymes for greater HP drain."},
                    {"id": "t1_hive_growth",       "name": "Accelerated Hive Growth",   "cost": 40,  "time": 12, "prereqs": [],                       "unlocks": ["+20% structure_regen"],  "description": "Stimulate organic building regeneration."},
                    {"id": "t1_swarm_instinct",    "name": "Swarm Instinct",            "cost": 30,  "time": 8,  "prereqs": [],                       "unlocks": ["+20% production_speed"], "description": "Faster drone spawning through pheromone cascades."}
                ]
            },
            "tier2": {
                "name": "Hive Adaptation",
                "nodes": [
                    {"id": "t2_wraith_soldier_ev", "name": "Soldier Evolution",          "cost": 70,  "time": 20, "prereqs": ["t1_feeding_frenzy"],   "unlocks": ["wraith_soldier", "+HP"], "description": "Breed stronger sentient warriors."},
                    {"id": "t2_tracker_breed",     "name": "Tracker Breed",              "cost": 75,  "time": 22, "prereqs": ["t1_swarm_instinct"],   "unlocks": ["wraith_tracker"],        "description": "Develop long-range hunter subspecies."},
                    {"id": "t2_dart_swarm",        "name": "Dart Swarm Tactics",         "cost": 65,  "time": 18, "prereqs": ["t1_hive_growth"],      "unlocks": ["wraith_dart", "dart_bay"],"description": "Mass-produce organic fighter craft."}
                ]
            },
            "tier3": {
                "name": "Queen's Will",
                "nodes": [
                    {"id": "t3_queen_evolution",   "name": "Queen Evolution",            "cost": 130, "time": 35, "prereqs": ["t2_wraith_soldier_ev"],"unlocks": ["wraith_queen"],          "description": "Evolve a more powerful Wraith Queen."},
                    {"id": "t3_cloning_mastery",   "name": "Cloning Mastery",            "cost": 110, "time": 30, "prereqs": ["t2_tracker_breed"],    "unlocks": ["cloning_facility"],      "description": "Mass cloning vats for overwhelming numbers."},
                    {"id": "t3_organic_armor",     "name": "Organic Carapace Armor",     "cost": 120, "time": 32, "prereqs": ["t2_dart_swarm"],       "unlocks": ["+25% unit HP"],          "description": "Thicker bio-armor growth for all Wraith units."}
                ]
            },
            "tier4": {
                "name": "Hive Fleet",
                "nodes": [
                    {"id": "t4_hive_ship_growth",  "name": "Hive Ship Gestation",        "cost": 200, "time": 50, "prereqs": ["t3_queen_evolution"],  "unlocks": ["+hive_ship_access"],     "description": "Begin growing a colossal living warship."},
                    {"id": "t4_psychic_web",       "name": "Psychic Hive Web",           "cost": 180, "time": 45, "prereqs": ["t3_cloning_mastery"],  "unlocks": ["+telepathic_buff_all"],  "description": "Queen's mind links all units for coordinated strikes."},
                    {"id": "t4_retrovirus",        "name": "Wraith Retrovirus",          "cost": 190, "time": 48, "prereqs": ["t3_organic_armor"],    "unlocks": ["+convert_enemy_units"],  "description": "Virus that turns enemies into Wraith servants."}
                ]
            },
            "tier5": {
                "name": "The Great Awakening",
                "nodes": [
                    {"id": "tier5_hive_awakening", "name": "Hive Awakening",            "cost": 350, "time": 75, "prereqs": ["t4_hive_ship_growth", "t4_psychic_web"],  "unlocks": ["hive_ship", "+40% all stats"], "description": "All hives awaken. The galaxy trembles."}
                ]
            }
        }
    }


def tech_ancients():
    """Ancients tech tree — ultimate power through knowledge and ascension."""
    return {
        "faction": "ancients",
        "tree_name": "Path of Enlightenment",
        "tiers": {
            "tier1": {
                "name": "Reawakening",
                "nodes": [
                    {"id": "t1_zpm_efficiency",    "name": "ZPM Efficiency",            "cost": 70,  "time": 18, "prereqs": [],                       "unlocks": ["+25% energy_gen"],       "description": "Optimize Zero Point Module energy extraction."},
                    {"id": "t1_drone_weapons",     "name": "Drone Weapon Reactivation", "cost": 65,  "time": 16, "prereqs": [],                       "unlocks": ["+15% damage"],           "description": "Reactivate Ancient drone weapon stockpiles."},
                    {"id": "t1_nanite_repair",     "name": "Nanite Repair Swarms",      "cost": 60,  "time": 15, "prereqs": [],                       "unlocks": ["+3 hp_regen_per_sec"],   "description": "Deploy microscopic repair machines."}
                ]
            },
            "tier2": {
                "name": "Lost Knowledge",
                "nodes": [
                    {"id": "t2_knight_protocol",   "name": "Knight Protocol",            "cost": 120, "time": 30, "prereqs": ["t1_drone_weapons"],    "unlocks": ["ancient_knight"],        "description": "Activate Ancient warrior power armor."},
                    {"id": "t2_seer_awakening",    "name": "Seer Awakening",             "cost": 130, "time": 32, "prereqs": ["t1_nanite_repair"],    "unlocks": ["ancient_seer"],          "description": "Awaken latent psionic abilities."},
                    {"id": "t2_puddle_jumper_bay", "name": "Jumper Bay Restoration",     "cost": 140, "time": 34, "prereqs": ["t1_zpm_efficiency"],   "unlocks": ["puddle_jumper", "aurora_drydock"],"description": "Restore the Puddle Jumper manufacturing bay."}
                ]
            },
            "tier3": {
                "name": "Higher Understanding",
                "nodes": [
                    {"id": "t3_ascension_research","name": "Ascension Research",         "cost": 200, "time": 45, "prereqs": ["t2_seer_awakening"],   "unlocks": ["ascension_chamber"],     "description": "Study the process of ascending to a higher plane."},
                    {"id": "t3_city_shield",       "name": "City Shield Activation",     "cost": 180, "time": 40, "prereqs": ["t2_knight_protocol"],  "unlocks": ["+shield_all_structures"],"description": "Activate Atlantis-type shield over the base."},
                    {"id": "t3_intergalactic",     "name": "Intergalactic Dial Program", "cost": 190, "time": 42, "prereqs": ["t2_puddle_jumper_bay"],"unlocks": ["+intergalactic_gate"],   "description": "Dial Stargates in other galaxies."}
                ]
            },
            "tier4": {
                "name": "Transcendence",
                "nodes": [
                    {"id": "t4_ascended_being",    "name": "First Ascension",            "cost": 300, "time": 65, "prereqs": ["t3_ascension_research"],"unlocks": ["ascended_being"],       "description": "The first being ascends to pure energy."},
                    {"id": "t4_aurora_project",    "name": "Aurora Project",              "cost": 320, "time": 70, "prereqs": ["t3_city_shield"],      "unlocks": ["+aurora_warship_access"],"description": "Begin construction of an Aurora-class warship."},
                    {"id": "t4_repository",        "name": "Repository of Knowledge",    "cost": 280, "time": 60, "prereqs": ["t3_intergalactic"],    "unlocks": ["+50% research_speed"],   "description": "Access the full Repository of Ancient knowledge."}
                ]
            },
            "tier5": {
                "name": "Legacy Fulfilled",
                "nodes": [
                    {"id": "tier5_legacy_of_the_ancients","name": "Legacy of the Ancients","cost": 500,"time": 110,"prereqs": ["t4_aurora_project", "t4_ascended_being"],  "unlocks": ["aurora_warship", "+60% all stats"], "description": "The full might of the Ancients is restored. Galaxies bow."}
                ]
            }
        }
    }


# ============================================================
#  GENERATORS MAP
# ============================================================

FACTION_GENERATORS = {
    "tauri":    def_tauri,
    "goauld":   def_goauld,
    "jaffa":    def_jaffa,
    "asgard":   def_asgard,
    "wraith":   def_wraith,
    "ancients": def_ancients,
}

TECH_GENERATORS = {
    "tauri":    tech_tauri,
    "goauld":   tech_goauld,
    "jaffa":    tech_jaffa,
    "asgard":   tech_asgard,
    "wraith":   tech_wraith,
    "ancients": tech_ancients,
}


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
        print("Usage: python generate_factions_and_tech.py <project_dir>")
        sys.exit(1)

    project_dir = os.path.abspath(sys.argv[1])
    print(f"  Project directory: {project_dir}")
    print(f"  Game: {GAME_NAME}")
    print()

    generated = []

    # === Faction data ===
    print("  Generating faction definitions...")
    for fid in FACTION_IDS:
        gen_func = FACTION_GENERATORS.get(fid)
        if not gen_func:
            print(f"  WARNING: No generator for faction '{fid}'")
            continue
        data = gen_func()
        rel_path = f"data/factions/{fid}.json"
        write_json(project_dir, rel_path, data)
        generated.append(rel_path)
        n_buildings = len(data.get("buildings", []))
        n_units = len(data.get("units", []))
        print(f"  [OK] {rel_path}  ({n_buildings} buildings, {n_units} units)")

    print()

    # === Tech trees ===
    print("  Generating technology trees...")
    for fid in FACTION_IDS:
        gen_func = TECH_GENERATORS.get(fid)
        if not gen_func:
            print(f"  WARNING: No tech generator for faction '{fid}'")
            continue
        data = gen_func()
        rel_path = f"data/tech/{fid}_tech.json"
        write_json(project_dir, rel_path, data)
        generated.append(rel_path)
        total_nodes = sum(len(tier["nodes"]) for tier in data["tiers"].values())
        print(f"  [OK] {rel_path}  ({total_nodes} tech nodes across 5 tiers)")

    # === Summary stats ===
    total_factions = len(FACTION_IDS)
    total_buildings = 0
    total_units = 0
    total_tech_nodes = 0
    for fid in FACTION_IDS:
        fd = FACTION_GENERATORS[fid]()
        total_buildings += len(fd.get("buildings", []))
        total_units += len(fd.get("units", []))
        td = TECH_GENERATORS[fid]()
        total_tech_nodes += sum(len(t["nodes"]) for t in td["tiers"].values())

    print()
    print("  ========================================")
    print(f"  FACTION & TECH GENERATION COMPLETE")
    print(f"  Factions:      {total_factions}")
    print(f"  Buildings:     {total_buildings} total")
    print(f"  Units:         {total_units} total")
    print(f"  Tech nodes:    {total_tech_nodes} total")
    print(f"  Files:         {len(generated)}")
    print("  ========================================")
    print()
    print("  Generated files:")
    for f in generated:
        print(f"    - {f}")
    print()

    # Faction roster summary
    print("  Faction Roster:")
    for fid in FACTION_IDS:
        fd = FACTION_GENERATORS[fid]()
        units_str = ", ".join(u["name"] for u in fd["units"])
        print(f"    {fd['name']:15s} | {len(fd['units'])} units: {units_str}")
    print()
    print("  All faction and tech data ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
