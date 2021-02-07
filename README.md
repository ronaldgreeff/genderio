# Instagender
## *AI powered ultrasound gender prediction* :baby:

#### Video Demo: [Click Here](https://youtu.be/DPfss9Alqtc)
&nbsp;
#### Description:
Instagender is a web application that predicts the gender of a baby from ultrasound images using a convolutional neural network.
&nbsp;
#### Background
I've developed this app as my final project for Harvard's CS50x course - building something of interest to me, that solves an actual problem and outlives the course. We've recently had a baby and my wife, wanting to be sure of the gender of the baby at 12 weeks, gave me the idea to build a gender prediction application. I hope to improve some aspects of the application and have used Docker specifically for the purposes of expansion and maintenance.

# Overview
## Built using
| Component | Function  |
|-|-|
| flask | Application framework |
| keras | Neural network model |
| postgres | Database |
| gunicorn | WSGI HTTP Server |
| nginx | Reverse Proxy |
| docker | Virtualisation engine |

&nbsp;
### Environment - Docker

The application was built using Docker so that I can separate the application and underlying infrastructure. This allows the application to be developed locally and deployed anywhere that supports Docker without having to reconfigure the application and environment each time.

Using the docker-compose command, two Docker `services` are spun up

- **`nginx`**, a high performance, production class load-balancer and web server.

- **`web`**, the Flask application (using Gunicorn as the WSGI server when run in production).

Four Docker volumes are defined in `docker-compose.prod.yml` and mounted to the container:

- **`postgres_data`**

- **`static_volume`**

- **`media_volume`**

- **`originals_volume`**

These allow data to be persisted if the `web` container is taken down. Volumes can also be easily backed-up.

&nbsp;
#### Useful Docker commands
To start, make sure you've changed the `env` files in the root directory to `.env`.

&nbsp;
##### General
```
# list active containers. Add -a flag to list all containers
docker ps

# enter a container using a bash terminal
docker exec -it <container name> bash

# kill a container if it crashes
docker kill <container name>
```
&nbsp;
##### Development
URL: 127.0.0.1:5000
```
# build and run the containers, in the background (-d)
docker-compose up -d --build

# view logs of the running containers
docker-compose logs -f

# bring the containers down, and destroy the volumes (-v)
docker-compose down -v

# execute the CLI commands specified in manage.py
docker-compose exec web python manage.py create_db
docker-compose exec web python manage.py seed_db

# you can access the postgres database using the defaults values specified in the env.db file
docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
  hello_flask_dev=# \l
  hello_flask_dev=# \c hello_flask_dev
  hello_flask_dev=# select * from parents;
  hello_flask_dev=# \dt
  hello_flask_dev=# \q
```
&nbsp;
##### Production
URL: 127.0.0.1:1337
```
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml exec web python manage.py create_db
docker-compose -f docker-compose.prod.yml exec web python manage.py seed_db

docker-compose exec db psql --username=hello_flask --dbname=hello_flask_prod
 hello_flask_prod=# \l
 hello_flask_prod=# \c hello_flask_dev
 hello_flask_prod=# select * from parents;
 hello_flask_prod=# \dt
 hello_flask_prod=# \q
```
&nbsp;
### Application - Flask
The application is built using three modules:
All views have appropriate flashed messages, but are easily found in the code so not mentioned detailed below.
&nbsp;
#### Auth
Auth partly uses `flask-login` to take care of some of the boilerplate for user registration and login. I've extended the module to include email confirmation, resending confirmations and resetting user's password. Flask-login includes a very useful `current_user` hook used throughout the project.
&nbsp;
##### *auth.tokenizers*
Auth tokens rely on `URLSafeTimedSerializer` to set time limit on token.

- **`generate_confirmation_token(email)`**
Generates confirmation token using user's email address, and `SECRET_KEY` and `SECURITY_PASSWORD_SALT` env variables.
&nbsp;
- **`confirm_email_token(token, expiration=3600)`**
1 hour window. Returns False if BadData or BadSignature, else returns user's de-serialized email address

&nbsp;
##### *auth.views*

- **`signup()` `/signup`**
  `GET`: Return sign-up form.
  `POST`: Validate sign-up form. Check if email address already used. If not, create the user (password is set using `set_password` method on `User` model, hashed using the `sha256` algorithm). Then tokenize user's email and generate url to `auth.confirm_email`, an send using the `email_confirm` template.
  *Redirect to `main.dashboard`.*
&nbsp;
- **`signin()` `/signin`**
  `GET`: Redirect user if already authenticated, else return sign-in form.
  `POST`: Validate sign-in form. If credentials correct, *redirect to `main.dashboard`, else* *redirect to `auth.signin`.*
&nbsp;
- **`unconfirmed()` `/unconfirmed`**
  `GET`: simply renders unconfirmed template.
