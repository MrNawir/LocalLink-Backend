# LocalLink Server

Here is how to get the backend up and running.

### 1. Install & Shell
Grab the dependencies and hop into the virtual environment:
```bash
pipenv install
pipenv shell
```

### 2. Setup Database
Run the migrations and seed it with some dummy data:
```bash
flask db upgrade
python seed.py
```

### 3. Run It
Start the server:
```bash
pipenv run python app.py
```

You should see it running on `http://localhost:5555`.