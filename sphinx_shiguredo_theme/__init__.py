from os import path
import re

from docutils import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform

def delete_html_escape_string(string):
    escape_strings = ['<', '>', ' ', '　', '&', '"', "'"]
    result = string
    for s in escape_strings:
        result = result.replace(s, '')
    return result

def on_doctree_resolved(app, doctree, docname):
    # add hash-based node-ID to sections
    section_text_list = [node.children[0].astext() for node in doctree.traverse(nodes.section)]
    doctree_same_values = set([v for v in section_text_list if 1 < section_text_list.count(v)])
    mapping = {}
    for node in doctree.traverse(nodes.section):
        new_id = node.children[0].astext()
        if new_id in doctree_same_values:
            new_id += '-{}'.format(node['ids'][-1])
        new_id = delete_html_escape_string(new_id)
        for node_id in node['ids']:
            mapping[node_id] = new_id
        node['ids'].insert(0, new_id)
    # use hash-based node-IDs at local reference
    for node in doctree.traverse(nodes.reference):
        refid = node.get('refid')
        if refid in mapping:
            node['refid'] = mapping.get(refid)
    # use hash-based node-IDs at toctrees
    for _, toctree in app.env.tocs.items():
        reference_text_list = [node.astext() for node in toctree.traverse(nodes.reference)]
        toctree_same_values = set([v for v in reference_text_list if 1 < reference_text_list.count(v)])
        for node in toctree.traverse(nodes.reference):
            if node.get('internal') and node.get('anchorname'):
                node_text = node.astext()
                if node_text in toctree_same_values:
                    original_anchorname = re.sub('^#', '', node.get('anchorname'))
                    if delete_html_escape_string(node_text) not in original_anchorname:
                        node['anchorname'] = '#{}-{}'.format(delete_html_escape_string(node.astext()), original_anchorname)
                else:
                    node['anchorname'] = '#{}'.format(delete_html_escape_string(node.astext()))


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
    app.connect('doctree-resolved', on_doctree_resolved)
    app.add_post_transform(TableWrapperTransform)
