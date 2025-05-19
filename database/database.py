import pymongo
import time
from typing import Tuple  # For Python 3.8 compatibility
from config import DB_URI, DB_NAME

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

user_data = database['users']
premium_users = database['premiumusers']

async def present_user(user_id: int) -> bool:
    """
    Check if a user exists in the users collection.
    """
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int) -> None:
    """
    Add a user to the users collection.
    """
    user_data.insert_one({'_id': user_id})

async def full_userbase() -> list:
    """
    Get all user IDs from the users collection.
    """
    user_docs = user_data.find()
    user_ids = [doc['_id'] for doc in user_docs]
    return user_ids

async def del_user(user_id: int) -> None:
    """
    Delete a user from the users collection.
    """
    user_data.delete_one({'_id': user_id})

async def add_premium_user(user_id: int, duration: int) -> None:
    """
    Add a user as premium with an expiration time (duration in seconds from command time).
    Stores expiration_time as current timestamp + duration.
    """
    expiration_time = int(time.time()) + duration
    premium_users.update_one(
        {'_id': user_id},
        {'$set': {'expiration_time': expiration_time}},
        upsert=True
    )

async def add_all_premium(duration: int) -> None:
    """
    Set all users as premium for the specified duration (in seconds from command time).
    Stores a global expiration time for 'All' users.
    """
    expiration_time = int(time.time()) + duration
    premium_users.update_one(
        {'_id': 'All'},
        {'$set': {'expiration_time': expiration_time}},
        upsert=True
    )

async def remove_premium_user(user_id: int) -> None:
    """
    Remove a user's premium status.
    """
    premium_users.delete_one({'_id': user_id})

async def is_premium_user(user_id: int) -> Tuple[bool, int]:
    """
    Check if a user is premium by comparing current time to expiration time.
    Returns (is_premium, remaining_time).
    is_premium is True if remaining_time > 0, False otherwise.
    """
    current_time = int(time.time())
    
    # Check individual premium status
    user_doc = premium_users.find_one({'_id': user_id})
    if user_doc and 'expiration_time' in user_doc:
        remaining_time = user_doc['expiration_time'] - current_time
        if remaining_time > 0:
            return True, remaining_time
    
    # Check global 'All' premium status
    all_doc = premium_users.find_one({'_id': 'All'})
    if all_doc and 'expiration_time' in all_doc:
        remaining_time = all_doc['expiration_time'] - current_time
        if remaining_time > 0:
            return True, remaining_time
    
    return False, 0

async def list_premium_users() -> list:
    """
    List all premium users and their remaining time (in seconds).
    Returns a list of tuples: [(user_id, remaining_time), ...].
    Includes 'All' if active.
    """
    premium_docs = premium_users.find()
    current_time = int(time.time())
    premium_list = []
    
    for doc in premium_docs:
        user_id = doc['_id']
        remaining_time = doc['expiration_time'] - current_time if 'expiration_time' in doc else 0
        if remaining_time > 0:
            premium_list.append((user_id, remaining_time))
    
    return premium_list
