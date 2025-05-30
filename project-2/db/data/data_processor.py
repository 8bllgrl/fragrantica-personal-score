from matplotlib.colors import to_rgb
from matplotlib import cm, pyplot as plt


class DataProcessor:
    @staticmethod
    def rgb_string_to_tuple(rgb_string):
        rgb_values = rgb_string.strip("rgb()").split(",")
        return tuple(int(v.strip()) / 255 for v in rgb_values)

    @staticmethod
    def process_accord_data(accords_data):
        accord_names = [row[0] for row in accords_data]
        accord_scores = [row[2] for row in accords_data]
        accord_colors = [DataProcessor.rgb_string_to_tuple(row[1]) for row in accords_data]
        return accord_names, accord_scores, accord_colors

    @staticmethod
    def process_note_data(notes_data):
        note_names = [row[0] for row in notes_data]
        note_scores = [row[1] for row in notes_data]
        norm = plt.Normalize(min(note_scores), max(note_scores))
        cmap = cm.get_cmap('viridis')
        note_colors = [cmap(norm(score)) for score in note_scores]
        return note_names, note_scores, note_colors