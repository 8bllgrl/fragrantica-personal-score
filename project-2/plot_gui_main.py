import sys
import os

from db.database_connector import DatabaseConnector
from db.queries import Query
from db.data.data_processor import DataProcessor
from gui.plotter import Plotter


# Database path
DATABASE_PATH = r"D:\sqlite_exp\frag\fragrance_51520251243.db"

# Initialize Database Connector
db_connector = DatabaseConnector(DATABASE_PATH)

# Get queries from the Query class
query_accords = Query.get_accords_query()
query_notes = Query.get_notes_query()

# Fetch data
accords_data = db_connector.fetch_data(query_accords)
notes_data = db_connector.fetch_data(query_notes)

if accords_data and notes_data:
    # Process data
    accord_names, accord_scores, accord_colors = DataProcessor.process_accord_data(accords_data)
    note_names, note_scores, note_colors = DataProcessor.process_note_data(notes_data)

    # Plot data
    Plotter.plot_accords(accord_names, accord_scores, accord_colors)
    Plotter.plot_notes(note_names, note_scores, note_colors)

    # Show plots
    Plotter.show_plots()
else:
    print("Failed to retrieve data from the database.")