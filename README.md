# Tato

Tato is just another URL shortner, built with Flask and capable of having user accounts. By generating URLs like Gfycat, this URL shortner might not shorten URLs at all!

## Set up a development environment

* Install dependencies
```bash
$ pip3 install -r requirements.txt
```

* Prepare environment
```bash
$ export FLASK_APP=shortner
$ export FLASK_DEBUG=1
```

* Create database
In an interactive python shell
```python
from shortner import db, create_app
db.create_all(app=create_app())
exit()
```

* Run the app
```bash
$ flask run
```