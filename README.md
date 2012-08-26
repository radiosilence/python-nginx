python-nginx
============

**WARNING: CURRENTLY ALPHA AS FUCK**

This is a simple reader/writer of nginx config files, for use in config
generation because string manipulation is so '90s.

Also has a handy query class for manipulating config.

Totally compatible with Python 3!


Quickstart
----------

    import nginx

    # Note that this is poorly formatted, but still valid!
    config = """server { server_name www.example.com; location / { try_files
        $request_uri index.html; }}"""

    root = nginx.loads(config)

    # Example, print server names and / locations for each server:
    for server in root.query('server'):
        print(server.query('server_name', first=True))
        for location in server.query('location', '/'):
            print(location)

    # Output:
    # server_name www.example.com;
    # location / {
    #     try_files $request_uri index.html;
    # }

    # Dump a config file.
    print(root)

    # Output:
    # server  {
    #     server_name www.example.com;
    #     location / {
    #         try_files $request_uri index.html;
    #     }
    # }

    # alternatively:
    print(root.dump(indent=1))

    # Output:
    #     server  {
    #         server_name www.example.com;
    #         location / {
    #             try_files $request_uri index.html;
    #         }
    #     }

TODO
----

* Much more to come on querying and manipulation of config.
* Support for retaining comments.
