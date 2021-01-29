$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml logs -f
$ docker-compose -f docker-compose.prod.yml down -v

TODO:
Add back the removed requirements (tensorflow, etc.)
Nginx reverse proxy + flask redirects:
https://stackoverflow.com/questions/22312014/flask-redirecturl-for-error-with-gunricorn-nginx
https://blog.macuyiko.com/post/2016/fixing-flask-url_for-when-behind-mod_proxy.html
