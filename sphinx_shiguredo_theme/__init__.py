from os import path

def setup(app):
    app.add_html_theme('sphinx_shiguredo_theme', path.abspath(path.dirname(__file__)))
