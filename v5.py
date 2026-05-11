import tkinter as tk
from FileHandler import FileHandler
from config import *
f = FileHandler(BASE_DIR)

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notes App - CSC")
        self.root.geometry("900x550")
        self.root.configure(bg=BG)

        self.active_lang = None
        self.recent_files = []

        self.show_language_home()

    # -------- UTIL --------
    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_main(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def show_language_home(self):
        self.clear_root()

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill="both", expand=True)

        tk.Label(
        frame,
        text="Select Subject",
        font=("Segoe UI", 26, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(pady=(50, 20))

        tk.Label(
        frame,
        text="Choose a Subject to explore topics",
        font=("Segoe UI", 11),
        bg=BG,
        fg=PLACEHOLDER
    ).pack(pady=(0, 20))

    # --- Scrollable container ---
        container = tk.Frame(frame, bg=BG)
        container.pack(fill="both", expand=True, padx=40, pady=10)

        canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG)

        scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

        canvas.create_window((0, 0), window=scroll_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=100)  # center with padding
        scrollbar.pack(side="right", fill="y")

    # --- Two-column subject buttons ---
        languages = f.list_languages()
        for i, lang in enumerate(languages):
            row = i // 2   # integer division → row index
            col = i % 2    # remainder → column index

            btn = tk.Button(
            scroll_frame,
            text=f"{lang.upper()}",
            font=("Segoe UI", 12, "bold"),
            bg=ACTIVE,
            fg="white",
            width=20,
            height=2,
            relief="flat",
            cursor="hand2",
            activebackground=HOVER,
            command=lambda l=lang: self.build_main_ui(l)
        )
            btn.grid(row=row, column=col, padx=20, pady=12, sticky="nsew")

    # Make columns expand evenly
        scroll_frame.grid_columnconfigure(0, weight=1)
        scroll_frame.grid_columnconfigure(1, weight=1)

    # -------- BUILD MAIN UI --------
    def build_main_ui(self, selected_lang):
        self.clear_root()

        self.sidebar = tk.Frame(self.root, bg=SIDEBAR, width=220)
        self.sidebar.pack(side="left", fill="y")

        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="right", fill="both", expand=True)

        self.build_sidebar()

        self.active_lang = selected_lang
        self.highlight_active_language()

        self.show_topics(selected_lang)



    # -------- SIDEBAR --------
    def build_sidebar(self):
        tk.Label(
            self.sidebar,
            text="Subjects",
            bg=SIDEBAR,
            fg=TEXT,
            font=("Segoe UI", 14, "bold")
        ).pack(pady=12)

        for lang in f.list_languages():
            btn = tk.Label(
                self.sidebar,
                text=f"  {lang.upper()}",
                bg=SIDEBAR,
                fg=TEXT,
                font=("Segoe UI", 11),
                anchor="w",
                padx=10,
                pady=8,
                cursor="hand2"
            )
            btn.pack(fill="x")

            btn.bind("<Button-1>", lambda e, l=lang: self.on_sidebar_click(l))
            btn.bind("<Enter>", lambda e: e.widget.config(bg=HOVER))
            btn.bind("<Leave>", lambda e: self.highlight_active_language())

        tk.Button(
            self.sidebar,
            text="Home",
            bg="#ff6b6b",
            fg="white",
            relief="flat",
            cursor="hand2",
            activebackground="#ff5252",
            command=self.show_language_home
        ).pack(side="bottom", pady=12, ipadx=10, ipady=5)

    def on_sidebar_click(self, lang):
        self.active_lang = lang
        self.highlight_active_language()
        self.show_topics(lang)

    def highlight_active_language(self):
        for child in self.sidebar.winfo_children():
            if isinstance(child, tk.Label):
            # Use .strip() and .upper() carefully
            # Better: store the 'lang' name in a custom attribute on the widget
                clean_text = child.cget("text").strip().upper()
                if self.active_lang and clean_text == self.active_lang.upper():
                    child.config(bg=ACTIVE, fg=TEXT)
                else:
                    child.config(bg=SIDEBAR, fg=TEXT)

    # -------- SEARCH --------
    def add_placeholder(self, entry, text):
        entry.insert(0, text)
        entry.config(fg=PLACEHOLDER)

        def on_focus_in(e):
            if entry.get() == text:
                entry.delete(0, "end")
                entry.config(fg="#000000")

        def on_focus_out(e):
            if entry.get() == "":
                entry.insert(0, text)
                entry.config(fg=PLACEHOLDER)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def filter_files(self, event=None):
        query = self.search_var.get().lower()
        if query == "search topics..." or query == "":
            self.render_files(self.all_files)
            return
        filtered = [f for f in self.all_files if query in f.lower()]
        self.render_files(filtered)

    def show_topics(self, lang):
        self.clear_main()
        self.active_lang = lang

        # 1. Header Section (Stretches horizontally)
        tk.Label(
            self.main,
            text=f"{lang.upper()} Topics",
            bg=BG, fg=TEXT,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(15, 5), fill="x")

        # 2. Search Bar (Responsive width with side padding)
        self.search_var = tk.StringVar()
        search = tk.Entry(
            self.main,
            textvariable=self.search_var,
            font=("Segoe UI", 11),
            bg=CARD, fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            bd=10
        )
        search.pack(pady=10, padx=40, fill="x")
        self.add_placeholder(search, "Search topics...")
        search.bind("<KeyRelease>", self.filter_files)

        # 3. Responsive Scroll Area Container
        container = tk.Frame(self.main, bg=BG)
        container.pack(fill="both", expand=True, padx=20)

        canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, command=canvas.yview)
        
        # This is the inner frame that holds the cards
        self.content = tk.Frame(canvas, bg=BG)

        # --- RESPONSIVENESS LOGIC ---
        # A. Update the scrollable area when widgets are added
        self.content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # B. THIS IS THE KEY: Force the inner frame to always match the canvas width
        canvas_window = canvas.create_window((0, 0), window=self.content, anchor="nw")
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(canvas_window, width=e.width)
        )
        # ----------------------------

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mousewheel support for Windows
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Initial Render
        self.all_files = f.list_topics(lang)
        self.render_files(self.all_files)

    # -------- RENDER FILES --------
    def render_files(self, files):
        for widget in self.content.winfo_children():
            widget.destroy()

        if not files:
            tk.Label(
                self.content,
                text="No matching topics found",
                bg=BG,
                fg=PLACEHOLDER,
                font=("Segoe UI", 11)
            ).pack(pady=30)
            return

        for file in files:
            path = f.file_path(self.active_lang, file)

            card = tk.Frame(self.content, bg=CARD)
            card.pack(fill="x", padx=20, pady=5)

            # icon = self.get_icon(file)

            lbl = tk.Label(
                card,
                text=f"{file}",
                bg=CARD,
                fg=TEXT,
                anchor="center",
                font=("Segoe UI", 11),
                padx=12,
                pady=10,
                cursor="hand2"
            )
            lbl.pack(side="left", fill="x", expand=True)

            lbl.bind("<Button-1>", lambda e, p=path, f=file: self.open_file(p, f))
            lbl.bind("<Enter>", lambda e: e.widget.config(bg=ACTIVE))
            lbl.bind("<Leave>", lambda e: e.widget.config(bg=CARD))

    # -------- OPEN FILE --------
    def open_file(self, path, file):
        f.open_file(path)

        if file not in self.recent_files:
            self.recent_files.insert(0, file)
            if len(self.recent_files) > 5:
                self.recent_files.pop()

        self.render_files(self.all_files)