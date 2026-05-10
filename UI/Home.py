import tkinter as tk
from config import *

class HomeView(tk.Frame):
    def __init__(self, parent, languages, on_select):
        super().__init__(parent, bg=BG)
        
        # Title Section
        tk.Label(self, text="Select Subject", font=("Segoe UI", 26, "bold"),
                 bg=BG, fg=TEXT).pack(pady=(50, 20))

        tk.Label(self, text="Choose a Subject to explore topics", font=("Segoe UI", 11),
                 bg=BG, fg=PLACEHOLDER).pack(pady=(0, 20))

        # Scrollable container
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True, padx=40, pady=10)

        canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=100)
        scrollbar.pack(side="right", fill="y")

        # Two-column subject buttons
        for i, lang in enumerate(languages):
            row, col = divmod(i, 2)
            btn = tk.Button(
                scroll_frame,
                text=lang.upper(),
                font=("Segoe UI", 12, "bold"),
                bg=ACTIVE,
                fg="white",
                width=20,
                height=2,
                relief="flat",
                cursor="hand2",
                activebackground=HOVER,
                command=lambda l=lang: on_select(l)
            )
            btn.grid(row=row, column=col, padx=20, pady=12, sticky="nsew")

        scroll_frame.grid_columnconfigure(0, weight=1)
        scroll_frame.grid_columnconfigure(1, weight=1)