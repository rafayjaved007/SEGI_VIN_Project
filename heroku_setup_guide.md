- install pipenv outside copied project folder
- create heroku account
- Download and install Heroku Command Line Interface(CLI) from heroku's website
- Run command 'heroku login' and login to your heroku account
- Create Procfile in project folder and paste 'web: gunicorn myproject.wsgi' in it with your project name
- Run 'pip install gunicorn' command
- Run 'pip install django-heroku' command
- Run 'pip freeze > requirements.txt' command
- Add the following import statement to the top of settings.py:
    `import django_heroku`
- Then add the following to the bottom of settings.py:
    `django_heroku.settings(locals())`
- Create heroku app with 'heroku create segi-vin'
- Run following commands to push code:
```
git init
git add .
heroku git:remote -a segi-vin
git commit -m "message"
git push heroku master
``` 

## Useful Commands:
1. `brew install heroku/brew/heroku`
2. `heroku login`
3. `heroku create <project_name>`
4. `git push heroku HEAD:main`
5. `heroku ps:scale web=1`
6. `heroku open`

- `heroku config:set DISABLE_COLLECTSTATIC=0`
- `heroku logs --tail`
- `heroku run python manage.py shell`
- `heroku run bash`
- `python manage.py dumpdata core > data.json`
