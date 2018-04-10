import datetime
import os
import sys

from pymongo import MongoClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import random_id

MONGODB_URI = os.environ.get(
    'MONGODB_URI', 'mongodb://localhost:27017/rsvpdata'
)


def up(db):
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    db.events.rename('event', dropTarget=True)
    for event in db.event.find():
        if isinstance(event['date'], datetime.datetime):
            continue

        db.event.find_one_and_update(
            {'_id': event['_id']},
            {
                '$set': {
                    'date': datetime.datetime.strptime(
                        event['date'], '%Y-%m-%d'
                    )
                }
            },
        )


def down(db):
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    db.event.rename('events', dropTarget=True)