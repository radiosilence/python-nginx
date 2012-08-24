import copy

def loads(string):
    """Loads a nginx config file into memory as a dict."""
    stack = []
    current_block = {}
    current_statement = []
    current_word = ''

    for char in string:
        if char == '{':
            """Put the current block on the stack, start a new block.
            Also, if we are in a word, "finish" that off, and end the current
            statement."""
            stack.append(current_block)
            current_block = {}
            if len(current_word) > 0:
                current_statement.append(current_word)
                current_word = ''
            if not 'name' in current_block:
                current_block['name'] = {}
            current_block['name'] = current_statement
            current_statement = []
        elif char == '}':
            """Finalize the current block, pull the previous (outer) block off
            of the stack, and add the inner block to the previous block's dict
            of blocks."""
            inner = current_block
            current_block = stack.pop()
            name = inner['name']
            del inner['name']
            if not 'blocks' in current_block:
                current_block['blocks'] = {}
            key = name[0]
            if len(name) > 1:
                inner['args'] = name[1:]
            if not key in current_block['blocks']:
                current_block['blocks'][key] = []
            current_block['blocks'][key].append(inner)
        elif char == ';':
            """End the current word and statement."""
            current_statement.append(current_word)
            current_word = ''
            if len(current_statement) > 0:
                key = current_statement[0]
                if not 'lines' in current_block:
                    current_block['lines'] = {}
                if not key in current_block['lines']:
                    current_block['lines'][key] = []
                current_block['lines'][key].append(' '.join(current_statement[1:]))
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
