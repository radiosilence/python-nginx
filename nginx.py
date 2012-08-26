import copy

class Node(object):
    def __init__(self, directive=None, args=None, children=None, root=False):
        if not directive and not root:
            raise Exception('If not root node, directive must be set.')
        if directive and root:
            raise Exception('Directive must not be set for root node.')
        self.directive = directive
        self.root = root
        if not args:
            args = []
        self.args = args
        if not children:
            children = []
        self.children = children

    def __repr__(self):
        if len(self.args) > 0:
            args = ' ' + ' '.join(self.args)
        else:
            args = ''
        return '<Node: {}{}>'.format(
            self.directive,
            args
        )

    def dump(self, indent=0):
        def get_children(_indent):
            return '\n'.join(
                [child.dump(_indent) for child in self.children]
            )
        spaces = indent * '    '
        if self.children:
            if self.root:
                return get_children(indent)
            else:
                return '{0}{1} {2} {{\n{3}\n{0}}}'.format(
                    spaces,
                    self.directive,
                    ' '.join(self.args),
                    get_children(indent + 1)
                )
        else:
            return '{}{} {};'.format(
                spaces,
                self.directive,
                ' '.join(self.args))

    def __str__(self):
        return self.dump(indent=0)


def loads(string):
    """Loads a nginx config file into memory as a dict."""
    stack = []
    current_block = Node(root=True)
    current_statement = []
    current_word = ''

    for char in string:
        if char == '{':
            """Put the current block on the stack, start a new block.
            Also, if we are in a word, "finish" that off, and end the current
            statement."""
            stack.append(current_block)
            if len(current_word) > 0:
                current_statement.append(current_word)
                current_word = ''
            current_block = Node(
                current_statement[0],
                args=current_statement[1:]
            )
            current_statement = []
        elif char == '}':
            """Finalize the current block, pull the previous (outer) block off
            of the stack, and add the inner block to the previous block's dict
            of blocks."""
            inner = current_block
            current_block = stack.pop()
            directive = current_block.directive
            current_block.children.append(inner)
        elif char == ';':
            """End the current word and statement."""
            current_statement.append(current_word)
            current_word = ''
            if len(current_statement) > 0:
                key = current_statement[0]
                current_block.children.append(Node(
                        current_statement[0],
                        args=current_statement[1:]
                ))
            current_statement = []
        elif char in ['\n', ' ', '\t']:
            """End the current word."""
            if len(current_word) > 0:
                current_statement.append(current_word)
                current_word = ''
        else:
            """Add current character onto current word."""
            current_word += char

    return current_block

def dumps(node):
    return node.dump()