import tkinter as tk
from tkinter import messagebox, filedialog
from program.dbcreator import create_db

class CreateDBTab:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.db_path_var = tk.StringVar(value=r'D:/sqlite_exp/frag/fragrance_530251032.db')

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="Database Path:").grid(row=0, column=0, sticky='w')
        tk.Entry(self.frame, textvariable=self.db_path_var, width=50).grid(row=0, column=1)
        tk.Button(self.frame, text="Browse...", command=self.browse_path).grid(row=0, column=2)

        tk.Button(self.frame, text="CREATE Database", command=self.create_database, bg="orange", fg="black").grid(row=1, column=1, pady=10)

    def browse_path(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite DB files", "*.db"), ("All files", "*.*")]
        )
        if path:
            self.db_path_var.set(path)

    def create_database(self):
        path = self.db_path_var.get()
        if not path:
            messagebox.showerror("Missing Path", "Please specify a database file path.")
            return

        try:
            create_db(path)
            messagebox.showinfo("Success", "Database created successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create database:\n{e}")
