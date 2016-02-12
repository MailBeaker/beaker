Beaker
============

----------------------------------------------
Requirements
----------------------------------------------

1. sudo apt-get install python-dev python-pip libpq-dev git
2. sudo pip -r requirements.txt

----------------------------------------------
Operation
----------------------------------------------
If you are doing local development work, copy the settingslocal tempate:
```
cp settingslocal.py.dev settingslocal.py
```

Now we need to stage static resources:
```
python manage.py collectstatic
```

Then set up a local SQLite DB:
```
python manage.py syncdb
```

Now we run the local dev server:
```
python manage.py runserver 5000
```


----------------------------------------------
Configuration
----------------------------------------------

Production settings are stored in the settings.py file.  For development work, please create a settingslocal.py file, which will be ignored by Git.
