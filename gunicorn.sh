#!/bin/sh
gunicorn --bind 0.0.0.0:5000 wsgi:app & gunicorn --certfile=server.crt --keyfile=server.key --bind 0.0.0.0:5000 wsgi:app