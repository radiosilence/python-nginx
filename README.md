python-nginx
============

**WARNING: CURRENTLY ALPHA AS FUCK**

This is a simple reader/writer of nginx config files, for use in config
generation because string manipulation is so '90s.

Also has a handy query class for manipulating config.

It also works with Python 3!


Quickstart
----------

    import nginx

    # Note that this is poorly formatted, but still valid!
    config = """server { location / { try_files $request_uri index.html; }}"""

    root = nginx.loads(config)

    # Example, print server names and / locations for each server:
    for server in root.query('server'):
        print(server.query('server_name', first=True))
        for location in server.query('location', '/'):
            print(location)

    # Dump a config file.
    print(root)
    # alternatively:
    print(root.dump(indent=1))


TODO
----

* Much more to come on querying and manipulation of config.
* Support for retaining comments.
