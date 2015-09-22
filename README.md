# Overview
This is a measly effort to provide an automatic web-API to Python functions that
are setup as workers using Celery. These workers can be dispatched from a web API.
In a nutshell, the first goal is to be able to make web-caclulators easy to setup
using python.

Security is of concern here. And this has to be addressed at various levels.

As no time has been spent thinking about licensing as of now, it defaults to GPL.

# Recommended setup
- Create a virtualenv for the project.
- pip install requirements.txt
- Start mongo
- Add the necessary json descriptor to the library that you want to export.
  json descriptor examples in function-json directory.
- Celerify python libraries. Use 'python manage.py filldb', this fills mongo
  with necessary symbols for the python lib, and also adds the necessary celery
  decorators to the python files.
- Start celery workers
- Start django
- Visit your webpage to see the python functions available.

#TODO

## Tests
- Add end to end tests. Use urllib to make a request to submit a job and match it
with python code. In long run, perhaps these can be added automatically?

## Security
- Timeout on the client can't be trusted?

## General
- Python3 compatibility
- Autostart celery workers
- Isolate requirements.txt of the project from guest code
- Automatically create a template of a json descriptor from python code.
- Automatically Celerify python code
- Provide HTML5 decoration with JSON?
- Javascript validate fields
- Fix the URLs to API?
- Previous results computed View (using d3?)
- Don't re-compute previously computed results (LRU_Cache?)
- Be able to pull a python project from github and celerify it?
