import copy
import json

EXAMPLE = """server {
    listen 80;
    server_name %(name)s %(aliases)s;
    client_max_body_size 4G;
    keepalive_timeout 5;

    location / {
        try_files $uri @%(name)s;
    }

    location /media {
        alias %(path)s/%(name)s/%(name)s/media/;
        expires 1h;
    }

    location @%(name)s {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_set_header  X-Real-IP  $remote_addr;
        proxy_redirect off;
        proxy_buffering off;
        proxy_pass http://app_server_%(name)s;
    }
}"""

from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

def loads(string):
    def process_block(words):
        blocks = []
        block_stack = []
        block_template = {
            'lines': [],
            'name': [],
            'blocks': []
        }
        current_block = copy.deepcopy(block_template)
        append_block = False
        current_statement = []
        for word in words:
            word = word.replace('\n', '')
            current_word = ''
            for char in word:
                if char == '{':
                    block_stack.append(current_block)
                    current_block = copy.deepcopy(block_template)
                    current_block['name'] = current_statement
                    current_statement = []
                elif char == '}':
                    inner = current_block
                    current_block = block_stack.pop()
                    current_block['blocks'].append(inner)
                current_word += char

            if current_word[-1] in ['}', '{', ';']:
                word = current_word[:-1]
                if len(word) > 0:
                    current_statement.append(word)
                if len(current_statement) > 0:
                    current_block['lines'].append(current_statement)
                current_statement = []
            else:
                current_statement.append(current_word)
        return current_block

    words = filter(lambda x: len(x) > 0, string.split())

    return process_block(words)

if __name__ == '__main__':
    print(json.dumps(loads(EXAMPLE)))
