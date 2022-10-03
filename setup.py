from setuptools import setup, find_packages

setup(
    name='sphinx_shiguredo_theme',
    version='2022.1.0',
    packages=find_packages('sphinx_shiguredo_theme'),
    entry_points={
        'sphinx.html_themes': [
            'sphinx_shiguredo_theme = sphinx_shiguredo_theme',
        ]
    }
)
