from setuptools import setup, find_namespace_packages

setup(
    name='sphinx_shiguredo_theme',
    version='2022.1.0',
    packages=find_namespace_packages(
        include=['sphinx_shiguredo_theme', 'sphinx_shiguredo_theme.*']
    ),
    entry_points={
        'sphinx.html_themes': [
            'sphinx_shiguredo_theme = sphinx_shiguredo_theme',
        ]
    },
    include_package_data=True,
    package_data={
        'sphinx_shiguredo_theme': [
            'theme.conf',
            '*.html',
            'static/css/*.css',
            'static/js/*.js',
        ]
    },
)
