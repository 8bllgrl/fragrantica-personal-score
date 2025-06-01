from enum import Enum
from typing import List

class Enjoyment(Enum):
    FAVORITE = 4
    LOVE = 3
    LIKE = 2
    OK = 1
    DISLIKE = -1
    HATE = -2
    DESPISE = -4

    @property
    def weight_multiplier(self) -> float:
        return {
            Enjoyment.FAVORITE: 1.6,
            Enjoyment.LOVE: 1.4,
            Enjoyment.LIKE: 1.2,
            Enjoyment.OK: 0.5,  # ↓ Reduced from 1.0
            Enjoyment.DISLIKE: -1.2,
            Enjoyment.HATE: -1.4,
            Enjoyment.DESPISE: -1.6
        }[self]


class NoteCategory(Enum):
    """Enum for note categories."""
    TOP = "Top Notes"
    MIDDLE = "Middle Notes"
    BASE = "Base Notes"
    UNKNOWN = "Unknown."

class Note:
    """Represents a fragrance note with properties."""

    def __init__(self, name: str, image_url: str, width: str, opacity: str, category: NoteCategory):
        self.name: str = name
        self.image_url: str = image_url
        self.width: str = width
        self.opacity: str = opacity
        self.category: NoteCategory = category

    def __repr__(self) -> str:
        return f"Note(name='{self.name}', category='{self.category.name}', width='{self.width}', opacity='{self.opacity}', image_url='{self.image_url}')"


class Accord:
    """Represents an accord with its properties."""

    def __init__(self, name: str, background: str, width: str, opacity: str):
        self.name: str = name
        self.background: str = background
        self.opacity: str = opacity

        # Normalize the width
        if '%' in width:
            self.width: float = float(width.strip('%')) / 100
        else:
            self.width: float = float(width)

    def __repr__(self) -> str:
        return f"Accord(name='{self.name}', background='{self.background}', width={self.width}, opacity='{self.opacity}')"



class PerfumeDetails:
    """Class that holds the details of a perfume including its name, accords, and notes."""

    def __init__(self, perfume_name: str, accords: List[Accord], notes: List[Note], url: str):
        self.perfume_name: str = perfume_name
        self.accords: List[Accord] = accords
        self.notes: List[Note] = notes
        self.url: str = url

    def __repr__(self) -> str:
        return f"PerfumeDetails(perfume_name='{self.perfume_name}', accords={self.accords}, notes={self.notes})"
