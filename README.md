# Instagender
## *AI powered gender prediction*

#### Video Demo:  [URL HERE](https://www.youtube.com/)
#### Description:
> Instagender is a web application that generates gender predictions using a neural network.

### Overview
#### Built using:
| Component | Function  |
|-|-|
| flask | Application framework |
| keras | Neural network model |
| postgres | Database |
| gunicorn | WSGI HTTP Server |
| nginx | Reverse Proxy |
| docker | Virtualisation engine |

The was application was built using Docker; separating it from underlying infrastructure. Docker facilitates easy deployment to a variety of environments without having to reconfigure the application each time.

Using the docker-compose commands below, two services are spun up - `nginx`, a high performance, production class load-balancer and web server, and `web` - the application built using flask.

Uploaded data is persisted using **media** and **originals** (along with static) docker volumes. A major benefit of volumes is that ability to easily back them up (along with the database container).

#### The Application's Structure
The application is built using three modules:
- ##### auth
Auth uses `flask-login` to take care of some of the boilerplate for user registration and login. I've extended the module to include email confirmation, confirmation resend and password reset. Flask-login includes a very useful `current_user` hook used throughout the project.

- ##### main
The primary application consists of a dashboard that allows the user to manage their babies. It takes into account that users may have existing children and that unborn babies may not yet be given a name. Users can upload image formats specified in `config.py`.

Since the model was trained on `jpg` images (because that was the bulk of what I had available), so predictions can currently only be done for `jpg` images. In reality I expect most images to be uploaded to be `png` and in future I'd like to explore using this format or a mix of formats (with appropriate pre-processing). I therefore store both original upload under `project.originals` and a `jpg` copy of it under `project.media`.

I use nginx to efficiently serve media (and static) files, as specified in the `nginx.conf` file. The `originals` folder is inaccessible to users while `media` requires a user to be logged in. I generate a unique ID for filenames to reduce the likelihood of a user accessing another user's baby's images. The logic for image conversion and generating a unique filename is stored under `project.helpers.utils`.

I noticed that I could significantly increase accuracy of my prediction by cropping out anything that isn't part of the baby's anatomy. Rather than cropping several thousand images by hand (again :expressionless:), I ask the user to do so upon upload, using [cropper.js](https://fengyuanchen.github.io/cropperjs/) within a bootstrap modal. Once the image is cropped, it's uploaded via Ajax, stored/converted, and the URL of the `jpg` is returned and inserted into the `src` attribute of the input that was originally clicked.

Users are able to delete babies from their dashboard. However, the data is not truly deleted. Instead, it is flagged as deleted and excluded from the dashboard on that basis. This makes is possible to review the data before retraining the model in future and deciding whether or not to keep it in.


- ##### prediction
The trained neural net is stored within `prediction.models` along with the pipeline, `prediction.tl2_final.py`. When a user requests a prediction on a baby, the application retrieves the images for that particular baby, pre-processes each one before passing them through the model, and calculates a single prediction for the image set.

Users are encouraged to upload scans for previous children if possible. If they do, they are given the chance to predict and confirm the prediction via the dashboard (`main.views.confirm_gender`). If however the baby's due date is in future, the user will receive an email 1 week after the due date asking whether or not the prediction was accurate (`prediction.views.confirm_outcome`). The latter tokenises the `baby_id` and `parent.email` values into a URL which is combined with a query parameter (`?oc=True` or `oc=False`) in `templates.email_confirm.html` and sent to the user using the CLI commands below.

- ###### The convolutional neural net
I experimented with several iterations of networks, learning rates, batch sizes and pre-trained models (for transfer learning - including VGG16, mobilenet and Xception, as well as building two of my own) and typically ended up with similar results/accuracy. Data cleansing was the most time consuming aspect of it all. The data I managed to obtain included corrupt images with termination error. To address this issue, I opened each image in the `Pillow` module, and re-saved them. I then copied the data to a new folder and progressively cleaned them as follows:

| Folder Name | Progress |
|-|-|
|raw| Corruptions fixed using Pillow |
|0| None ultrasounds, reformatted duplicates or obvious duplicates, 4D ultrasound, any too unfocussed - all removed|
|1| Merged into gender folders with any multi-set ultrasounds placed into separate folders.|
|2| All images Cropped to a minimum|
|3| Poor quality images removed|
|4| All images copped to only include anatomic features|

- ##### Additional

Within the `web` root, a `manage.py` file is included with the following cli commands:
- `create_db()`: drop and re-create the database
- `seed_db()`: seed the database with the first (admin) user
- `scheduled()`: run scheduled email follow ups to confirm gender

This allows me to run the defined commands from the host machine using the docker `exec` command (see below). The `scheduled()` command can be run regularly by defining a cron job to do so.

- ##### Misc

All `static/img` are `.svg` so that they scale crisply on any device. They're also all original pieces of artwork :blush:

#### future plans
- [ ] testing
- [ ] further refine dataset - remove poor quality images, crop remaining closer to target
- [ ] normalise images using scikit image library
- [ ] real-time model improvement
- [ ] add in adwords if traffic grows


#### shoutouts
- Excellent guide for setting up a basic docker, nginx, gunicorn, flask application with CLI commands
  https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
- Excellent explanation why CLI commands + cron jobs are better for scheduling regular tasks (than implementing a solution within the app itself)
  https://blog.miguelgrinberg.com/post/run-your-flask-regularly-scheduled-jobs-with-cron#commentform
- Good starting guide for building a flask-keras application
  https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html
- Great guide for what to do if you're data poor
  https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html

#### useful commands

##### general
```
docker exec -it <container name> bash
docker kill <container name>
```

##### development

```
docker-compose up -d --build
docker-compose exec web python manage.py create_db
docker-compose exec web python manage.py seed_db

docker-compose logs -f
docker-compose down -v

docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
  hello_flask_dev=# \l
  hello_flask_dev=# \c hello_flask_dev
  hello_flask_dev=# select * from parents;
  hello_flask_dev=# \dt
  hello_flask_dev=# \q
```

##### production

```
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py create_db
docker-compose -f docker-compose.prod.yml exec web python manage.py seed_db
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml down -v

docker-compose exec db psql --username=hello_flask --dbname=hello_flask_prod
 hello_flask_prod=# \l
 hello_flask_prod=# \c hello_flask_dev
 hello_flask_prod=# select * from parents;
 hello_flask_prod=# \dt
 hello_flask_prod=# \q
```
