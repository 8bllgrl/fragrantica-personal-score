import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.simpledialog import askstring
import subprocess
import os
import sys

from program.model.parfum import Enjoyment
from program.sqliteParseTest import scrape_and_store_multiple


class FragranceScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fragrance Scraper GUI")

        self.database_path = tk.StringVar()
        self.enjoyment_level = tk.StringVar(value="LOVE")
        self.urls = []

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.scraper_tab = ttk.Frame(self.notebook)
        self.visualizer_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.scraper_tab, text="Scraper")
        self.notebook.add(self.visualizer_tab, text="Visualizers")

        self.setup_scraper_tab()
        self.setup_visualizer_tab()

    def setup_scraper_tab(self):
        tab = self.scraper_tab

        tk.Label(tab, text="Database:").grid(row=0, column=0, sticky='w')
        tk.Entry(tab, textvariable=self.database_path, width=50).grid(row=0, column=1)
        tk.Button(tab, text="Browse...", command=self.select_db).grid(row=0, column=2)

        tk.Label(tab, text="Enjoyment:").grid(row=1, column=0, sticky='w')
        tk.OptionMenu(tab, self.enjoyment_level, *Enjoyment.__members__.keys()).grid(row=1, column=1, sticky='w')

        tk.Label(tab, text="URLs:").grid(row=2, column=0, sticky='nw')
        self.url_listbox = tk.Listbox(tab, height=8, width=60)
        self.url_listbox.grid(row=2, column=1, columnspan=2, sticky='w')

        tk.Button(tab, text="Add URL", command=self.add_url).grid(row=3, column=0, sticky='w')
        tk.Button(tab, text="Remove Selected", command=self.remove_selected_url).grid(row=3, column=2, sticky='w')
        tk.Button(tab, text="Remove All", command=self.remove_all_urls).grid(row=3, column=1, sticky='e')

        tk.Button(tab, text="Scrape & Store", command=self.run_scraper, bg="green", fg="white").grid(row=4, column=1, pady=10)

    def setup_visualizer_tab(self):
        tab = self.visualizer_tab

        tk.Label(tab, text="Database:").grid(row=0, column=0, sticky='w')
        tk.Entry(tab, textvariable=self.database_path, width=50).grid(row=0, column=1)
        tk.Button(tab, text="Browse...", command=self.select_db).grid(row=0, column=2)

        tk.Button(tab, text="Show Plot", command=self.run_visualizer, bg="blue", fg="white").grid(row=2, column=1, pady=10)

    def select_db(self):
        path = filedialog.askopenfilename(filetypes=[("SQLite DB files", "*.db"), ("All files", "*.*")])
        if path:
            self.database_path.set(path)

    def add_url(self):
        url = askstring("Add URL", "Enter fragrance URL:")
        if url:
            self.urls.append(url)
            self.url_listbox.insert(tk.END, url)

    def remove_selected_url(self):
        selected = self.url_listbox.curselection()
        for index in reversed(selected):
            self.url_listbox.delete(index)
            del self.urls[index]

    def remove_all_urls(self):
        self.url_listbox.delete(0, tk.END)
        self.urls.clear()

    def run_scraper(self):
        if not self.database_path.get():
            messagebox.showerror("Missing Database", "Please select a database file.")
            return

        if not self.urls:
            messagebox.showerror("No URLs", "Please add at least one URL.")
            return

        enjoyment = Enjoyment[self.enjoyment_level.get()]
        try:
            scrape_and_store_multiple(self.urls, enjoyment, self.database_path.get())
            messagebox.showinfo("Done", "Scraping completed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def run_visualizer(self):
        db_path = self.database_path.get()

        if not db_path:
            messagebox.showerror("Missing Database", "Please select a database file.")
            return

        script_dir = os.path.dirname(os.path.abspath(__file__))
        visualizer_path = os.path.join(script_dir, "..", "visualizer", "matplotvisualizer.py")
        visualizer_path = os.path.abspath(visualizer_path)

        try:
            subprocess.Popen([sys.executable, visualizer_path, db_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch visualizer:\n{e}")


# --- Run the GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FragranceScraperGUI(root)
    root.mainloop()
