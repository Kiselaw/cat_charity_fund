## QRkot

QRKot is an app where users can make donations to the fund that distributes them between social projects. 

### Overview

In general, the project is exactly an API based on FastAPI.

Any user can view the entire list of current fund projects. Authenticated people can make donations, moreover, they can also view the list of already made donations.

An important feature is that funds flow into a common "boiler", from where they are automatically distributed among projects depending on the date of their creation.

### Technologies

- Python 3.9.5
- FastAPI

### Installation and launch

Clone the repository and go to it using the command line:

```bash
git clone 
```

```bash
cd cat_charity_project
```

Create and activate a virtual environment:

Windows:

```bash
py -3 -m venv env
```

```bash
. venv/Scripts/activate 
```

```bash
py -m pip install --upgrade pip
```

macOS/Linux:

```bash
python3 -m venv .venv
```

```bash
source env/bin/activate
```

```bash
python3 -m pip install --upgrade pip
```

Install dependencies from a file requirements.txt:

```bash
pip install -r requirements.txt
```

Make migrations:

```bash
alembic upgrade head
```

Launch:

```bash
uvicorn app.main:app --reload
```

### License

MIT