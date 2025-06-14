import pymongo
import time
from typing import Tuple  # For Python 3.8 compatibility
from config import *

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

user_data = database['users']
premium_users = database['premiumusers']
channel_data = database[f'channels{TG_BOT_TOKEN}']
fsub_data = database[f'fsub{TG_BOT_TOKEN}']   
rqst_fsub_data = database[f'request_forcesub{TG_BOT_TOKEN}']
rqst_fsub_Channel_data = database[f'request_forcesub_channel{TG_BOT_TOKEN}']

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
    print(f"Added premium for user {user_id}: expiration_time={expiration_time}")

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
    print(f"Added All premium: expiration_time={expiration_time}")

async def remove_premium_user(user_id: int) -> None:
    """
    Remove a user's premium status.
    """
    premium_users.delete_one({'_id': user_id})
    print(f"Removed premium for user {user_id}")

async def is_premium_user(user_id: int) -> Tuple[bool, int]:
    """
    Check if a user is premium by comparing current time to expiration time.
    Returns (is_premium, remaining_time).
    is_premium is True only if remaining_time > 0.
    """
    current_time = int(time.time())
    
    # Check individual premium status
    user_doc = premium_users.find_one({'_id': user_id})
    if user_doc and 'expiration_time' in user_doc:
        remaining_time = user_doc['expiration_time'] - current_time
        print(f"User {user_id} check: expiration_time={user_doc['expiration_time']}, remaining_time={remaining_time}")
        if remaining_time > 0:
            return True, remaining_time
    
    # Check global 'All' premium status
    all_doc = premium_users.find_one({'_id': 'All'})
    if all_doc and 'expiration_time' in all_doc:
        remaining_time = all_doc['expiration_time'] - current_time
        print(f"All premium check: expiration_time={all_doc['expiration_time']}, remaining_time={remaining_time}")
        if remaining_time > 0:
            return True, remaining_time
    
    print(f"User {user_id} is not premium: no valid premium entry found")
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
    
    print(f"Premium users list: {premium_list}")
    return premium_list
    
async def channel_exist(channel_id: int):
    found = await fsub_data.find_one({'_id': channel_id})
    return bool(found)
    
async def add_channel(channel_id: int):
    if not await channel_exist(channel_id):
        await fsub_data.insert_one({'_id': channel_id})
        return

async def rem_channel(channel_id: int):
    if await channel_exist(channel_id):
        await fsub_data.delete_one({'_id': channel_id})
        return

async def show_channels():
    channel_docs = await fsub_data.find().to_list(length=None)
    channel_ids = [doc['_id'] for doc in channel_docs]
    return channel_ids

    
# Get current mode of a channel
async def get_channel_mode(channel_id: int):
    data = await fsub_data.find_one({'_id': channel_id})
    return data.get("mode", "off") if data else "off"

    # Set mode of a channel
async def set_channel_mode(channel_id: int, mode: str):
    await fsub_data.update_one(
        {'_id': channel_id},
        {'$set': {'mode': mode}},
        upsert=True
    )

    # REQUEST FORCE-SUB MANAGEMENT

    # Add the user to the set of users for a   specific channel
async def req_user(channel_id: int, user_id: int):
    try:
        await rqst_fsub_Channel_data.update_one(
            {'_id': int(channel_id)},
            {'$addToSet': {'user_ids': int(user_id)}},
            upsert=True
        )
    except Exception as e:
        print(f"[DB ERROR] Failed to add user to request list: {e}")


    # Method 2: Remove a user from the channel set
async def del_req_user(channel_id: int, user_id: int):
        # Remove the user from the set of users for the channel
    await rqst_fsub_Channel_data.update_one(
        {'_id': channel_id}, 
        {'$pull': {'user_ids': user_id}}
    )

    # Check if the user exists in the set of the channel's users
async def req_user_exist(channel_id: int, user_id: int):
    try:
        found = await rqst_fsub_Channel_data.find_one({
            '_id': int(channel_id),
            'user_ids': int(user_id)
        })
        return bool(found)
    except Exception as e:
        print(f"[DB ERROR] Failed to check request list: {e}")
        return False  


    # Method to check if a channel exists using show_channels
async def reqChannel_exist(channel_id: int):
    # Get the list of all channel IDs from the database 
    channel_ids = await show_channels()
        #print(f"All channel IDs in the database: {channel_ids}")

    # Check if the given channel_id is in the list of channel IDs
    if channel_id in channel_ids:
            #print(f"Channel {channel_id} found in the database.")
        return True
    else:
            #print(f"Channel {channel_id} NOT found in the database.")
        return False

db = Database(DB_URI, DB_NAME, TG_BOT_TOKEN)
