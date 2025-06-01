import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import messagebox
from program.model.parfum import Enjoyment
from program.sqliteParseTest import scrape_and_store_multiple

class ScraperTab:
    def __init__(self, parent, database_path_var):
        self.frame = tk.Frame(parent)
        self.database_path = database_path_var
        self.enjoyment_level = tk.StringVar(value="LOVE")
        self.urls = []

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="Database:").grid(row=0, column=0, sticky='w')
        tk.Entry(self.frame, textvariable=self.database_path, width=50).grid(row=0, column=1)
        tk.Button(self.frame, text="Browse...", command=self.select_db).grid(row=0, column=2)

        tk.Label(self.frame, text="Enjoyment:").grid(row=1, column=0, sticky='w')
        tk.OptionMenu(self.frame, self.enjoyment_level, *Enjoyment.__members__.keys()).grid(row=1, column=1, sticky='w')

        tk.Label(self.frame, text="URLs:").grid(row=2, column=0, sticky='nw')
        self.url_listbox = tk.Listbox(self.frame, height=8, width=60)
        self.url_listbox.grid(row=2, column=1, columnspan=2, sticky='w')

        tk.Button(self.frame, text="Add URL", command=self.add_url).grid(row=3, column=0, sticky='w')
        tk.Button(self.frame, text="Remove Selected", command=self.remove_selected_url).grid(row=3, column=2, sticky='w')
        tk.Button(self.frame, text="Remove All", command=self.remove_all_urls).grid(row=3, column=1, sticky='e')

        tk.Button(self.frame, text="Scrape & Store", command=self.run_scraper, bg="green", fg="white").grid(row=4, column=1, pady=10)

    def select_db(self):
        from tkinter import filedialog
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
