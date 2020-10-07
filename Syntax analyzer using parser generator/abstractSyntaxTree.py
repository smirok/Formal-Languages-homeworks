class Node:
    def __init__(self, type, children=None):
        if children is None:
            children = []
        self.children = children
        self.type = type
        self.leaf = len(self.children) == 0


def traverse(output_file, root: Node, space: str):
    output_file.write(f'{space}{root.type}\n')
    if root.leaf:
        return

    for kid in root.children:
        traverse(output_file, kid, space=space + '--')
