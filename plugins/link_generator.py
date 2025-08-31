from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode
import re

def extract_message_details(url):
    # Match URLs like https://t.me/c/{channel_id_without_-100}/{msg_id}
    match = re.search(r'https://t\.me/c/([^/]+)/(\d+)$', url)
    if match:
        channel_id_without_minus_100 = match.group(1)
        msg_id = int(match.group(2))
        return msg_id, channel_id_without_minus_100
    return None, None

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def bulk(client: Client, message: Message):
    try:
        bulk_input = await client.ask(
            text="Send the structured text with subjects and links (e.g., https://t.me/c/123456789/1).",
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

        f_msg_id, f_channel_id = extract_message_details(links[0])
        s_msg_id, s_channel_id = extract_message_details(links[1])

        if not f_msg_id or not s_msg_id or not f_channel_id or not s_channel_id:
            response_text += f"{subject}\n❌ Error: Invalid links\n\n"
            continue

        # Ensure both links are from the same channel
        if f_channel_id != s_channel_id:
            response_text += f"{subject}\n❌ Error: Links must be from the same channel\n\n"
            continue

        # Generate batch link with channel_id from message link
        channel_id_without_minus_100 = f_channel_id
        modified_channel_id = int(channel_id_without_minus_100) * 8  # Multiply by 8
        string = f"get-{f_msg_id}-{s_msg_id}--100{modified_channel_id}"
        base64_string = await encode(string)
        batch_link = f"https://t.me/{client.username}?start={base64_string}"

        response_text += f"{subject}\n{batch_link}\n\n"

    # Send response
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={batch_link}')]])
    await message.reply_text(response_text, quote=True, reply_markup=reply_markup)
