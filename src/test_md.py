import unittest

from blocks_md import (
    CODE,
    HEADING,
    OLIST,
    PARAGRAPH,
    QUOTE,
    ULIST,
    block_to_block_type,
    markdown_to_blocks,
)


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), QUOTE)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
