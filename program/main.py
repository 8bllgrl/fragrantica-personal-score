import os

from program.model.parfum import Enjoyment
from program.sqliteParseTest import scrape_and_store_multiple

# DATABASE_PATH = os.getenv("FRAGRANCE_DB_PATH")
DATABASE_PATH = r"D:\sqlite_exp\frag\fragrance_4420251217.db"

# Example Usage
urls = [
    'https://www.fragrantica.com/perfume/Maison-Martin-Margiela/Dancing-On-The-Moon-41186.html',
]
enjoyment = Enjoyment.HATE
scrape_and_store_multiple(urls, enjoyment, DATABASE_PATH)
