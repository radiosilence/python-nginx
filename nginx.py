import copy

def loads(string):
    def process_block(string):
        stack = []
        current_block = {}
        current_statement = []

        current_word = ''
        for char in string:
            if char == '{':
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
                if len(current_word) > 0:
                    current_statement.append(current_word)
                    current_word = ''
            else:
                current_word += char

        return current_block

    return process_block(string)
