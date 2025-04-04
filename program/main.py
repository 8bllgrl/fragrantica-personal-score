import os

from program.model.parfum import Enjoyment
from program.sqliteParseTest import scrape_and_store_multiple

DATABASE_PATH = os.getenv("FRAGRANCE_DB_PATH")

# Example Usage
urls = [
    'https://www.fragrantica.com/perfume/Maison-Martin-Margiela/Dancing-On-The-Moon-41186.html',
]
enjoyment = Enjoyment.DISLIKE
scrape_and_store_multiple(urls, enjoyment)