&nbsp;
- **`confirm_email(token)` `/confirm/<token>`**
  `GET`: Validate token. If valid token, confirm user.
  *Redirect to `main.dashboard`.*
&nbsp;
- **`resend_confirmation()` `/resend`**
  *Requires user to be logged in.*
  `GET`: Tokenises `current_user`'s email and emails `email_confirm` template.
  *Redirect to `auth.unconfirmed`.*
&nbsp;
- **`logout()` `/logout`**
  `GET`: Executes `flask_login.logout_user()`.
  *Redirect to `main.index` (which redirects to `auth.signin` if not signed in).*
&nbsp;
- **`reset()` `/reset`**
  `GET`: Return email address form.
  `POST`: If valid email, tokenize email and generate url to `auth.confirm_reset`, then send using `email_reset` template.
  *Redirect to `auth.signin`.*
&nbsp;
- **`confirm_reset(token)` `/reset/<token>`**
  `GET`: Validate token. If valid token, return password reset form.
  `POST`: Validate reset form.
  *Redirect to `auth.signin`.*

&nbsp;
#### Main
The primary application consists of a dashboard that allows the user to manage their babies. It takes into account that users may have existing children and that unborn babies may not yet be given a name. Users can upload image formats specified in `config.py`.

Since the model was trained on `jpg` images (because that was the bulk of what I had available), so predictions can currently only be done for `jpg` images. In reality I expect most images to be uploaded to be `png` and in future I'd like to explore using this format or a mix of formats (with appropriate pre-processing). I therefore store both original upload under `project.originals` and a `jpg` copy of it under `project.media`.

I use nginx to efficiently serve media (and static) files, as specified in the `nginx.conf` file. The `originals` folder is inaccessible to users while `media` requires a user to be logged in. I generate a unique ID for filenames to reduce the likelihood of a user accessing another user's baby's images. The logic for image conversion and generating a unique filename is stored under `project.helpers.utils`.

