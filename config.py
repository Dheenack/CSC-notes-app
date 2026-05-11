try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass
from tkinter import ttk

import json
import os
import sys
# -------- THEME --------
# BG = "#1e1e2f"
# SIDEBAR = "#252538"
# ACTIVE = "#4e73df"
# HOVER = "#3a3a55"
# TEXT = "#ffffff"
# CARD = "#2f2f45"
# PLACEHOLDER = "#9aa0a6"
# BASE_DIR=os.path.abspath("final\\notes")


def get_config_path():
    # This ensures the app finds the JSON even after being packed by PyInstaller
    if getattr(sys, 'frozen', False):
        # Path of the .exe file
        return os.path.join(os.path.dirname(sys.executable), "config.json")
    # Path of the script
    return os.path.join(os.path.dirname(__file__), "config.json")

# Default values in case the JSON is missing or corrupted
DEFAULT_CONFIG = {
    "THEME": {
        "BG": "#1e1e2f", "SIDEBAR": "#252538", "ACTIVE": "#4e73df",
        "HOVER": "#3a3a55", "TEXT": "#ffffff", "CARD": "#2f2f45", "PLACEHOLDER": "#9aa0a6"
    },
    "SETTINGS": {
        "BASE_DIR": "./notes"
    }
}

try:
    with open(get_config_path(), "r") as f:
        data = json.load(f)
except Exception:
    data = DEFAULT_CONFIG

# Export variables so your other files can still use 'from config import BG'
theme = data.get("THEME", DEFAULT_CONFIG["THEME"])
settings = data.get("SETTINGS", DEFAULT_CONFIG["SETTINGS"])

BG = theme["BG"]
SIDEBAR = theme["SIDEBAR"]
ACTIVE = theme["ACTIVE"]
HOVER = theme["HOVER"]
TEXT = theme["TEXT"]
CARD = theme["CARD"]
PLACEHOLDER = theme["PLACEHOLDER"]

BASE_DIR = os.path.abspath(settings["BASE_DIR"])