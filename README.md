# Insta-gender
## Neural network powered gender prediction
#### Video Demo:  <URL HERE>
#### Description:
web app that allows users to upload and crop baby scans before performing a prediction on the gender using a neural network model built with keras.

built with:
flask
keras
postgres
gunicorn
nginx
docker

env variable files for development and production

app consists of
auth:
main:
prediction:
manage.py file with cli commands:
re-creating the database
seeding the database
running scheduled email follow ups

shoutouts
https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
https://blog.miguelgrinberg.com/post/run-your-flask-regularly-scheduled-jobs-with-cron#commentform
https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html
https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html

useful commands

docker-compose exec web python manage.py create_db
docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
  hello_flask_dev=# \l
  hello_flask_dev=# \c hello_flask_dev
  hello_flask_dev=# select * from parents;
  hello_flask_dev=# \dt
  hello_flask_dev=# \q
  update parents set confirmed = 't' where id = 1;

docker-compose -f docker-compose.prod.yml up -d --build
winpty docker-compose -f docker-compose.prod.yml exec web python manage.py test
winpty docker-compose -f docker-compose.prod.yml exec web python manage.py create_db
winpty docker-compose -f docker-compose.prod.yml exec web python manage.py seed_db
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml down -v

docker exec -it <container name> bash
docker kill <container name>

winpty docker-compose exec db psql --username=hello_flask --dbname=hello_flask_prod
