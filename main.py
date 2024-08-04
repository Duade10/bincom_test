import re


def read_html_file(path_to_html_file):
    with open(path_to_html_file, 'r') as f:
        html = f.read()
    return html


HTML_FILE_PATH = 'python_class_question.html'

html_content = read_html_file(HTML_FILE_PATH)

print(html_content)