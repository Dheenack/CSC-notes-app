import tkinter as tk
from config import *

class TopicView(tk.Frame):
    def __init__(self, parent, file_handler):
        super().__init__(parent, bg=BG)
        self.f = file_handler
        self.active_lang = None
        self.all_files = []

        # --- Header Section ---
        self.header = tk.Label(
            self, text="", bg=BG, fg=TEXT, 
            font=("Segoe UI", 18, "bold")
        )
        self.header.pack(pady=(15, 5), fill="x")

        # --- Search Bar (Responsive Width) ---
        self.search_var = tk.StringVar()
        # Using a frame to create a border/padding effect for the flat entry
        search_frame = tk.Frame(self, bg=CARD, bd=0)
        search_frame.pack(pady=10, padx=40, fill="x") 

        self.search_entry = tk.Entry(
            search_frame, 
            textvariable=self.search_var,
            font=("Segoe UI", 11),
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT, # cursor color
            relief="flat",
            bd=8
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", self.filter_files)
        
        # Helper from your original code (ensure it's available)
        # self.add_placeholder(self.search_entry, "Search topics...")

        # --- Responsive Scroll Area ---
        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(self.container, bg=BG, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.container, command=self.canvas.yview)
        
        # This frame holds the actual topic cards
        self.content = tk.Frame(self.canvas, bg=BG)

        # 1. Update scroll region when content changes
        self.content.bind("<Configure>", self._on_frame_configure)
        
        # 2. IMPORTANT: Update content frame width when canvas resizes
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.content, anchor="nw"
        )
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Optional: Mousewheel support for Windows
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Force the inner frame to match the canvas width for true responsiveness"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def load_lang(self, lang):
        self.active_lang = lang
        self.header.config(text=f"{lang.upper()} Topics")
        self.all_files = self.f.list_topics(lang)
        self.render_files(self.all_files)

    def filter_files(self, event=None):
        query = self.search_var.get().lower()
        # If placeholder is active, don't filter
        if query == "search topics...":
            self.render_files(self.all_files)
            return
        filtered = [f for f in self.all_files if query in f.lower()]
        self.render_files(filtered)

    def render_files(self, files):
        for widget in self.content.winfo_children():
            widget.destroy()

        if not files:
            tk.Label(self.content, text="No matching topics found",
                     bg=BG, fg=PLACEHOLDER, font=("Segoe UI", 11)).pack(pady=30)
            return

        for file in files:
            path = self.f.file_path(self.active_lang, file)
            
            # Card Container
            card = tk.Frame(self.content, bg=CARD, cursor="hand2")
            card.pack(fill="x", padx=10, pady=4)
            
            lbl = tk.Label(
                card, text=file, bg=CARD, fg=TEXT,
                font=("Segoe UI", 11), anchor="w",
                padx=15, pady=12, cursor="hand2"
            )
            lbl.pack(fill="x", expand=True)

            # Bindings for hover and click (applied to both card and label)
            for w in (card, lbl):
                w.bind("<Button-1>", lambda e, p=path, f=file: self.f.open_file(p))
                w.bind("<Enter>", lambda e, c=card: self._on_hover(c))
                w.bind("<Leave>", lambda e, c=card: self._off_hover(c))

    def _on_hover(self, widget):
        widget.config(bg=ACTIVE)
        for child in widget.winfo_children():
            child.config(bg=ACTIVE)

    def _off_hover(self, widget):
        widget.config(bg=CARD)
        for child in widget.winfo_children():
            child.config(bg=CARD)