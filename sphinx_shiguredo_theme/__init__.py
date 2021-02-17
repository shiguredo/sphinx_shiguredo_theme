from os import path
from docutils import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform

def on_doctree_resolved(app, doctree, docname):
    from docutils import nodes
    # create same value list
    values = [node.children[0].astext() for node in doctree.traverse(nodes.section)]
    same_value_counter = { v: 0 for v in set([v for v in values if 1 < values.count(v)])}
    # add hash-based node-ID to sections
    mapping = {}
    for node in doctree.traverse(nodes.section):
        new_id = node.children[0].astext()
        if new_id in same_value_counter.keys():
            same_value_counter[new_id] += 1
            new_id += "-" + str(same_value_counter[new_id])
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
        for node in toctree.traverse(nodes.reference):
            anchorname = node.get('anchorname')
            if node.get('internal') and anchorname:
                new_anchorname = mapping.get(anchorname.replace("#", ""))
                if new_anchorname:
                    node['anchorname'] = '#' + new_anchorname

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
