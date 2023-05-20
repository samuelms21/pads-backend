# How to start REST API

## macOS
1. Create a Python virtual environment (venv)

```
pip install virtualenv
python -m venv venv
```

2. Start virtual environment (macOS & Windows)
   a. MacOS

```
source venv/bin/activate
```

## Windows

### A. Initialization

1. Create a Python virtual environment (venv)

```
pip install virtualenv
python -m venv venv
```

2. Install all packages/libraries required
```
pip install -r requirements.txt
```


### B. Run

1. Activate python venv
```
venv\Scripts\activate
```

2. Start REST API
```
python rest_api.py
```


## Addtionals:

View SQLite Database:

```
sqlite3 app.db
```
