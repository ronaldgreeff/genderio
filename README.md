docker-compose exec web python manage.py create_db
docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
  hello_flask_dev=# \l
  hello_flask_dev=# \c hello_flask_dev
  hello_flask_dev=# select * from parents;
  hello_flask_dev=# \dt
  hello_flask_dev=# \q

docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py create_db
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml down -v

TODO:
Add back the removed requirements (tensorflow, etc.)
Nginx reverse proxy + flask redirects:
https://stackoverflow.com/questions/22312014/flask-redirecturl-for-error-with-gunricorn-nginx
https://blog.macuyiko.com/post/2016/fixing-flask-url_for-when-behind-mod_proxy.html
