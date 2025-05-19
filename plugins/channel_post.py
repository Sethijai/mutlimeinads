import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, WEBSITE_URL, WEBSITE_URL_MODE
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats','nbatch']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return

    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    if WEBSITE_URL_MODE == True:
        link = f"{WEBSITE_URL}?HACKHEIST={base64_string}"
    else:
        link = f"https://t.me/{client.username}?start={base64_string}"
        
    await reply_text.edit(f"<b>Here is your link</b>\n\n<code>{link}</code>", disable_web_page_preview=True)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):
    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    if WEBSITE_URL_MODE == True:
        link = f"{WEBSITE_URL}?HACKHEIST={base64_string}"
    else:
        link = f"https://t.me/{client.username}?start={base64_string}"
    
    # Removed the line that edits message with the link
    try:
        pass  # Placeholder for any future use
    except Exception as e:
        print(e)
        pass
