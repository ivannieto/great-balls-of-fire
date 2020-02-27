# Great Balls Of Fire

Demo data visualizations made with Dash by Plot.ly for Python Vigo group 'lightning talks' held on July 20th 2017.

How to run this project locally:

```Bash
git clone git@bitbucket.org:inieto/great-balls-of-fire.git
cd great-balls-of-fire
```

```Bash
python3 -m venv .venv
source .venv/bin/activate
```

### Update main tools

```Bash
pip install --upgrade pip setuptools wheel pip-tools
```

### Instal requirements

```Bash
pip install -r requirements.txt
```

### Export your Google Geocoding API Key - [[Get a key]](https://developers.google.com/maps/documentation/geocoding/intro?hl=es-419)
```Bash
export GOOGLE_API_KEY='AIzaSyAgMa15p1oCEzUDs0MFQ2WgNiI6OQWQsjh'
```

### Run the project

```Bash
python src/app
```

Open [http://localhost:9000/](http://localhost:9000/)

Project is deployed live on Heroku.

[https://great-balls-of-fire.herokuapp.com](https://great-balls-of-fire.herokuapp.com)