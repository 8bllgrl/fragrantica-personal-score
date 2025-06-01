from program.visualizer.matplotvisualizer import show_plot
import tkinter as tk
from tkinter import messagebox

class VisualizerTab:
    def __init__(self, parent, database_path_var):
        self.frame = tk.Frame(parent)
        self.database_path = database_path_var
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="Database:").grid(row=0, column=0, sticky='w')
        tk.Entry(self.frame, textvariable=self.database_path, width=50).grid(row=0, column=1)
        tk.Button(self.frame, text="Browse...", command=self.select_db).grid(row=0, column=2)

        tk.Button(self.frame, text="Show Plot", command=self.run_visualizer, bg="blue", fg="white").grid(row=2, column=1, pady=10)

    def select_db(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(filetypes=[("SQLite DB files", "*.db"), ("All files", "*.*")])
        if path:
            self.database_path.set(path)

    def run_visualizer(self):
        db_path = self.database_path.get()
        if not db_path:
            messagebox.showerror("Missing Database", "Please select a database file.")
            return
        try:
            show_plot(db_path)  # Call the function directly
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch visualizer:\n{e}")
