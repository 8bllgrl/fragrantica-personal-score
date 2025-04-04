import os

from program.model.parfum import Enjoyment
from program.sqliteParseTest import scrape_and_store_multiple

# DATABASE_PATH = os.getenv("FRAGRANCE_DB_PATH")
DATABASE_PATH = r"D:\sqlite_exp\frag\fragrance_4420251217.db"

# Example Usage
# urls = [
#     'https://www.fragrantica.com/perfume/Bath-Body-Works/Sweater-Weather-64785.html',
#     'https://www.fragrantica.com/perfume/Maison-Martin-Margiela/Beach-Walk-15261.html',
#     'https://www.fragrantica.com/perfume/Maison-Martin-Margiela/Jazz-Club-20541.html',
#     'https://www.fragrantica.com/perfume/Yves-Saint-Laurent/Black-Opium-25324.html',
#     'https://www.fragrantica.com/perfume/Maison-Martin-Margiela/By-the-Fireplace-31623.html',
#     'https://www.fragrantica.com/perfume/Maison-Martin-Margiela/Sailing-Day-47891.html',
#     'https://www.fragrantica.com/perfume/Zoologist-Perfumes/Tyrannosaurus-Rex-51353.html',
#     'https://www.fragrantica.com/perfume/Maison-Martin-Margiela/Autumn-Vibes-67789.html',
#     'https://www.fragrantica.com/perfume/Maison-Martin-Margiela/When-the-Rain-Stops-70985.html',
#     'https://www.fragrantica.com/perfume/Zoologist-Perfumes/Northern-Cardinal-74111.html',
#     'https://www.fragrantica.com/perfume/Fine-ry/Not-Another-Cherry-79167.html',
#     'https://www.fragrantica.com/perfume/Fine-ry/Jungle-Santal-79172.html',
#     'https://www.fragrantica.com/perfume/Fine-ry/Pistachio-Please-91427.html',
#     'https://www.fragrantica.com/perfume/Fine-ry/Born-To-Empress-91434.html',
#     'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Divin-Enfant-4514.html',
#     'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Fat-Electrician-Semi-Modern-Vetiver-7139.html',
#     'https://www.fragrantica.com/perfume/Zoologist-Perfumes/Bee-58140.html',
#     'https://www.fragrantica.com/perfume/Zoologist-Perfumes/Sloth-59597.html',
#     'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Soul-Of-My-Soul-61989.html',
#     'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Exit-The-King-62701.html',
#     'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Frustration-71611.html'
# ]
# enjoyment = Enjoyment.LIKE
# scrape_and_store_multiple(urls, enjoyment, DATABASE_PATH)

urls = [
    'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Tilda-Swinton-Like-This-8893.html',
    'https://www.fragrantica.com/perfume/Zoologist-Perfumes/Squid-56294.html',
    'https://www.fragrantica.com/perfume/Zoologist-Perfumes/Chipmunk-67998.html',
    'https://www.fragrantica.com/perfume/Zoologist-Perfumes/Bat-Edition-2020-59596.html',
    'https://www.fragrantica.com/perfume/Maison-Martin-Margiela/On-A-Date-78292.html',
    'https://www.fragrantica.com/perfume/Toskovat/Empty-Wishes-Well-75419.html'
]
enjoyment = Enjoyment.LOVE
scrape_and_store_multiple(urls, enjoyment, DATABASE_PATH)



