import random
import os, asyncio, humanize
import base64
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import *
from helper_func import subscribed, encode, decode, get_messages, add_user, del_user, present_user, full_userbase

codeflixbots = FILE_AUTO_DELETE
subaru = codeflixbots
file_auto_delete = humanize.naturaldelta(subaru)

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except Exception as e:
            print(f"Error adding user: {e}")
            pass
    
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except IndexError:
            return

        string = await decode(base64_string)
        argument = string.split("-")
        
        # Handle new format: get-{user_id}-{msg_id * abs(client.db_channel.id)}
        if len(argument) == 3 and argument[0] == "get":
            try:
                user_id = int(argument[1])
                encoded_msg_id = int(argument[2])
                msg_id = int(encoded_msg_id / abs(client.db_channel.id))
                
                # Check if the user_id matches the message sender
                if user_id != id:
                    await message.reply_text("This link is not for you!")
                    return

                temp_msg = await message.reply("𝗥𝘂𝗸 𝗘𝗸 𝗦𝗲𝗰 👽..")
                try:
                    messages = await get_messages(client, [msg_id])
                except Exception as e:
                    await message.reply_text("Something Went Wrong..!")
                    print(f"Error getting message: {e}")
                    return
                finally:
                    await temp_msg.delete()

                for msg in messages:
                    filename = "Unknown"
                    media_type = "Unknown"

                    if msg.video:
                        media_type = "Video"
                        filename = msg.video.file_name if msg.video.file_name else "Unnamed Video"
                    elif msg.document:
                        filename = msg.document.file_name if msg.document.file_name else "Unnamed Document"
                        media_type = "PDF" if filename.endswith(".pdf") else "Document"
                    elif msg.photo:
                        media_type = "Image"
                        filename = "Image"
                    elif msg.text:
                        media_type = "Text"
                        filename = "Text Content"

                    caption = (
                        CUSTOM_CAPTION.format(
                            previouscaption=(msg.caption.html if msg.caption else "🔥 𝐇𝐈𝐃𝐃𝐄𝐍𝐒 🔥"),
                            filename=filename,
                            mediatype=media_type,
                        )
                        if bool(CUSTOM_CAPTION)
                        else (msg.caption.html if msg.caption else "")
                    )

                    reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None

                    try:
                        await msg.copy(
                            chat_id=message.from_user.id,
                            caption=caption,
                            parse_mode=ParseMode.HTML,
                            reply_markup=reply_markup,
                            protect_content=False,  # Set to False for the button link
                        )
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                        await msg.copy(
                            chat_id=message.from_user.id,
                            caption=caption,
                            parse_mode=ParseMode.HTML,
                            reply_markup=reply_markup,
                            protect_content=False,
                        )
                    except Exception as e:
                        print(f"Failed to send message: {e}")
                return

        # Existing logic for range or single message IDs
        ids = []
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            except Exception as e:
                print(f"Error decoding IDs: {e}")
                return
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                print(f"Error decoding ID: {e}")
                return

        temp_msg = await message.reply("�_R𝘂𝗸 𝗘𝗸 𝗦𝗲𝗰 👽..")
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            await message.reply_text("Something Went Wrong..!")
            print(f"Error getting messages: {e}")
            return
        finally:
            await temp_msg.delete()

        codeflix_msgs = []
        for msg in messages:
            filename = "Unknown"
            media_type = "Unknown"

            if msg.video:
                media_type = "Video"
                filename = msg.video.file_name if msg.video.file_name else "Unnamed Video"
            elif msg.document:
                filename = msg.document.file_name if msg.document.file_name else "Unnamed Document"
                media_type = "PDF" if filename.endswith(".pdf") else "Document"
            elif msg.photo:
                media_type = "Image"
                filename = "Image"
            elif msg.text:
                media_type = "Text"
                filename = "Text Content"

            caption = (
                CUSTOM_CAPTION.format(
                    previouscaption=(msg.caption.html if msg.caption else "🔥 𝐇𝐈𝐃𝐃𝐄𝐍𝐒 🔥"),
                    filename=filename,
                    mediatype=media_type,
                )
                if bool(CUSTOM_CAPTION)
                else (msg.caption.html if msg.caption else "")
            )

            # Generate base64-encoded URL for the button
            base64_string2 = await encode(f"get-{id}-{msg.id * abs(client.db_channel.id)}")
            button_url = f"https://t.me/Jaddu2bot?start={base64_string2}"
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔗 𝐅𝐨𝐫 𝐅𝐨𝐫𝐰𝐚𝐫𝐝𝐢𝐧𝐠", url=button_url)]]
            ) if DISABLE_CHANNEL_BUTTON else msg.reply_markup

            try:
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT,
                )
                if copied_msg:
                    codeflix_msgs.append(copied_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT,
)
                if copied_msg:
                    codeflix_msgs.append(copied_msg)
            except Exception as e:
                print(f"Failed to send message: {e}")

        # Notify user about auto-deletion
        k = await client.send_message(
            chat_id=message.from_user.id,
            text=f"<b>‼️ 𝐓𝐡𝐞𝐬𝐞 𝐋𝐄𝐂𝐓𝐔𝐑𝐄𝐒/𝐏𝐃𝐅𝐬 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐜 𝐃𝐞𝐥𝐞𝐭𝐢𝐧𝐠 𝐢𝐧 𝟭𝟮 𝗛𝗼𝘂𝗿𝘀 🔥</b>\n\n"
                 f"<b>ʙᴜᴛ ᴅᴏɴ'ᴛ ᴡᴏʀʀʏ 😁 ᴀғᴛᴇʀ ᴅᴇʟᴇᴛᴇᴅ ʏᴏᴜ ᴄᴀɴ ᴀɢᴀɪɴ ᴀᴄᴄᴇss ᴛʜʀᴏᴜɢʜ ᴏᴜʀ ᴡᴇʙsɪᴛᴇs 😘</b>\n\n"
                 f"<b> <a href=https://yashyasag.github.io/hiddens_officials>🌟 𝗢𝗧𝗛𝗘𝗥 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦 🌟</a></b>",
        )

        codeflix_msgs.append(k)
        asyncio.create_task(delete_files(codeflix_msgs, client, message, k))
        return

    else:
        reply_markup = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("🔥 𝗠𝗔𝗜𝗡 𝗪𝗘𝗕𝗦𝗜𝗧𝗘 🔥", url="https://yashyasag.github.io/hiddens_officials")
            ],[
                InlineKeyboardButton("‼️ 𝗕𝗔𝗖𝗞𝗨𝗣 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 ‼️", url="https://t.me/+Sk3pfX_PWTQ3NmI1")
            ],[
                InlineKeyboardButton("👻 ᴄᴏɴᴛᴀᴄᴛ ᴜs 👻", url="https://t.me/TEAM_HIDDENS_BOT")
            ]]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="😈 𝗢𝗣𝗠𝗔𝗦𝗧𝗘𝗥𝗦 💀", url=client.invitelink4),
        ],
        [
            InlineKeyboardButton(text="🌟 𝗝𝗼𝗶�_n 𝟭𝘀𝘁 🌟", url=client.invitelink),
            InlineKeyboardButton(text="💝 𝗝𝗼𝗶𝗻 𝟮𝗻𝗱 💝", url=client.invitelink2),
        ],
        [
            InlineKeyboardButton(text="🕊 𝗝𝗼𝗶𝗻 𝟯𝗿𝗱 🕊", url=client.invitelink3),
        ]        
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='♻️ 𝐓𝐑𝐘 𝐀𝐆𝐀𝐈𝐍 ♻️',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=f"Processing...")
    users = await full_userbase()
    await msg.edit(f"{len(users)} Users Are Using This Bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if not message.reply_to_message:
        msg = await message.reply("Reply to a message to broadcast it.")
        await asyncio.sleep(8)
        return await msg.delete()

    # Extract seconds from command if provided
    try:
        seconds = int(message.text.split(maxsplit=1)[1])
    except (IndexError, ValueError):
        seconds = None  # No auto-delete if not provided

    query = await full_userbase()
    broadcast_msg = message.reply_to_message
    total = 0
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0
    sent_messages = []  # To store (chat_id, message_id)

    pls_wait = await message.reply("<i>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴘʀᴏᴄᴇꜱꜱɪɴɢ ᴛɪʟʟ ᴡᴀɪᴛ ʙʀᴏᴏ... </i>")

    for chat_id in query:
        try:
            sent = await broadcast_msg.copy(chat_id)
            sent_messages.append((chat_id, sent.id))
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
            sent = await broadcast_msg.copy(chat_id)
            sent_messages.append((chat_id, sent.id))
            successful += 1
        except UserIsBlocked:
            await del_user(chat_id)
            blocked += 1
        except InputUserDeactivated:
            await del_user(chat_id)
            deleted += 1
        except:
            unsuccessful += 1
            pass
        total += 1

    status = f"""<b><u>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</u>

ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ: <code>{total}</code>
ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{successful}</code>
ʙʟᴏᴄᴋᴇᴅ ᴜꜱᴇʀꜱ: <code>{blocked}</code>
ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ: <code>{deleted}</code>
ᴜɴꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{unsuccessful}</code></b>"""

    await pls_wait.edit(status)

    # Schedule deletion after given seconds if specified
    if seconds:
        await asyncio.sleep(seconds)
        for chat_id, msg_id in sent_messages:
            try:
                await client.delete_messages(chat_id, msg_id)
            except:
                pass

# Function to handle file deletion
async def delete_files(codeflix_msgs, client, message, k):
    await asyncio.sleep(FILE_AUTO_DELETE)  # Wait for the duration specified in config.py
    
    for msg in codeflix_msgs:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            print(f"The attempt to delete the media {msg.id} was unsuccessful: {e}")
