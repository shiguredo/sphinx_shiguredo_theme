from collections import defaultdict
from hashlib import sha1
from os import path
import re

from docutils import nodes
from sphinx.transforms.post_transforms import SphinxPostTransform

ANCHOR_ID_PATTERN = re.compile(r"#id[0-9]+")


def on_doctree_resolved(app, doctree, docname):
    # add hash-based node-ID to sections
    mapping = {}
    sequences = defaultdict(int)
    for node in doctree.traverse(nodes.section):
        text = node.children[0].astext()
        sequences[text] += 1
        new_id = sha1("{}-{}".format(text, sequences[text]).encode("utf-8")).hexdigest()[:6]
        for node_id in node["ids"]:
            mapping[node_id] = new_id
        node["ids"].insert(0, new_id)

    # use hash-based node-IDs at local reference
    for node in doctree.traverse(nodes.reference):
        refid = node.get("refid")
        if refid in mapping:
            node["refid"] = mapping.get(refid)

    # use hash-based node-IDs at toctrees
    for _, toctree in app.env.tocs.items():
        sequences = defaultdict(int)
        for node in toctree.traverse(nodes.reference):
            anchorname = node.get("anchorname")
            # hase-based node-ID の利用は id0 のような id で始まる連番のケースに限定する
            if node.get("internal") and anchorname and ANCHOR_ID_PATTERN.match(anchorname):
                text = node.astext()
                sequences[text] += 1
                new_id = sha1("{}-{}".format(text, sequences[text]).encode("utf-8")).hexdigest()[:6]
                node["anchorname"] = "#" + new_id


def on_builder_inited(app):
    app.config.html_additional_pages["404"] = "404.html"


class TableWrapperTransform(SphinxPostTransform):
    builder = ("html",)
    default_priority = 500

    def run(self, **kwargs):
        for node in self.document.traverse(nodes.table):
            table_wrapper = nodes.container()
            table_wrapper["classes"] = ["table_wrapper"]
            pos = node.parent.index(node)
            node.parent.insert(pos, table_wrapper)
            node.parent.remove(node)
            table_wrapper += node

def setup(app):
    app.add_html_theme("sphinx_shiguredo_theme", path.abspath(path.dirname(__file__)))
    app.connect("doctree-resolved", on_doctree_resolved)
    app.add_post_transform(TableWrapperTransform)
    app.connect("builder-inited", on_builder_inited)
