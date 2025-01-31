from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode

import re

def extract_message_id(url):
    match = re.search(r'/(\d+)$', url)
    return int(match.group(1)) if match else None

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('bulk'))
async def bulk(client: Client, message: Message):
    try:
        bulk_input = await client.ask(
            text="Send the structured text with subjects and links.",
            chat_id=message.from_user.id,
            filters=filters.text,
            timeout=180
        )
    except:
        return
    
    bulk_text = bulk_input.text.strip()
    subjects = {}
    current_subject = None

    # Processing user input
    for line in bulk_text.split("\n"):
        if not line.strip():
            continue
        if not line.startswith("1 ") and not line.startswith("2 "):
            current_subject = line.strip()
            subjects[current_subject] = []
        else:
            subjects[current_subject].append(line.split(" ")[1])

    response_text = ""
    for subject, links in subjects.items():
        if len(links) < 2:
            response_text += f"{subject}\n❌ Error: Missing links\n\n"
            continue

        f_msg_id = extract_message_id(links[0])
        s_msg_id = extract_message_id(links[1])

        if not f_msg_id or not s_msg_id:
            response_text += f"{subject}\n❌ Error: Invalid links\n\n"
            continue

        # Generate batch link
        string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
        base64_string = await encode(string)
        batch_link = f"https://t.me/{client.username}?start={base64_string}"

        response_text += f"{subject}\n🔗 <code>{batch_link}</code>\n\n"

    # Send response
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={batch_link}')]])
    await message.reply_text(response_text, quote=True, reply_markup=reply_markup)
