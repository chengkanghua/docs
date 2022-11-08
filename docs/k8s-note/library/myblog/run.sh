#!/bin/bash
uwsgi --ini ./uwsgi.ini
nginx -c /etc/nginx/myblog.conf -g 'daemon off;'