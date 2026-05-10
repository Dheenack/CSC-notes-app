import tkinter as tk
from config import *

class TopicView(tk.Frame):
    def __init__(self, parent, file_handler):
        super().__init__(parent, bg=BG)
        self.f = file_handler
        self.active_lang = None
        self.all_files = []

        self.header = tk.Label(self, text="", bg=BG, fg=TEXT, font=("Segoe UI", 18, "bold"))
        self.header.pack(pady=(15, 5))

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self, textvariable=self.search_var, font=("Segoe UI", 11), relief="flat")
        self.search_entry.pack(pady=10, padx=20, fill="x")
        self.search_entry.bind("<KeyRelease>", self.filter_files)

        # Scrollable Area
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, command=self.canvas.yview)
        self.content = tk.Frame(self.canvas, bg=BG)
        
        self.content.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_lang(self, lang):
        self.active_lang = lang
        self.header.config(text=f"{lang.upper()} Topics")
        self.all_files = self.f.list_topics(lang)
        self.render_list(self.all_files)

    def filter_files(self, event=None):
        query = self.search_var.get().lower()
        filtered = [f for f in self.all_files if query in f.lower()]
        self.render_list(filtered)

    def render_list(self, files):
        for w in self.content.winfo_children(): w.destroy()
        for file in files:
            path = self.f.file_path(self.active_lang, file)
            lbl = tk.Label(self.content, text=file, bg=CARD, fg=TEXT, font=("Segoe UI", 11),
                           anchor="w", padx=12, pady=10, cursor="hand2")
            lbl.pack(fill="x", padx=20, pady=5)
            lbl.bind("<Button-1>", lambda e, p=path: self.f.open_file(p))
            lbl.bind("<Enter>", lambda e: e.widget.config(bg=ACTIVE))
            lbl.bind("<Leave>", lambda e: e.widget.config(bg=CARD))