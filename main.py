import re
from collections import Counter


def read_html_file(path_to_html_file):
    with open(path_to_html_file, 'r') as f:
        html = f.read()
    return html


def extract_colours(html_content):
    colours = re.findall(r'\b[A-Z]+\b', html_content)
    colours = [colour for colour in colours if
               colour not in ['DAY', 'COLOURS', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']]
    return colours


def get_mean_colour(colours):
    colour_count = Counter(colours)
    colour_frequency = sum(colour_count.values() / len(colour_count))
    mean_colour = min(colour_count, key=lambda x: abs(colour_count[x] - colour_frequency))
    return mean_colour


HTML_FILE_PATH = 'python_class_question.html'

html_content = read_html_file(HTML_FILE_PATH)

colours = extract_colours(html_content)
print(colours)

mean_colour = get_mean_colour(colours)
print(mean_colour)
