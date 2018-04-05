# rsvpapp

RSVP app for TIKS

## Installation & Running the app

1. Setup a virtualenv and activate it

```sh
virtualenv -p python3 /path/to/venv
source /path/to/venv/bin/activate
```

2. Install the requirements

```sh
pip install -r requirements.txt
```

3. Setup environment variables

```sh
export LOGO=https://thatteidlikaalsoup.team/images/tiks-logo.ico
export TEXT1="Thatte Idli Kaal Soup"
export TEXT2="Practice RSVP"
export COMPANY="Thatte Idli Kaal Soup"
export DEBUG=1
```

4. Run the app

```sh
python rsvp.py
```
