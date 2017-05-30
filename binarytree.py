from random import sample, random


class Node(object):
    """Represents a binary tree node."""

    def __init__(self, value, parent=None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent

    def __repr__(self):
        l = self.left.value if self.left is not None else None
        r = self.right.value if self.right is not None else None
        p = self.parent.value if self.parent is not None else None
        return 'Node(value={}, left={}, right={}, parent={})'.format(self.value,
                                                                     l, r, p)

    def __str__(self):
        return stringify(self)

    def to_list(self):
        return convert(self)


def _build_list(root):
    """Build a list from a tree and return it"""
    result = []
    current_nodes = [root]
    level_not_empty = True

    while level_not_empty:
        level_not_empty = False
        next_nodes = []

        for node in current_nodes:
            if node == None:
                result.append(None)
                next_nodes.append(None)
                next_nodes.append(None)
            else:
                result.append(node.value)

                left_child = node.left
                right_child = node.right

                if left_child != None:
                    level_not_empty = True
                if right_child != None:
                    level_not_empty = True

                next_nodes.append(left_child)
                next_nodes.append(right_child)

        current_nodes = next_nodes

    while result and result[-1] == None:
        result.pop()
    return result


def _build_str(node):
    """Helper function used for pretty-printing."""
    if node == None:
        return 0, 0, 0, []

    line1 = []
    line2 = []
    val_len = gap_len = len(str(node.value))

    l_len, l_val_from, l_val_to, l_lines = _build_str(node.left)
    r_len, r_val_from, r_val_to, r_lines = _build_str(node.right)

    if l_len > 0:
        l_anchor = -int(-(l_val_from + l_val_to) / 2) + 1  # ceiling
        line1.append(' ' * (l_anchor + 1))
        line1.append('_' * (l_len - l_anchor))
        line2.append(' ' * l_anchor + '/')
        line2.append(' ' * (l_len - l_anchor))
        val_from = l_len + 1
        gap_len += 1
    else:
        val_from = 0

    line1.append(str(node.value))
    line2.append(' ' * val_len)

    if r_len > 0:
        r_anchor = int((r_val_from + r_val_to) / 2)  # floor
        line1.append('_' * r_anchor)
        line1.append(' ' * (r_len - r_anchor + 1))
        line2.append(' ' * r_anchor + '\\')
        line2.append(' ' * (r_len - r_anchor))
        gap_len += 1
    val_to = val_from + val_len - 1

    gap = ' ' * gap_len
    lines = [''.join(line1), ''.join(line2)]
    for i in range(max(len(l_lines), len(r_lines))):
        l_line = l_lines[i] if i < len(l_lines) else ' ' * l_len
        r_line = r_lines[i] if i < len(r_lines) else ' ' * r_len
        lines.append(l_line + gap + r_line)

    return len(lines[0]), val_from, val_to, lines


def _bst_insert(root, value):
    """Insert a node into the BST."""
    depth = 1
    node = root
    while True:
        if node.value > value:
            left_child = node.left
            if left_child == None:
                node.left = Node(value, node)
                break
            node = left_child
        else:
            right_child = node.right
            if right_child == None:
                node.right = Node(value, node)
                break
            node = right_child
        depth += 1
    return depth


def _validate_tree(root):
    """Check if the tree is malformed."""
    current_nodes = [root]

    while current_nodes:
        next_nodes = []
        for node in current_nodes:
            if isinstance(node, Node):
                if node.value == None:
                    raise ValueError('A node cannot have a null value')
                next_nodes.append(node.left)
                next_nodes.append(node.right)
            elif node != None:
                # Halt if the node is not NULL nor a node instance
                raise ValueError('Found an invalid node in the tree')
        current_nodes = next_nodes


def _generate_values(height, multiplier=1):
    """Generate and return a list of random node values."""
    if not isinstance(height, int) or height < 0:
        raise ValueError('Height must be a non-negative integer')
    count = 2 ** (height + 1) - 1
    return sample(range(count * multiplier), count)


def bst(height=4, values=None):
    """Generate a random binary search tree and return its root.

    :param height: the height of the tree (default: 4)
    :return: the root of the generated binary search tree
    """
    if values is None:
        values = _generate_values(height)
    root = Node(values[0])
    for index in range(1, len(values)):
        depth = _bst_insert(root, values[index])
        if depth == height:
            break
    return root


def stringify(bt):
    """Return the string representation of the binary tree.

    :param bt: the binary tree
    :return: the string representation
    """
    if bt == None:
        return ''
    elif isinstance(bt, list):
        if not bt:
            return ''
        bt = bst(height=999, values=bt)
    elif isinstance(bt, Node):
        _validate_tree(bt)
    else:
        raise ValueError('Expecting a list or a node')
    return '\n' + '\n'.join(_build_str(bt)[-1])


def convert(bt):
    """Convert a binary tree into a list, or vice versa.

    :param bt: the binary tree to convert
    :return: the converted form of the binary tree
    :raises ValueError: if an invalid tree is given
    """
    if bt == None:
        return []
    if isinstance(bt, list):
        return bst(height=999, values=bt)
    elif isinstance(bt, Node):
        _validate_tree(bt)
        return _build_list(bt)
    raise ValueError('Expecting a list or a node')

