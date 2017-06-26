# Bundestag Agenda Scraper

Scraper to get Tagesordnungspunkte (agendas) from the German Bundestag.

## Setup
```bash
pip install -r requirements.txt
```

Change database configuration in `settings.py`
```
DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '32780',
    'username': 'postgres',
    'password': '',
    'database': ''
}
```

## Running

```bash
cd agendas
scrapy crawl agendaspider
```
This will add new table to the databse called `topics`