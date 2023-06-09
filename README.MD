# How to start REST API

## I. macOS
1. Create a Python virtual environment (venv)

```
pip install virtualenv
python -m venv venv
```

2. Start virtual environment 

```
source venv/bin/activate
```

## II. Windows

### A. Initialization

1. Create a Python virtual environment (venv)
```
pip install virtualenv
python -m venv venv
```

2. Activate python vevn & install packages/libraries required
```
venv\Scripts\activate
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


## III. Addtionals:

View SQLite Database:

```
sqlite3 app.db
```

To view database schema for all tables (in sqlite CLI):

```
.schema
```

To view schema for specific table:

```
.schema TABLE_NAME
```
