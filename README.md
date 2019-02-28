# Twitter Like Micro Blog

> Twitter like micro blogging site based on Django, Jquery, Ajax and Twitter Bootstrap.

## Hosted on Heruko

https://twitter-like-micro-blog.herokuapp.com/

## Todo

- [ ] Home page
- [ ] Feature to follow users
- [x] <b>Feature to like posts</b>
- [ ] SearchBar to search users and tags
- [x] <b>Detect tags from post</b>
- [x] <b>Tag page</b>
- [ ] User profile page
- [ ] Reset password
- [ ] Trending Tags section

## Development setup

Fork it and clone as local repository.

```sh
$ cd twitter-like-micro-blog
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```