urls = [
    'https://www.fragrantica.com/perfume/Fine-ry/I-m-A-Musk-79170.html',
    'https://www.fragrantica.com/perfume/Marc-Jacobs/Daisy-Eau-So-Fresh-10858.html',
    'https://www.fragrantica.com/perfume/Maison-Martin-Margiela/Bubble-Bath-60105.html',
    'https://www.fragrantica.com/perfume/Yves-Saint-Laurent/L-Homme-734.html',
    'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Sous-Le-Pont-Mirabeau-80360.html',
    'https://www.fragrantica.com/perfume/Zoologist-Perfumes/Beaver-Maple-Edition-101664.html',
    'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/She-Was-An-Anomaly-56994.html',
    'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/You-Or-Someone-Like-You-43531.html',
    'https://www.fragrantica.com/perfume/Fine-ry/Before-The-Rainbow-79171.html',
    'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Hermann-a-mes-Cotes-me-Paraissait-une-Ombre-34730.html',
    'https://www.fragrantica.com/perfume/Fine-ry/Madame-91435.html',
    'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/I-am-Trash-Les-Fleurs-du-Dechet-50009.html',
    'https://www.fragrantica.com/perfume/Viktor-Rolf/Flowerbomb-Tiger-Lily-88986.html',
    'https://www.fragrantica.com/perfume/Zoologist-Perfumes/Snowy-Owl-64381.html',
    'https://www.fragrantica.com/perfume/Fine-ry/Midnight-Cafe-79168.html',
    'https://www.fragrantica.com/perfume/Zoologist-Perfumes/Musk-Deer-62710.html',
    'https://www.fragrantica.com/perfume/Zoologist-Perfumes/Rhinoceros-Edition-2020-64004.html',
    'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Spice-Must-Flow-53041.html',
    'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/500-Years-53040.html',
    'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Experimentum-Crucis-54453.html',
    'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Clean-Suede-82999.html'
]
enjoyment = Enjoyment.OK
scrape_and_store_multiple(urls, enjoyment, DATABASE_PATH)

urls = [
    'https://www.fragrantica.com/perfume/Fine-ry/Without-A-Trace-91430.html',
    'https://www.fragrantica.com/perfume/Maison-Martin-Margiela/Under-The-Lemon-Tree-53379.html',
    'https://www.fragrantica.com/perfume/Maison-Martin-Margiela/Lazy-Sunday-Morning-20542.html',
    'https://www.fragrantica.com/perfume/Maison-Martin-Margiela/Whispers-in-the-Library-53537.html',
    'https://www.fragrantica.com/perfume/Fine-ry/Flower-Bed-79174.html',
    'https://www.fragrantica.com/perfume/Mugler/Angel-704.html',
    'https://www.fragrantica.com/perfume/Fine-ry/Magnetic-Candy-79169.html',
    'https://www.fragrantica.com/perfume/Toskovat/Anarchist-A-78326.html',
    'https://www.fragrantica.com/perfume/Toskovat/Silent-at-The-Theme-Park-75423.html',
    'https://www.fragrantica.com/perfume/Giorgio-Armani/My-Way-62036.html',
    'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Putain-des-Palaces-4521.html',
    'https://www.fragrantica.com/perfume/Fine-ry/Mysterious-Nomad-91428.html',
    'https://www.fragrantica.com/perfume/Maison-Martin-Margiela/Dancing-On-The-Moon-41186.html',
    'https://www.fragrantica.com/perfume/Fine-ry/No-Prince-Required-103430.html',
    'https://www.fragrantica.com/perfume/Fine-ry/Sweet-On-The-Outside-79165.html',
    'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Dangerous-Complicity-15947.html',
    'https://www.fragrantica.com/perfume/Nest/Lychee-Rose-88577.html'
]
enjoyment = Enjoyment.DISLIKE
scrape_and_store_multiple(urls, enjoyment, DATABASE_PATH)

urls = [
    'https://www.fragrantica.com/perfume/Viktor-Rolf/Flowerbomb-Nectar-48062.html',
    'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/The-Ghost-In-The-Shell-69412.html',
    'https://www.fragrantica.com/perfume/Zoologist-Perfumes/Cockatiel-75184.html',
    'https://www.fragrantica.com/perfume/Etat-Libre-d-Orange/Eau-de-Protection-79013.html',
    'https://www.fragrantica.com/perfume/Zoologist-Perfumes/Rabbit-91167.html'
]

enjoyment = Enjoyment.HATE
scrape_and_store_multiple(urls, enjoyment, DATABASE_PATH)