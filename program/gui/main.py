import tkinter as tk
from tkinter import ttk

from tabs.scraper_tab import ScraperTab
from tabs.visualizer_tab import VisualizerTab
from tabs.create_db_tab import CreateDBTab

class FragranceScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fragrance Scraper GUI")

        self.database_path = tk.StringVar()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.scraper_tab = ScraperTab(self.notebook, self.database_path)
        self.visualizer_tab = VisualizerTab(self.notebook, self.database_path)
        self.create_db_tab = CreateDBTab(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.scraper_tab.frame, text="Scraper")
        self.notebook.add(self.visualizer_tab.frame, text="Visualizers")
        self.notebook.add(self.create_db_tab.frame, text="Create DB")

if __name__ == "__main__":
    root = tk.Tk()
    app = FragranceScraperGUI(root)
    root.mainloop()
