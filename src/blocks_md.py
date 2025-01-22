PARAGRAPH = "paragraph"
HEADING = "heading"
CODE = "code"
QUOTE = "quote"
OLIST = "ordered_list"
ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return PARAGRAPH
        return QUOTE
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return PARAGRAPH
        return ULIST
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return PARAGRAPH
        return ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return PARAGRAPH
            i += 1
        return OLIST
    return PARAGRAPH
