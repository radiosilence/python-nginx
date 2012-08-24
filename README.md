python-nginx
============

Simple reader/writer of nginx config files, for use in config generation.

Python 3 compatible.


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