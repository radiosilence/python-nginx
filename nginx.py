import copy
import json
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

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
}
server {
    listen 80;
    server_name %(name)s %(aliases)s;
    root        %(path)s/%(name)s/%(name)s/_wwwroot;
    access_log  %(path)s/%(name)s/access.log;
    autoindex   on;

    location ~* \.(jpg|jpeg|gif|css|png|js|ico)$ {
        access_log      off;
        expires         30d;
    }

    location / {
        try_files $uri /maintenance.html /index.html =404;
    }
}
"""

from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

def loads(string):
    def process_block(string):
        block_stack = []
        current_block = {}
        current_statement = []

        current_word = ''
        for char in string:
            if char == '{':
                block_stack.append(current_block)
                current_block = {}
                current_statement.append(current_word)
                current_word = ''
                if not 'name' in current_block:
                    current_block['name'] = {}
                current_block['name'] = ' '.join(current_statement)
                current_statement = []
            elif char == '}':
                inner = current_block
                current_block = block_stack.pop()
                name = inner['name']
                del inner['name']
                if not 'blocks' in inner:
                    inner['blocks'] = {}
                if not 'blocks' in current_block:
                    current_block['blocks'] = {}
                if not name in current_block['blocks']:
                    current_block['blocks'][name] = []
                current_block['blocks'][name].append(inner)
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

        # starts_special = current_word[0] in ('{',)
        # ends_special = current_word[-1] in ('}', ';')
        # if starts_special or ends_special:
        #     if starts_special:
        #         word = current_word[1:]
        #     if ends_special:
        #         word = current_word[:-1]
        #     if len(word) > 0:
        #         current_statement.append(word)
        #     if ends_special and len(current_statement) > 0:
        #         print (current_statement)
        #         key = current_statement[0]
        #         if not key in current_block['lines']:
        #             current_block['lines'][key] = []
        #         current_block['lines'][key].append(' '.join(current_statement[1:]))
        #         current_statement = []
        # else:
        #     current_statement.append(current_word)
        return current_block

    return process_block(string)

if __name__ == '__main__':
    #
    #print(yaml.dump(loads(EXAMPLE), default_flow_style=False, Dumper=Dumper))
    print(json.dumps(loads(EXAMPLE)))