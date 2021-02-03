# Insta-gender
## *AI powered gender prediction*

#### Video Demo:  [URL HERE](https://www.youtube.com/)
#### Description:
> web app that generates gender predictions using neural network.

#### Built using:
- flask
- keras
- postgres
- gunicorn
- nginx
- docker

#### app consists of
**auth**: user registration, login, password management, token generation and `current_user` hooks
**main**: user dashboard for creating babies, uploading and cropping their scans, and gaining a prediction
**prediction**: retrieves uploaded images for given `baby_id`, pre-processes them and generates a gender prediction

`manage.py` file with cli commands:
- re-creating the database
- seeding the database
- running scheduled email follow ups (using cron jobs)

`env` variable files for development and production environments


#### future plans
- [ ] testing
- [ ] further refine dataset - remove poor quality images, crop remaining closer to target
- [ ] normalise images using scikit image library
- [ ] real-time model improvement
- [ ] add in adwords if traffic grows


#### shoutouts
https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
https://blog.miguelgrinberg.com/post/run-your-flask-regularly-scheduled-jobs-with-cron#commentform
https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html
https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html

#### useful commands

###### development

docker-compose up -d --build
docker-compose exec web python manage.py create_db
docker-compose exec web python manage.py seed_db
docker-compose logs -f
docker-compose down -v

docker exec -it <container name> bash
docker kill <container name>

docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
  hello_flask_dev=# \l
  hello_flask_dev=# \c hello_flask_dev
  hello_flask_dev=# select * from parents;
  hello_flask_dev=# \dt
  hello_flask_dev=# \q

###### production

docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py create_db
docker-compose -f docker-compose.prod.yml exec web python manage.py seed_db
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml down -v

winpty docker-compose exec db psql --username=hello_flask --dbname=hello_flask_prod
hello_flask_prod=# \l
hello_flask_prod=# \c hello_flask_dev
hello_flask_prod=# select * from parents;
hello_flask_prod=# \dt
hello_flask_prod=# \q
