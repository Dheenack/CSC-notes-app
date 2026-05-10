import tkinter as tk
from tkinter import ttk
from config import *
from FileHandler import FileHandler
from UI.Sidebar import Sidebar
from UI.Topic import TopicView
from UI.Home import HomeView


try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except: pass

from UI.Home import HomeView # Add this import

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notes App - CSC")
        self.root.geometry("950x600")
        self.f = FileHandler()

        self.sidebar = None
        self.main_container = tk.Frame(self.root, bg=BG)
        self.main_container.pack(side="right", fill="both", expand=True)

        # Start at Home
        self.show_home()

    def show_home(self):
        # Remove sidebar if it exists when going back to Home
        if self.sidebar:
            self.sidebar.pack_forget() 
        
        # Clear main area
        for w in self.main_container.winfo_children(): w.destroy()
        
        # Load Home View
        home = HomeView(self.main_container, self.f.list_languages(), self.switch_to_subject)
        home.pack(fill="both", expand=True)

    def switch_to_subject(self, lang):
        # Show sidebar if it's hidden
        if not self.sidebar:
            self.sidebar = Sidebar(self.root, self.f.list_languages(), 
                                   self.switch_to_subject, self.show_home)
            self.sidebar.pack(side="left", fill="y")
        
        self.sidebar.active_lang = lang
        self.sidebar.refresh_highlight()
        
        # Clear main area and load Topic View
        for w in self.main_container.winfo_children(): w.destroy()
        topic_view = TopicView(self.main_container, self.f)
        topic_view.pack(fill="both", expand=True)
        topic_view.load_lang(lang)

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()