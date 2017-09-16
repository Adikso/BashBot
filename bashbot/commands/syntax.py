class SyntaxBuilder:
    def __init__(self):
        self.root_node = SyntaxNode("root")
        self.current_node = self.root_node

    def node(self, name):
        node = SyntaxNode(name)
        node.parent = self.current_node

        self.current_node.nodes.append(node)
        self.current_node = node
        return self

    def param(self, name, action=None, multiple=False):
        node = SyntaxNode(name)
        node.parent = self.current_node
        node.param = True
        node.multiple = multiple
        node.action = action

        self.current_node.nodes.append(node)
        self.current_node = node
        return self

    def action(self, name, func_name):
        node = SyntaxNode(name)
        node.parent = self.current_node
        node.action = func_name

        self.current_node.nodes.append(node)
        self.current_node = node
        return self

    def parent(self):
        self.current_node = self.current_node.parent
        return self

    def set_action(self, action):
        self.current_node.action = action
        return self

    def build(self):
        return self.root_node


class SyntaxNode:
    def __init__(self, name):
        self.nodes = []
        self.action = None  # Function name

        self.name = name
        self.parent = None
        self.param = False
        self.multiple = False

    def get(self, name):
        for node in self.nodes:
            if node.name == name:
                return node

        return None

    def get_param(self):
        for node in self.nodes:
            if node.param:
                return node

        return None
