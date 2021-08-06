# appointment_maker
## Setup

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```


Once `pip` has finished downloading the dependencies:
If Debug = True
```sh
(env)$ cd project
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate

(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000`.
