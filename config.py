try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass
from tkinter import ttk
import os

# -------- THEME --------
BG = "#1e1e2f"
SIDEBAR = "#252538"
ACTIVE = "#4e73df"
HOVER = "#3a3a55"
TEXT = "#ffffff"
CARD = "#2f2f45"
PLACEHOLDER = "#9aa0a6"
BASE_DIR=os.path.abspath("./notes")
