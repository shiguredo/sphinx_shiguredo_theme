import re
from collections import defaultdict
from hashlib import sha1
from os import path

from docutils import nodes
import sphinx.addnodes
from sphinx.transforms.post_transforms import SphinxPostTransform


def strip_rst_comments(source):
    """RST ソーステキストからコメントを除去する"""
    # ディレクティブ等のパターン（コメントではない）
    directive_re = re.compile(r"^\.\.\s+[\w][\w.-]*::")
    hyperlink_re = re.compile(r"^\.\.\s+_")
    substitution_re = re.compile(r"^\.\.\s+\|")
    footnote_re = re.compile(r"^\.\.\s+\[")

    lines = source.split("\n")
    result = []
    in_comment = False
    comment_indent = 0

    for line in lines:
        stripped = line.rstrip()

        if in_comment:
            if stripped == "":
                # 空行はいったん保留（次の非空行で判断）
                result.append(("pending", line))
                continue
            current_indent = len(line) - len(line.lstrip())
            if current_indent > comment_indent:
                # コメント継続行（除去）
                # 保留中の空行もコメントの一部として除去
                result = [(t, l) for t, l in result if t != "pending"]
                continue
            else:
                # コメント終了
                in_comment = False
                # 保留中の空行をコメントの一部として除去
                result = [(t, l) for t, l in result if t != "pending"]

        # コメント開始判定
        if stripped == "..":
            # 空コメント開始
            in_comment = True
            comment_indent = 0
            continue

        if stripped.startswith(".. "):
            if (
                not directive_re.match(stripped)
                and not hyperlink_re.match(stripped)
                and not substitution_re.match(stripped)
                and not footnote_re.match(stripped)
            ):
                # コメント開始
                in_comment = True
                comment_indent = len(line) - len(line.lstrip())
                continue

        result.append(("keep", line))

    # pending が残っている場合は除去
    output_lines = [l for t, l in result if t == "keep"]

    # 3行以上の連続空行を2行にまとめる
    cleaned = []
    empty_count = 0
    for line in output_lines:
        if line.strip() == "":
            empty_count += 1
            if empty_count <= 2:
                cleaned.append(line)
        else:
            empty_count = 0
            cleaned.append(line)

    # 末尾の余分な空行を除去
    while cleaned and cleaned[-1].strip() == "":
        cleaned.pop()

    return "\n".join(cleaned) + "\n" if cleaned else ""


def on_html_page_context(app, pagename, templatename, context, doctree):
    """クリーンな RST ソースをテンプレートコンテキストに渡す"""
    try:
        source_path = app.env.doc2path(pagename)
        with open(source_path, "r", encoding="utf-8") as f:
            source = f.read()
        context["clean_rst_source"] = strip_rst_comments(source)
    except Exception:
        context["clean_rst_source"] = ""


def on_doctree_resolved(app, doctree, docname):
    # add hash-based node-ID to sections
    mapping = {}
    sequences = defaultdict(int)

    condition = lambda node: isinstance(node, (nodes.section, sphinx.addnodes.desc_signature))

    for node in doctree.traverse(condition=condition):
        # .. py ディレクティブによって作られるセクションの toctree における anchorname には _toc_name が使われる
        if isinstance(node, sphinx.addnodes.desc_signature):
            # NOTE: 非公開 attrtibute なので undocumented な sphinx の変更の影響を受ける可能性がある
            text = node["_toc_name"]
        else:
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
            if node.get("internal") and node.get("anchorname"):
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
    app.connect("html-page-context", on_html_page_context)
