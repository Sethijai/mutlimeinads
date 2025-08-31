#(©)CodeFlix_Bots

import base64
import re
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, FORCE_SUB_CHANNEL3, FORCE_SUB_CHANNEL4, ADMINS
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait
from typing import Tuple, Union

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
    base64_string = base64_string.strip("=")
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
        base64_string2 = base64_string2.strip("=")
        base64_bytes = (base64_string2 + "=" * (-len(base64_string2) % 4)).encode("ascii")
        string_bytes = base64.urlsafe_b64decode(base64_bytes)
        string = string_bytes.decode("ascii")
        return string
    except Exception as e:
        print(f"Decode_new error: {e}")
        raise

async def encode_link(user_id: int = None, f_msg_id: int = None, s_msg_id: int = None, channel_id: int = None) -> str:
    """
    Encode a Telegram bot deep link for batch or HACKHEIST access.
    
    Args:
        user_id: User ID (required for HACKHEIST, optional for batch)
        f_msg_id: First message ID (required)
        s_msg_id: Second message ID (optional for batch, None for HACKHEIST or single message)
        channel_id: Channel ID (required)
        
    Returns:
        Telegram bot deep link: https://t.me/AK_LECTURES_BOT?start={encoded_string}
    """
    if channel_id is None or f_msg_id is None:
        raise ValueError("channel_id and f_msg_id are required")
    
    # Create the string to encode
    if user_id is not None and s_msg_id is None:
        # HACKHEIST link for single message
        raw_string = f"HACKHEIST-{user_id}-{f_msg_id}-{channel_id}"
    elif s_msg_id is not None:
        # Batch link for message range
        raw_string = f"get-{channel_id}-{f_msg_id}-{s_msg_id}"
    else:
        # Batch link for single message
        raw_string = f"get-{channel_id}-{f_msg_id}"
    
    # Encode to base64
    string_bytes = raw_string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii").rstrip("=")
    
    return f"https://t.me/AK_LECTURES_BOT?start={base64_string}"

async def decode_link(encoded_string: str) -> Tuple[str, Union[int, None], int, int, Union[int, None]]:
    """
    Decode a base64 string from a Telegram bot deep link.
    
    Args:
        encoded_string: The base64 encoded string (without the Telegram URL prefix)
        
    Returns:
        Tuple of (link_type, user_id, f_msg_id, channel_id, s_msg_id)
        - link_type: "HACKHEIST" or "batch"
        - user_id: User ID (for HACKHEIST) or None (for batch)
        - f_msg_id: First message ID
        - channel_id: Channel ID
        - s_msg_id: Second message ID (None for single message or HACKHEIST)
    """
    # Handle padding
    encoded_string = encoded_string.rstrip("=")
    base64_bytes = (encoded_string + "=" * (-len(encoded_string) % 4)).encode("ascii")
    
    # Decode base64
    try:
        string_bytes = base64.urlsafe_b64decode(base64_bytes)
        decoded_string = string_bytes.decode("ascii")
    except (base64.binascii.Error, UnicodeDecodeError):
        raise ValueError("Invalid base64 encoded string")
    
    # Parse the decoded string
    parts = decoded_string.split("-")
    
    if decoded_string.startswith("HACKHEIST-"):
        # HACKHEIST link: HACKHEIST-user_id-msg_id-channel_id
        if len(parts) != 4:
            raise ValueError("Invalid HACKHEIST string structure")
        try:
            user_id = int(parts[1])
            f_msg_id = int(parts[2])
            channel_id = int(parts[3])  # Handles negative or positive channel_id
            return "HACKHEIST", user_id, f_msg_id, channel_id, None
        except (ValueError, IndexError):
            raise ValueError("Invalid number format in HACKHEIST string")
    
    elif decoded_string.startswith("get-"):
        # Batch link: get--channel_id-f_msg_id-s_msg_id or get-channel_id-f_msg_id-s_msg_id
        if len(parts) not in [3, 4, 5]:
            raise ValueError("Invalid batch string structure")
        try:
            if parts[1] == "":
                # Negative channel ID: get--channel_id-...
                channel_id = int(f"-{parts[2]}")
                f_msg_id = int(parts[3])
                s_msg_id = int(parts[4]) if len(parts) == 5 else None
            else:
                # Positive channel ID: get-channel_id-...
                channel_id = int(parts[1])
                f_msg_id = int(parts[2])
                s_msg_id = int(parts[3]) if len(parts) == 4 else None
            return "batch", None, f_msg_id, channel_id, s_msg_id
        except (ValueError, IndexError):
            raise ValueError("Invalid number format in batch string")
    
    else:
        raise ValueError("Invalid encoded string format")

