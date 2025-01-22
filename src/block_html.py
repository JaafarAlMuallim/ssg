from blocks_md import block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_md import text_to_textnodes
from textnode import TextType


def markdown_to_html_node(markdown):
    structure = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        structure.append(text_to_children(block, block_type))
    return ParentNode("div", structure)


def text_to_children(block, block_type):
    match block_type:
        case "quote":
            return LeafNode("blockquote", block.split("> ")[1])

        case "unordered_list":
            lst = block.split("\n")
            children = []
            for line in lst:
                if line.startswith("* "):
                    textnodes = text_to_textnodes(line.split("* ")[1])
                    if len(textnodes) == 1:
                        children.append(LeafNode("li", line.split("* ")[1]))
                        continue
                    inner_child = []
                    for i, textnode in enumerate(textnodes):
                        inner_child.append(
                            LeafNode(
                                text_type_to_tag(textnode.text_type),
                                textnode.text,
                                (
                                    {"href": textnodes[0].url}
                                    if textnodes[0].url is not None
                                    else None
                                ),
                            )
                        )
                        children.append(inner_child)

                elif line.startswith("- "):
                    textnodes = text_to_textnodes(line.split("- ")[1])
                    if len(textnodes) == 1:
                        children.append(LeafNode("li", line.split("- ")[1]))
                        continue
                    inner_child = []
                    for i, textnode in enumerate(textnodes):
                        inner_child.append(
                            LeafNode(
                                text_type_to_tag(textnode.text_type),
                                textnode.text,
                                (
                                    {"href": textnodes[0].url}
                                    if textnodes[0].url is not None
                                    else None
                                ),
                            )
                        )
                    children.append(ParentNode("li", inner_child))

            return ParentNode("ul", children)

        case "ordered_list":
            lst = block.split("\n")
            children = []
            for (
                i,
                line,
            ) in enumerate(lst):
                textnodes = text_to_textnodes(line.split(f"{i + 1}. ")[1])
                if len(textnodes) == 1:
                    children.append(LeafNode("li", line.split(f"{i + 1}. ")[1]))
                    continue
                inner_child = []
                for i, textnode in enumerate(textnodes):
                    inner_child.append(
                        LeafNode(
                            text_type_to_tag(textnode.text_type),
                            textnode.text,
                            (
                                {"href": textnodes[0].url}
                                if textnodes[0].url is not None
                                else None
                            ),
                        )
                    )
                    children.append(ParentNode("li", inner_child))
            return ParentNode("ol", children)

        case "code":
            return LeafNode("code", block.split("```")[1])

        case "heading":
            tag = "h6"
            value = block
            for i in range(6, 0, -1):
                pattern = f"{'#' * i} "
                if value.startswith(pattern):
                    tag = f"h{i}"
                    value = block.split(pattern)[1]
                    break
            return LeafNode(tag, value)

        case _:
            textnodes = text_to_textnodes(block)
            parent = False
            children = []
            if len(textnodes) > 1:
                parent = True

            for i, node in enumerate(textnodes):
                if parent and i == 0:
                    continue
                if parent:
                    children.append(
                        LeafNode(
                            text_type_to_tag(node.text_type),
                            node.text,
                            {"href": node.url} if node.url is not None else None,
                        )
                    )
            if parent:
                text_type = text_type_to_tag(textnodes[0].text_type)
                if textnodes[0].text is not None:
                    children.insert(
                        0,
                        LeafNode(text_type, textnodes[0].text),
                    )
                if text_type is None:
                    text_type = "p"
                return ParentNode(
                    text_type,
                    children,
                )
            prop = {}
            if text_type_to_tag(textnodes[0].text_type) == "a":
                prop["url"] = textnodes[0].url
            if text_type_to_tag(textnodes[0].text_type) == "img":
                prop["src"] = textnodes[0].url

            return LeafNode(
                text_type_to_tag(textnodes[0].text_type),
                textnodes[0].text,
                prop if textnodes[0].url is not None else None,
            )


def text_type_to_tag(text_type):
    match text_type:
        case TextType.NORMAL:
            return None
        case TextType.BOLD:
            return "b"
        case TextType.ITALIC:
            return "i"
        case TextType.CODE:
            return "code"
        case TextType.IMAGE:
            return "img"
        case TextType.LINK:
            return "a"