I noticed that I could significantly increase accuracy of my prediction by cropping out anything that isn't part of the baby's anatomy. Rather than cropping several thousand images by hand (again :expressionless:), I ask the user to do so upon upload, using [cropper.js](https://fengyuanchen.github.io/cropperjs/) within a bootstrap modal. Once the image is cropped, it's uploaded via Ajax, stored/converted, and the URL of the `jpg` is returned and inserted into the `src` attribute of the input that was originally clicked.

Users are able to delete babies from their dashboard. However, the data is not truly deleted. Instead, it is flagged as deleted and excluded from the dashboard on that basis. This makes is possible to review the data before retraining the model in future and deciding whether or not to keep it in.

`dashboard` only accepts `GET` request and `make_baby` `POST` - they're separated so that user can refresh page without re-submitting the new baby form if they hit refresh after a baby was added.

&nbsp;
##### *main.views*

- **`index()` `/`**
  `GET`: return `welcome` template.
&nbsp;
- **`dashboard()` `/dashboard`**
  *Requires user to be logged in.*
  `GET`: if user uncofirmed, *redirect to `auth.unconfirmed`, else retrieve babies for* `current_user`. If no babies, flash message on how to get started. Returns new baby form along with any babies with the attribute `deleted == False`. An update baby form is returned for each baby.
&nbsp;
- **`make_baby()` `/make_baby`**
  *Requires user to be logged in.*
  `POST`: validated new baby form and creates a baby if valid.
  *Redirect to `main.dashboard`.*
&nbsp;
- **`update_baby()` `/update_baby`**
  *Requires user to be logged in.*
  `POST`: validate update baby form. Checks baby exists and belongs to the `current_user`. If `update` button pressed, baby's details are updated. If `delete` button pressed, attribute `deleted == True` is set.
&nbsp;
- **`confirm_gender()` `/confirm_gender`**
  *Requires user to be logged in.*
  `POST`: validate gender confirmation form. Checks baby exists and belongs to the `current_user`. If "right" (correct prediction outcome) is clicked, the `Baby` model's `gender` attribute is set to the value of `predicted_gender`. If "wrong" is clicked, the `gender` attribute is reversed using a dictionary.
  *Redirect to `main.dashboard`.*
&nbsp;
- **`upload_img()` `/upload_img`**
  *Requires user to be logged in.*
  `POST`: Checks baby exists and belongs to the `current_user`. If valid, generates unique filename for image. Original upload stored in `project/originals` and a jpg conversion stored in `project/media`. Filepath to media is stored in the database and then also returned to the front-end as `JSON`, where it is inserted into the `src` attribute of the image placeholder. If successful, the front-end triggers a page refresh.

&nbsp;
#### Prediction
The trained neural net is stored within `prediction.models` along with the pipeline, `prediction.tl2_final.py`. When a user requests a prediction on a baby, the application retrieves the images for that particular baby, pre-processes each one before passing them through the model, and calculates a single prediction for the image set.

Users are encouraged to upload scans for previous children if possible. If they do, they are given the chance to predict and confirm the prediction via the dashboard (`main.views.confirm_gender`). If however the baby's due date is in future, the user will receive an email 1 week after the due date asking whether or not the prediction was accurate (`prediction.views.confirm_outcome`). The latter tokenises the `baby_id` and `parent.email` values into a URL which is combined with a query parameter (`?oc=True` or `oc=False`) in `templates.email_confirm.html` and sent to the user using the CLI commands below.
&nbsp;
##### *prediction.tokenizers*
Auth tokens rely on `URLSafeSerializer`.

- **`generate_outcome_token(parent_email, baby_id)`**
Generates confirmation token using a dictionary comprised of a user's email address and the baby's id, along with `SECRET_KEY` env variable.
***Note:*** This is called from `manage.py` using the `scheduled` CLI command.
&nbsp;
- **`deserialize_outcome_token(token)`**
Returns False if BadData or BadSignature, else returns user's de-serialized dictionary of user's email address and baby id.
&nbsp;
##### *prediction.views*

- **`predict_gender(baby)`**
  Function used to collect all of a baby instance's images, pre-process them (convert them to grayscale and resize to 128 x 128 pixels), generating a prediction per image and calculating an overall prediction outcome.
&nbsp;
- **`predict()` `/predict`**
  *Requires user to be logged in.*
  `POST`: Checks baby exists and belongs to the `current_user`. If valid, `predict_gender` is called. The outcome is set against the baby model instance's `predicted_gender` outcome.
  *Redirect to `main.dashboard`.*
&nbsp;
- **`confirm_outcome(token)` `/outcome/<token>`**
  `GET`: If `token` and URL query args (`?oc=True` or `?oc=False`), validate token. If token valid, set `gender` attribute relative to `predicted_gender` - if query arg is `True`, set it to same value as `predicted`, otherwise reverse the gender with a simple dictionary.
&nbsp;
##### *The convolutional neural net*
I experimented with several iterations of networks, learning rates, batch sizes and pre-trained models (for transfer learning - including VGG16, mobilenet and Xception models, as well as building two of my own) and typically ended up with similar results/accuracy. The trained model and it's headers are stored in `prediction/models`.
&nbsp;
###### Notable points
- `class_mode` is set to binary, since there are binary outputs.
- As such the output of the model is a *single* node using `sigmoid` activation function.
- The loss function uses `binary_crossentropy` and `BinaryAccuracy` metrics.
- Since colour doesn't matter (and actually decreased accuracy), I convert the images to grayscale. This changes the input shape to have 1 channel instead of 3.
&nbsp;
###### Challenges
Data cleansing was the most time consuming aspect of it all. The data I managed to obtain included corrupt images with termination error. To address this issue, I opened each image in the `Pillow` module, and re-saved them. I then copied the data to a new folder and progressively cleaned them as follows:

| Folder Name | Progress |
|-|-|
|raw| Full dataset with corruptions fixed using the `Pillow` library |
|0| None ultrasounds, reformatted duplicates or obvious duplicates, 4D ultrasound, any too unfocussed - all removed|
|1| Merged into gender folders with any multi-set ultrasounds placed into separate folders.|
|2| All images Cropped to a minimum|
|3| Poor quality images removed|
|4| All images cropped to only include anatomic features|

&nbsp;
#### Additional

Within the `web` root, a `manage.py` file is included with the following cli commands:

- **`create_db()`**
  drop and re-create the database
&nbsp;
- **`seed_db()`**
  seed the database with the first (admin) user
&nbsp;
- **`scheduled()`**
  run scheduled email follow ups to confirm gender

This allows me to run the defined commands from the host machine using the docker `exec` command (see below). The `scheduled()` command can be run regularly by defining a cron job to do so.

&nbsp;
#### Misc
I noticed from the dataset that there were a significant number of photos taken of scans that were either too close, too far or obscured by the camera flash. To try and address this, I have tried to explain to the user how to take a good picture at various points (the welcome page and during image upload).

I decided to create all the images (in `static/img`) as `.svg` so that they scale crisply on any device.

&nbsp;
#### Future Plans
- [ ] Write tests
- [ ] Add database migration support
- [ ] Further refine the dataset / increase accuracy of model
- [ ] Normalise images using sci-kit image library
- [ ] Add real-time model improvement

&nbsp;
#### Shout-outs
- Excellent guide for setting up a basic docker, nginx, gunicorn, flask application
  https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
- Excellent explanation why CLI commands + cron jobs are better for scheduling regular tasks (than implementing a solution within the app itself)
  https://blog.miguelgrinberg.com/post/run-your-flask-regularly-scheduled-jobs-with-cron#commentform
- Good starting guide for building a flask-keras application
  https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html
- Great guide for what to do if you're data poor
  https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html
