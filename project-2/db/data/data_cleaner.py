#!/usr/bin/env python3
import sqlite3

# Fix imports for direct execution (e.g., in PyCharm)
if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from db.database_connector import DatabaseConnector
else:
    from ..database_connector import DatabaseConnector


class DataCleaner:
    consolidation_rules = {
        "Vetiver": (135, ["Java vetiver oil", "Vetyver", "Haitian Vetiver", "Tahitian Vetiver", "Bourbon vetiver"]),
        "Civet": (46, ["Synthetic Civet"]),
        "Neroli": (20, ["neroli", "neroli essence", "Orange Blossom"]),
        "Lemon": (10, ["amalfi lemon", "lemon zest"]),
        "Rose": (
            44, ["turkish rose", "damask rose", "rose oil", "rose", "white rose", "rose de mai", "bulgarian rose",
                 "rose hip"]),
        "Cedarwood": (
        13, ["virginia cedar", "virginian cedar", "atlas cedar", "himalayan cedar", "cedarwood", "Texas Cedar"]),
        "Cashmere Wood": (29, ["cashmeran", "Cashmere Wood", "cashmere", "cashmere musk"]),
        "Iris": (40, ["orris", "orris root"]),
        "Almond": (72, ["bitter almond", "white almond"]),
        "Incense": (114, ["kyara incense"]),
        "Jasmine": (
            24, ["indian jasmine", "egyptian jasmine", "jasmine sambac", "night blooming jasmine", "water jasmine"]),
        "Patchouli": (25, ["indonesian patchouli leaf", "indian patchouli"]),
        "Tobacco": (84, ["tobacco leaf", "tobacco absolute", "tobacco accord"]),
        "Whiskey": (200, ["rum", "bourbon whiskey"]),
        "Sage": (145, ["clary sage"]),
        "Ambrette (Musk Mallow)": (194, ["ambrettolide", "Ambrette"]),
        "Champagne": (261, ["champagne rosé", "champagne rose", "prosecco"]),
        "Tea": (285, ["green tea", "black tea", "oolong tea", "rooibos tea", "lapsang souchong tea"]),
        "Black Currant": (182, ["blackcurrant syrup"]),
        "Vanilla": (21, ["vanille", "vanilla bean", "madagascar vanilla", "bourbon vanilla", "vanilla absolute"]),
        "Sandalwood": (96, ["sandalowood", "australian sandalwood"]),
        "Myrrh": (109, ["myrhh"]),
        "Chocolate": (240, ["Cacao", "cocoa shell", "cocoa"]),
        "Spices": (158, ["spicy notes"]),
        "Labdanum": (98, ["french labdanum"]),
        "Coconut": (156, ["coconut milk", "coconut water"]),
        "Clove": (32, ["clove", "cloves"]),
        "Oud": (390, ["agarwood (oud)", "laotian oud"]),
        "Tonka Bean": (78, ["coumarin"]),
        "Apple": (1, ["granny smith apple", "green apple", "apple"]),
        "Metallic Notes": (147, ["metal notes"]),
        "Elemi": (165, ["elemi resin"]),
        "Stone": (143, ["pebbles"]),
        "Bay Leaf": (53, ["west indian bay"]),
        "Woody Notes": (214, ["woodsy notes"]),
        "Pepperwood™": (181, ["pepperwood or hercules club", "Pepperwood™"]),
        "Hyacinth": (372, ["hiacynth", "blue hyacinth"]),
        "Marshmallow": (82, ["marshamallow", "marshmallow"]),
        "Strawberry": (423, ["big strawberry"]),
        "Green Notes": (66, ["green accord"]),
        "Water Notes": (367, ["watery notes", "rain notes"]),
        "Sea Water": (387, ["aquatic notes", "sea notes"]),
        "Osmanthus": (58, ["chinese osmanthus"]),
        "Pine": (207, ["pine tree", "pine needles"]),
        "Hinoki Wood": (247, ["hinoki"]),
        "Fir": (50, ["fir resin", "balsam fir"]),
        "Musk": (7, ["white musk", "Velvet", "Paper", "Silk"]),
        "Salt": (177, ["sea salt", "salt"]),
        "Oakmoss": (69, ["moss"]),
        "Earthy Notes": (141, ["soil tincture"]),
        "Chestnut": (30, ["marron glace"]),
        "Violet": (150, ["Violet Leaf", "Violet", "Black Violet"]),
        "Bamboo": (342, ["Bamboo Leaf", "Bamboo"]),
        "Cherry": (71, ["Cherry", "Cherry Blossom", "Maraschino Cherry"]),

        # Add more consolidation rules here
    }

    def __init__(self, database_path):
        self.database_path = database_path
        self.db_connector = DatabaseConnector(database_path)

    def find_note_ids_by_names(self, note_names):
        """
        Finds the IDs of notes given a list of note names, case-insensitively,
        and trims leading/trailing whitespace from the note names before comparison.
        """
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        # Convert and trim note names to lowercase for comparison
        processed_names = [name.lower().strip() for name in note_names]
        placeholders = ','.join(['?'] * len(processed_names))

        cursor.execute(
            f"SELECT id, name FROM Notes WHERE LOWER(TRIM(name)) IN ({placeholders})",
            processed_names
        )

        # Map found trimmed and lowercased names back to their IDs
        name_to_id = {row[1].lower().strip(): row[0] for row in cursor.fetchall()}
        conn.close()
        return name_to_id

    def consolidate_by_mapping(self):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        for consolidated_name, (consolidated_id, similar_names) in self.consolidation_rules.items():
            name_to_id = self.find_note_ids_by_names(similar_names)
            ids_to_replace = [note_id for name, note_id in name_to_id.items()
                              if note_id != consolidated_id and name in [n.lower() for n in similar_names]]

            if not ids_to_replace:
                print(f"No notes found to consolidate into '{consolidated_name}' from: {similar_names}")
                continue

            try:
                cursor.execute(f"""
                    UPDATE PerfumeNotes
                    SET note_id = ?
                    WHERE note_id IN ({','.join('?' * len(ids_to_replace))})
                """, (consolidated_id,) + tuple(ids_to_replace))
                conn.commit()
                print(
                    f"Updated PerfumeNotes: Replaced {ids_to_replace} with {consolidated_id} ('{consolidated_name}').")

                cursor.execute(f"""
                    DELETE FROM Notes
                    WHERE id IN ({','.join('?' * len(ids_to_replace))})
                """, tuple(ids_to_replace))
                conn.commit()
                print(f"Deleted obsolete notes with IDs: {ids_to_replace}.")

            except sqlite3.Error as e:
                conn.rollback()
                print(f"Database error during consolidation for '{consolidated_name}': {e}")

        conn.close()


if __name__ == "__main__":
    DATABASE_PATH = r"D:\sqlite_exp\frag\fragrance_51520251243.db"
    # DATABASE_PATH =  r'D:\sqlite_exp\frag\fragrance_520OKONLYforgraphing.db'
    cleaner = DataCleaner(DATABASE_PATH)
    cleaner.consolidate_by_mapping()
