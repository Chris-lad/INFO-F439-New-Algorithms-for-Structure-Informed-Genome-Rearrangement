from enum import Enum
from SignedString import SignedString


class NodeType(Enum):
    LEAF = 0
    P_NODE = 1
    Q_NODE = 2


class Node:
    def __init__(self, type, char, sign):
        self.type = type
        self.char = char
        self.sign = sign
        self.l = None
        self.r = None
        self.children = []
    
    @staticmethod
    def from_parenthesis_representation(string):
        if string[0] == '(' or string[0] == '[':
            node_type = NodeType.P_NODE if string[0] == '(' else NodeType.Q_NODE
            
            node = Node(node_type, '', '')
            substrings = []
            i = 1
            while i < len(string)-1:
                if string[i] == '[':
                    opened_count = 1
                    j = i + 1
                    while j < len(string)-1:
                        if string[j] == '[':
                            opened_count += 1
                        elif string[j] == ']':
                            opened_count -= 1
                        j += 1
                        if opened_count == 0:
                            break
                    substrings.append(string[i:j])
                    i = j
                elif string[i] == '(':
                    opened_count = 1
                    j = i + 1
                    while j < len(string)-1:
                        if string[j] == '(':
                            opened_count += 1
                        elif string[j] == ')':
                            opened_count -= 1
                        j += 1
                        if opened_count == 0:
                            break
                    substrings.append(string[i:j])
                    i = j
                elif string[i] != ' ':
                    substrings.append(string[i:i+2])
                    i += 2
                else:
                    i += 1
            for substring in substrings:
                node.add_child(Node.from_parenthesis_representation(substring))
            node.set_sign_majority_leaves()
            return node
        else:
            return Node(NodeType.LEAF, string[0], string[1])
    
    def add_child(self, child):
        self.children.append(child)

    def post_order(self):
        nodes = []
        for child in self.children:
            nodes.extend(child.post_order())
        nodes.append(self)
        return nodes
    
    def substring(self):
        string = ''
        for x in self.children:
            string += x.sign + x.char
        return SignedString(string)

    def number_of_leaves(self):
        nodes = self.post_order()
        count = 0
        for node in nodes:
            if node.type == NodeType.LEAF:
                count += 1
        return count

    def get_weight(self):
        return (self.number_of_leaves()-1)/2
    
    def __repr__(self):
        return '<' + NodeType(self.type).name + ' ' + self.sign + self.char + '>'
    
    def is_equivalent(self, other):
        for x in self.children:
            present = False
            for y in other.children:
                if x.type == y.type and x.char == y.char:
                    present = True
            if not present:
                return False
        return True
    
    def set_sign_majority_leaves(self):
        count = 0
        for node in self.post_order():
            if node.type == NodeType.LEAF:
                if node.sign == '+':
                    count += 1
                else:
                    count -= 1
        if count > 0:
            self.sign = '+'
        elif count < 0:
            self.sign = '-'
        else:
            self.sign = '*'
    
    def flip(self):
        if self.sign == '-':
            self.sign = '+'
        elif self.sign == '+':
            self.sign = '-'
        self.children.reverse()
        for child in self.children:
            child.flip()


class PQtree:
    def __init__(self, root):
        self.root = root

    def post_order(self):
        return self.root.post_order()
    
    def frontier(self):
        string = ''
        for x in self.post_order():
            if x.type == NodeType.LEAF:
                string += x.sign + x.char
        return SignedString(string)

    def flip(self):
        self.root.flip()

    def get_Q_node_count(self):
        count = 0
        nodes = self.post_order()
        for node in nodes:
            if node.type == NodeType.Q_NODE:
                count += 1
        return count

    @staticmethod
    def from_parenthesis_representation(string):
        root = Node.from_parenthesis_representation(string)
        return PQtree(root)

    @staticmethod
    def add_equivalent_colors(tree1, tree2):
        id = len(tree1.frontier().chars)
        for node1 in tree1.post_order():
            if node1.type != NodeType.LEAF:
                for node2 in tree2.post_order():
                    if node1.is_equivalent(node2):
                        node1.char = node2.char = str(id)
                        id += 1
