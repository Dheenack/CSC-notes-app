import tkinter as tk
from config import *

class Sidebar(tk.Frame):
    def __init__(self, parent, languages, on_select, on_home):
        super().__init__(parent, bg=SIDEBAR, width=220)
        self.on_select = on_select
        self.active_lang = None

        tk.Label(self, text="Subjects", bg=SIDEBAR, fg=TEXT, 
                 font=("Segoe UI", 14, "bold")).pack(pady=12)

        self.buttons = {}
        for lang in languages:
            btn = tk.Label(self, text=f"  {lang.upper()}", bg=SIDEBAR, fg=TEXT,
                           font=("Segoe UI", 11), anchor="w", padx=10, pady=8, cursor="hand2")
            btn.pack(fill="x")
            btn.bind("<Button-1>", lambda e, l=lang: on_select(l))
            btn.bind("<Enter>", lambda e: e.widget.config(bg=HOVER))
            btn.bind("<Leave>", lambda e: self.refresh_highlight())
            self.buttons[lang] = btn

        tk.Button(self, text="Home", bg="#ff6b6b", fg="white", relief="flat",
                  cursor="hand2", command=on_home).pack(side="bottom", pady=12, ipadx=10, ipady=5)

    def refresh_highlight(self):
        for lang, btn in self.buttons.items():
            bg_color = ACTIVE if lang == self.active_lang else SIDEBAR
            btn.config(bg=bg_color)