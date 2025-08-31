#(©)CodeFlix_Bots

import base64
import re
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, FORCE_SUB_CHANNEL3, FORCE_SUB_CHANNEL4, ADMINS
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait

async def is_subscribed(filter, client, update):
    if not FORCE_SUB_CHANNEL:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(chat_id = FORCE_SUB_CHANNEL, user_id = user_id)
    except UserNotParticipant:
        return False

    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    else:
        return True

async def is_subscribed(filter, client, update):
    if not FORCE_SUB_CHANNEL2:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(chat_id = FORCE_SUB_CHANNEL2, user_id = user_id)
    except UserNotParticipant:
        return False

    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    else:
        return True

async def is_subscribed(filter, client, update):
    if not FORCE_SUB_CHANNEL3:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(chat_id = FORCE_SUB_CHANNEL3, user_id = user_id)
    except UserNotParticipant:
        return False

    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    else:
        return True

async def is_subscribed(filter, client, update):
    if not FORCE_SUB_CHANNEL4:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(chat_id = FORCE_SUB_CHANNEL4, user_id = user_id)
    except UserNotParticipant:
        return False

    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    else:
        return True
    
async def is_subscribed(filter, client, update):
    if not FORCE_SUB_CHANNEL:
        return True
    if not FORCE_SUB_CHANNEL2:
        return True
    if not FORCE_SUB_CHANNEL3:
        return True  
    if not FORCE_SUB_CHANNEL4:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(chat_id = FORCE_SUB_CHANNEL, user_id = user_id)
    except UserNotParticipant:
        return False

    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    try:
        member = await client.get_chat_member(chat_id = FORCE_SUB_CHANNEL2, user_id = user_id)
    except UserNotParticipant:
        return False
    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    try:
        member = await client.get_chat_member(chat_id = FORCE_SUB_CHANNEL3, user_id = user_id)
    except UserNotParticipant:
        return False        
    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    try:
        member = await client.get_chat_member(chat_id = FORCE_SUB_CHANNEL4, user_id = user_id)
    except UserNotParticipant:
        return False                
    else:
        return True

async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii").strip("=")
    return base64_string

async def decode(base64_string):
    base64_string = base64_string.strip("=")  # Handle any remaining padding
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    string = string_bytes.decode("ascii")
    return string

async def encode_new(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string2 = base64_bytes.decode("ascii").strip("=")
    return base64_string2

async def decode_new(base64_string2):
    try:
        base64_string2 = base64_string2.strip("=")  # Handle any remaining padding
        base64_bytes = (base64_string2 + "=" * (-len(base64_string2) % 4)).encode("ascii")
        string_bytes = base64.urlsafe_b64decode(base64_bytes)
        string = string_bytes.decode("ascii")
        return string
    except Exception as e:
        print(f"Decode_new error: {e}")
        raise

async def get_messages(client, message_ids, channel_id):
    if not message_ids:
        raise ValueError("No message IDs provided")
    if not channel_id:
        raise ValueError("No channel ID provided")

    # Attempt to ensure channel access
    try:
        chat = await client.get_chat(channel_id)
        print(f"Successfully accessed channel {channel_id}: {chat.title}")
    except ChannelInvalid:
        print(f"ChannelInvalid: Bot does not have access to channel {channel_id}")
        try:
            # Attempt to join the channel if possible (e.g., if public or bot has an invite link)
            await client.join_chat(channel_id)
            print(f"Joined channel {channel_id} successfully")
        except Exception as join_error:
            print(f"Failed to join channel {channel_id}: {join_error}")
            raise ChannelInvalid(f"Bot cannot access channel {channel_id}. Ensure the bot is a member.")
    except ChatAdminRequired:
        print(f"ChatAdminRequired: Bot needs admin rights for channel {channel_id}")
        raise ChatAdminRequired(f"Bot requires admin access to channel {channel_id}")
    except Exception as e:
        print(f"Error accessing channel {channel_id}: {e}")
        raise Exception(f"Error accessing channel {channel_id}: {e}")

    messages = []
    total_messages = 0
    while total_messages < len(message_ids):
        temb_ids = message_ids[total_messages:total_messages+200]
        try:
            msgs = await client.get_messages(
                chat_id=channel_id,
                message_ids=temb_ids
            )
            # Filter out None or invalid messages
            valid_msgs = [msg for msg in msgs if msg is not None]
            if not valid_msgs:
                print(f"No valid messages found for IDs {temb_ids} in channel {channel_id}")
            messages.extend(valid_msgs)
        except FloodWait as e:
            print(f"FloodWait: Waiting {e.x} seconds for IDs {temb_ids}")
            await asyncio.sleep(e.x)
            try:
                msgs = await client.get_messages(
                    chat_id=channel_id,
                    message_ids=temb_ids
                )
                valid_msgs = [msg for msg in msgs if msg is not None]
                messages.extend(valid_msgs)
            except Exception as retry_error:
                print(f"Error fetching messages after FloodWait for IDs {temb_ids}: {retry_error}")
                raise
        except MessageIdsInvalid:
            print(f"Invalid message IDs: {temb_ids} in channel {channel_id}")
            raise MessageIdsInvalid(f"Invalid message IDs: {temb_ids}")
        except Exception as e:
            print(f"Error fetching messages for IDs {temb_ids} in channel {channel_id}: {e}")
            raise
        total_messages += len(temb_ids)
    
    if not messages:
        raise ValueError(f"No messages found for IDs {message_ids} in channel {channel_id}")
    
    return messages

async def get_message_id(client, message):
    if message.forward_from_chat:
        return message.forward_from_message_id, str(message.forward_from_chat.id)
    elif message.forward_sender_name:
        return 0, None
    elif message.text:
        pattern = r"https://t\.me/(?:c/)?([^/]+)/(\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return 0, None
        channel_id_without_minus_100 = matches.group(1)
        msg_id = int(matches.group(2))
        # Reconstruct full channel ID
        channel_id = f"-100{channel_id_without_minus_100}"
        return msg_id, channel_id
    else:
        return 0, None

def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time

subscribed = filters.create(is_subscribed)
       
