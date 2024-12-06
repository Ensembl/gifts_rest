[![Build Status](https://travis-ci.org/Ensembl/gifts_rest.svg?branch=master)](https://travis-ci.org/Ensembl/gifts_rest)
[![Coverage Status](https://coveralls.io/repos/github/Ensembl/gifts_rest/badge.svg)](https://coveralls.io/github/Ensembl/gifts_rest)

Initial version of the GIFTS REST interface.

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py collectstatic

python manage.py runserver
```