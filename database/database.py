# database.py
import pymongo, os
from config import DB_URI, DB_NAME

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']
random_messages = database['random_messages']  # Collection for random message IDs

async def present_user(user_id: int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

async def add_random_message(channel_id: str, msg_id: int):
    random_messages.insert_one({'channel_id': channel_id, 'msg_id': msg_id})
    return

async def remove_random_message(channel_id: str, msg_id: int):
    random_messages.delete_one({'channel_id': channel_id, 'msg_id': msg_id})
    return

async def get_all_random_messages():
    messages = random_messages.find()
    return [(doc['channel_id'], doc['msg_id']) for doc in messages]
