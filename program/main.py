import os

from program.model.parfum import Enjoyment
from program.sqliteParseTest import scrape_and_store_multiple

#latest version:
DATABASE_PATH = r"D:\sqlite_exp\frag\fragrance_51520251243.db"
#Grapher DB(SET TO OK):
# DATABASE_PATH = r'D:\sqlite_exp\frag\fragrance_520OKONLYforgraphing.db'

urls = [
    'https://www.fragrantica.com/perfume/19-69/Miami-Blue-66722.html',
]

enjoyment = Enjoyment.LOVE
scrape_and_store_multiple(urls, enjoyment, DATABASE_PATH)