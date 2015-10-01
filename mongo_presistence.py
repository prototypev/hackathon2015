from pymongo import MongoClient


mongodb_url = 'mongodb://localhost:27017/'


def get_db():
    client = MongoClient(mongodb_url)
    return client.hackathon_database


def get_oauth_collection(db):
    return db.oauthCollection


def create_oauth_info(db, oauthInfo):
    return get_oauth_collection(db).insert_one(oauthInfo).inserted_id


def get_oauth_info(db):
    return get_oauth_collection(db).find_one()


def insert_email(db, email):
    return db.emails.insert_one(email).inserted_id


def get_email_collection(db):
    return db.emails