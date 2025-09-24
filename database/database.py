import pymongo, os
from config import DB_URI, DB_NAME

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']
special_messages = database['special_messages']

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

async def add_special_message(msg_id: int):
    """
    Add a message ID to the special messages collection.
    """
    special_messages.update_one(
        {'_id': 'special_msg_ids'},
        {'$addToSet': {'msg_ids': msg_id}},
        upsert=True
    )
    return

async def remove_special_message(msg_id: int):
    """
    Remove a message ID from the special messages collection.
    """
    special_messages.update_one(
        {'_id': 'special_msg_ids'},
        {'$pull': {'msg_ids': msg_id}}
    )
    return

async def get_special_messages():
    """
    Retrieve all special message IDs.
    """
    doc = special_messages.find_one({'_id': 'special_msg_ids'})
    return doc['msg_ids'] if doc and 'msg_ids' in doc else []
