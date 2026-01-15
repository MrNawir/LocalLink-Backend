# LocalLink


## Setup (pyenv + pipenv)

1. Install Python 3.8.13 with pyenv (if not already installed):

```bash
pyenv install 3.8.13
pyenv local 3.8.13
```

2. Create the pipenv environment using that Python:

```bash
# example using an explicit pyenv python binary
~/.pyenv/versions/3.8.13/bin/python3.8 -m pipenv install --python ~/.pyenv/versions/3.8.13/bin/python3.8
```

3. Activate the shell and run the app:

```bash
pipenv shell
pipenv run python app.py
```

Alternatively run without spawning a shell:

```bash
pipenv run flask run --host=0.0.0.0 --port=5000
```

## Notes

- The project contains a `Pipfile` declaring `flask` and `.python-version` set to `3.8.13` for pyenv.
- To run with a production server: `pipenv run gunicorn -w 4 wsgi:app` (install `gunicorn` if needed).
