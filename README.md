python-nginx
============

This is a simple reader/writer of nginx config files, for use in config
generation because string manipulation is so '90s.

It also works with Python 3!


Quickstart
----------

    import nginx

    # Note that this is poorly formatted, but still valid!
    config = """server { location / { try_files $request_uri index.html; }}"""

    data = nginx.loads(config)

    print(data)



TODO
----

* Dumping/writing nginx config.