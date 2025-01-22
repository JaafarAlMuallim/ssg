import unittest

from block_html import markdown_to_html_node


class TestBlockHTML(unittest.TestCase):
    def test_block_html(self):
        text = """
# Heading

Paragraph

* List 1
* List 2

1. List 2
2. List 2

[Link](https://x.com)

![Image](img src)

*italic text*

**bold text**

Inline `code`
"""
        blocks = markdown_to_html_node(text)

        value = "ParentNode(div, children: [LeafNode(h1, Heading, None), LeafNode(p, Paragraph, None), ParentNode(ul, children: [LeafNode(li, List 1, None), LeafNode(li, List 2, None)], None), ParentNode(ol, children: [LeafNode(li, List 2, None), LeafNode(li, List 2, None)], None), LeafNode(link, Link, {'url': 'https://x.com'}), LeafNode(img, Image, {'url': 'img src'}), LeafNode(i, italic text, None), LeafNode(b, bold text, None), HTMLNode(p, Inline , children: [LeafNode(code, code, None)], None)], None)"
        self.assertEqual(repr(blocks), value)
