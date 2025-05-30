import matplotlib.pyplot as plt

class Plotter:
    @staticmethod
    def plot_accords(accord_names, accord_scores, accord_colors):
        plt.figure("Accords", figsize=(12, 6))
        bars = plt.bar(accord_names, accord_scores, color=accord_colors)
        plt.ylabel('Accord Score')
        plt.title('Top Perfume Accords by Score')
        plt.xticks(rotation=45, ha='right')
        Plotter._add_value_labels(bars, accord_scores)
        plt.tight_layout()

    @staticmethod
    def plot_notes(note_names, note_scores, note_colors):
        plt.figure("Notes", figsize=(12, 6))
        bars = plt.bar(note_names, note_scores, color=note_colors)
        plt.ylabel('Note Score')
        plt.title('Top Perfume Notes by Score')
        plt.xticks(rotation=45, ha='right')
        Plotter._add_value_labels(bars, note_scores)
        plt.tight_layout()

    @staticmethod
    def _add_value_labels(bars, values):
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                     f'{value}', ha='center', va='bottom', fontsize=9)

    @staticmethod
    def show_plots():
        plt.show()