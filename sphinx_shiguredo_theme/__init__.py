from os import path
from docutils import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform

class TableWrapperTransform(SphinxPostTransform):
    builder = ('html',)
    default_priority = 500

    def run(self, **kwargs):
        for node in self.document.traverse(nodes.table):
            table_wrapper = nodes.container()
            table_wrapper['classes'] = ['table_wrapper']
            pos = node.parent.index(node)
            node.parent.insert(pos, table_wrapper)
            node.parent.remove(node)
            table_wrapper += node

def setup(app):
    app.add_html_theme('sphinx_shiguredo_theme', path.abspath(path.dirname(__file__)))
    app.add_post_transform(TableWrapperTransform)
