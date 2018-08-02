# Report Exporting Service (RES)
## Description

This API is capable of reporting abstract reports in XML and PDF formats from a PostgreSQL database

## Install requirements

The requirements are stores as usual in the requirements file

```bash
pip3 install -r requirements.txt
```

## Export DB_PASSWORD and DB_USERNAME and PYTHONPATH

To be able to connect to the database you must export `DB_USERNAME` and `DB_PASSWORD`, also
export `PYTHONPATH` to the current git root to be able to find the packages.

``` bash
export DB_USERNAME=my_name
export DB_PASSWORD=my_secret
export PYTHONPATH=$(pwd)
```

## How to run

To run simply write

```bash
python3 runserver.py
```
