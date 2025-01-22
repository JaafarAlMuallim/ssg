class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.value is None or self.children is None or len(self.children) == 0:
            raise ValueError("HTMLNode should have at least one chlid or a value")
        elif self.children is None or len(self.children) == 0:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        elif self.value is None or self.value == "":
            all_children = ""
            for chlid in self.children:
                all_children += chlid.to_html()
            return f"<{self.tag}{self.props_to_html()}>{all_children}</{self.tag}>"
        else:
            all_children = ""
            for chlid in self.children:
                all_children += chlid.to_html()
            if self.tag is None:
                return f"{self.value}{all_children}"
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>{all_children}"

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        if self.tag is None:
            self.tag = "p"
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
