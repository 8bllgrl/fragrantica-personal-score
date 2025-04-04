from enum import Enum

class Enjoyment(Enum):
    LOVE = 3
    LIKE =2
    OK =1
    DISLIKE = -1
    HATE = -2

class NoteCategory(Enum):
    """Enum for note categories."""
    TOP = "Top Notes"
    MIDDLE = "Middle Notes"
    BASE = "Base Notes"
    UNKNOWN = "Unknown."


class Note:
    """Represents a fragrance note with properties."""

    def __init__(self, name, image_url, width, opacity, category):
        self.name = name
        self.image_url = image_url
        self.width = width
        self.opacity = opacity
        self.category = category

    def __repr__(self):
        return f"Note(name='{self.name}', category='{self.category.name}', width='{self.width}', opacity='{self.opacity}', image_url='{self.image_url}')"


class Accord:
    """Represents an accord with its properties."""

    def __init__(self, name, background, width, opacity):
        self.name = name
        self.background = background
        self.width = width
        self.opacity = opacity

    def __repr__(self):
        return f"Accord(name='{self.name}', background='{self.background}', width='{self.width}', opacity='{self.opacity}')"


class PerfumeDetails:
    """Class that holds the details of a perfume including its name, accords, and notes."""

    def __init__(self, perfume_name, accords, notes, url):
        self.perfume_name = perfume_name
        self.accords = accords
        self.notes = notes
        self.url = url

    def __repr__(self):
        return f"PerfumeDetails(perfume_name='{self.perfume_name}', accords={self.accords}, notes={self.notes})"