async def get_messages(client, message_ids, channel_id):
    """
    Fetch messages from a specified channel by message IDs.
    
    Args:
        client: Pyrogram client
        message_ids: List of message IDs to fetch
        channel_id: Channel ID to fetch messages from
        
    Returns:
        List of fetched messages (may include None for inaccessible messages)
    """
    messages = []
    total_messages = 0

    if not message_ids:
        print("No message IDs provided")
        return messages
    if not channel_id:
        print("No channel ID provided")
        return messages

    # Validate channel access
    try:
        await client.get_chat(channel_id)
        print(f"Access confirmed for channel {channel_id}")
    except ChannelInvalid:
        print(f"Invalid channel ID: {channel_id}")
        return messages
    except ChatAdminRequired:
        print(f"Bot requires admin access to channel: {channel_id}")
        return messages
    except Exception as e:
        print(f"Error accessing channel {channel_id}: {e}")
        return messages

    while total_messages < len(message_ids):
        temb_ids = message_ids[total_messages:total_messages+200]
        try:
            msgs = await client.get_messages(
                chat_id=channel_id,
                message_ids=temb_ids
            )
            valid_msgs = [msg for msg in (msgs if isinstance(msgs, list) else [msgs]) if msg is not None]
            if valid_msgs:
                print(f"Fetched {len(valid_msgs)} messages for IDs {temb_ids} in channel {channel_id}")
            else:
                print(f"No valid messages found for IDs {temb_ids} in channel {channel_id}")
            messages.extend(valid_msgs)
        except FloodWait as e:
            print(f"FloodWait: Waiting {e.value} seconds for channel {channel_id}")
            await asyncio.sleep(e.value)
            try:
                msgs = await client.get_messages(
                    chat_id=channel_id,
                    message_ids=temb_ids
                )
                valid_msgs = [msg for msg in (msgs if isinstance(msgs, list) else [msgs]) if msg is not None]
                if valid_msgs:
                    print(f"Fetched {len(valid_msgs)} messages for IDs {temb_ids} in channel {channel_id} after FloodWait")
                else:
                    print(f"No valid messages found for IDs {temb_ids} in channel {channel_id} after FloodWait")
                messages.extend(valid_msgs)
            except Exception as e:
                print(f"Error after FloodWait for IDs {temb_ids} in channel {channel_id}: {e}")
        except MessageIdsInvalid:
            print(f"Invalid message IDs: {temb_ids} in channel {channel_id}")
        except Exception as e:
            print(f"Error fetching messages for IDs {temb_ids} in channel {channel_id}: {e}")
        total_messages += len(temb_ids)

    if messages:
        print(f"Successfully fetched {len(messages)} messages from channel {channel_id}")
    else:
        print(f"No messages fetched for IDs {message_ids} in channel {channel_id}")
    return messages

async def get_message_id(client, message):
    if message.forward_origin and hasattr(message.forward_origin, 'chat'):
        # Handle forwarded messages
        return message.forward_origin.chat.id, message.forward_origin.message_id
    elif message.forward_origin and hasattr(message.forward_origin, 'sender_user_name'):
        return None, 0  # Forwarded from a hidden user, invalid
    elif message.text:
        # Handle both private (https://t.me/c/2493255368/45956) and public (https://t.me/username/45956) links
        pattern = r"https://t.me/(?:c/)?([^/]+)/(\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return None, 0
        channel_identifier = matches.group(1)  # Either channel ID (digits) or username
        msg_id = int(matches.group(2))
        try:
            if channel_identifier.isdigit():
                # Private channel (e.g., 2493255368)
                channel_id = int(f"-100{channel_identifier}")
            else:
                # Public channel (e.g., username)
                chat = await client.get_chat(channel_identifier)
                channel_id = chat.id
            return channel_id, msg_id
        except:
            return None, 0
    else:
        return None, 0

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
       
