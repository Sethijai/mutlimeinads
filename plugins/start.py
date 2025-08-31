import random
import os, asyncio, humanize
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import *
from helper_func import subscribed, encode, decode, encode_new, decode_new, get_messages
from database.database import add_user, del_user, full_userbase, present_user

# Different delete times for different access types
BULK_DELETE_TIME = FILE_AUTO_DELETE
try:
    INDIVIDUAL_DELETE_TIME = INDIVIDUAL_AUTO_DELETE
except NameError:
    INDIVIDUAL_DELETE_TIME = FILE_AUTO_DELETE

codeflixbots = FILE_AUTO_DELETE
subaru = codeflixbots
file_auto_delete = humanize.naturaldelta(subaru)

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            add_user(id)
        except Exception as e:
            print(f"Error adding user: {e}")
            pass
    
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except IndexError:
            return

        # Handle HACKHEIST for individual access
        try:
            string = await decode_new(base64_string)
            if string.startswith("HACKHEIST-"):
                # Split carefully to handle negative channel IDs
                parts = string.split("-")
                if len(parts) >= 4 and parts[0] == "HACKHEIST":
                    try:
                        user_id = int(parts[1])
                        msg_id = int(parts[2])
                        # Handle channel_id, which may include a negative sign
                        channel_id_str = "-".join(parts[3:])  # Rejoin remaining parts for negative channel_id
                        channel_id = int(channel_id_str)
                        
                        # Check if the current user is authorized
                        if message.from_user.id != user_id:
                            await message.reply_text("❌ You are not authorized to access this content!")
                            return
                        
                        temp_msg = await message.reply("𝗥𝘂𝗸 𝗘𝗸 𝗦𝗲𝗰 👽..")
                        try:
                            messages = await get_messages(client, [msg_id], channel_id)
                            if not messages or all(msg is None for msg in messages):
                                await temp_msg.edit("Failed to fetch message. It may have been deleted or is inaccessible.")
                                return
                        except Exception as e:
                            await temp_msg.edit(f"Something went wrong: {str(e)}")
                            print(f"Error getting message {msg_id} from {channel_id}: {e}")
                            return
                        finally:
                            await temp_msg.delete()

                        # Send the individual message with protect_content = False
                        codeflix_msgs = []
                        for msg in messages:
                            if not msg:
                                continue
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

                            # Generate caption
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
                                copied_msg = await msg.copy(
                                    chat_id=message.from_user.id,
                                    caption=caption,
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=reply_markup,
                                    protect_content=False,
                                )
                                
                                if copied_msg:
                                    codeflix_msgs.append(copied_msg)
                                    
                            except Exception as e:
                                print(f"Failed to send individual message: {e}")
                                await message.reply_text("❌ Failed to send the content!")
                                return
                        
                        # Notify user about auto-deletion for individual message
                        k = await client.send_message(
                            chat_id=message.from_user.id,
                            text=f"<b>‼️ 𝐓𝐡𝐢𝐬 𝐋𝐄𝐂𝐓𝐔𝐑𝐄/𝐏𝐃𝐅 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐜 𝐃𝐞𝐥𝐞𝐭𝐢𝐧𝐠 𝐢𝐧 𝟯 𝗗𝗮𝘆𝘀 💀</b>\n\n"
                                 f"<b>🥰 𝘕𝘰𝘸 𝘺𝘰𝘶 𝘤𝘢𝘯 𝘍𝘰𝘳𝘸𝘢𝘳𝘥 𝘵𝘩𝘪𝘴 𝘓𝘦𝘤𝘵𝘶𝘳𝘦/𝘗𝘥𝘧 𝘢𝘯𝘥 𝘢𝘭𝘴𝘰 𝘺𝘰𝘶 𝘤𝘢𝘯 𝘥𝘰𝘸𝘯𝘭𝘰𝘢𝘥 𝘢𝘯𝘥 𝘚𝘢𝘷𝘦 𝘪𝘯 𝘎𝘢𝘭𝘭𝘦𝘳𝘺 𝘋𝘰 𝘍𝘢𝘴𝘵 𝘧𝘰𝘳 𝘵𝘩𝘢𝘁 𝘺𝘰𝘶 𝘩𝘢𝘷𝘦 𝘰𝘯𝘭𝘺 3 𝘋𝘢𝘺𝘀.</b>\n\n"
                                 f"<b>🥺 𝐌𝐞𝐧𝐞 𝐬𝐮𝐧𝐚 𝐡𝐚𝐢 𝐭𝐮 𝐡𝐚𝐦𝐚𝐫𝐢 𝐰𝐞𝐛𝐬𝐢𝐭𝐞 𝐬𝐞 𝐋𝐞𝐜𝐭𝐮𝐫𝐞 𝐝𝐞𝐤𝐡𝐭𝐚 𝐡𝐚𝐢 𝐩𝐚𝐫 𝐖𝐞𝐛𝐬𝐢𝐭𝐞 𝐚𝐩𝐧𝐞 𝐝𝐨𝐬𝐭𝐨 𝐤𝐞 𝐬𝐚𝐭𝐡 𝐬𝐡𝐚𝐫𝐞 𝐧𝐚𝐡𝐢 𝐤𝐚𝐫𝐭𝐚 😔 𝐆𝐚𝐥𝐚𝐭 𝐛𝐚𝐚𝐭 𝐡𝐚𝐢 𝐧𝐚 𝐛𝐡𝐚𝐢 𝐜𝐡𝐚𝐥 𝐚𝐛 𝐤𝐚𝐫𝐝𝐞 𝐒𝐡𝐚𝐫𝐞 ❣️</b>\n\n"
                                 f"<b>ʙᴜᴛ ᴅᴏɴ'ᴛ ᴡᴏʀʀʏ 😁 ᴀғᴛᴇʀ ᴅᴇʟᴇᴛᴇᴅ ʏᴏᴜ ᴄᴀɴ ᴀɢᴀɪɴ ᴀᴄᴄᴇss ᴛʜʀᴏᴜɢʜ ᴏᴜʀ ᴡᴇʙsɪᴛᴇs 😘</b>\n\n"
                                 f"<b> <a href=https://yashyasag.github.io/hiddens_officials>🌟 𝗢𝗧𝗛𝗘𝗥 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦 🌟</a></b>",
                        )
                        
                        codeflix_msgs.append(k)
                        # Schedule auto-deletion for individual message
                        asyncio.create_task(delete_files(codeflix_msgs, client, message, k, INDIVIDUAL_DELETE_TIME))
                        return
                    except Exception as e:
                        print(f"Error in HACKHEIST parsing: {e}")
                        await message.reply_text(f"Invalid HACKHEIST link format: {str(e)}")
                        return
                else:
                    await message.reply_text("Invalid HACKHEIST link structure")
                    return
        except Exception as e:
            print(f"Error decoding HACKHEIST link: {e}")
            # Fall through to batch processing if HACKHEIST fails

        # Batch message handling
        try:
            string = await decode(base64_string)
            print(f"Decoded batch string: {string}")
            argument = string.split("-")

            # Handle channel_id (may include negative sign)
            if len(argument) == 5 and argument[1] == "":
                channel_id = int(f"-{argument[2]}")
                f_msg_id = int(argument[3])
                s_msg_id = int(argument[4])
                print(f"Negative channel ID format - channel_id: {channel_id}, f_msg_id: {f_msg_id}, s_msg_id: {s_msg_id}")
                if f_msg_id <= s_msg_id:
                    ids = list(range(f_msg_id, s_msg_id + 1))
                else:
                    ids = list(range(f_msg_id, s_msg_id - 1, -1))
            elif len(argument) == 4 and argument[1] != "":
                channel_id = int(argument[1])
                f_msg_id = int(argument[2])
                s_msg_id = int(argument[3])
                print(f"Positive channel ID format - channel_id: {channel_id}, f_msg_id: {f_msg_id}, s_msg_id: {s_msg_id}")
                if f_msg_id <= s_msg_id:
                    ids = list(range(f_msg_id, s_msg_id + 1))
                else:
                    ids = list(range(f_msg_id, s_msg_id - 1, -1))
            elif len(argument) == 4 and argument[1] == "":
                channel_id = int(f"-{argument[2]}")
                f_msg_id = int(argument[3])
                print(f"Single negative ID format - channel_id: {channel_id}, f_msg_id: {f_msg_id}")
                ids = [f_msg_id]
            elif len(argument) == 3 and argument[1] != "":
                channel_id = int(argument[1])
                f_msg_id = int(argument[2])
                print(f"Single positive ID format - channel_id: {channel_id}, f_msg_id: {f_msg_id}")
                ids = [f_msg_id]
            else:
                await message.reply_text("Invalid format structure: Incorrect number of arguments")
                return
        except (ValueError, IndexError) as e:
            print(f"Error decoding batch link: {e}")
            await message.reply_text(f"Error parsing format: {str(e)}")
            return

        temp_msg = await message.reply("𝗥𝘂𝗸 𝗘𝗸 𝗦𝗲𝗰 👽..")
        try:
            messages = await get_messages(client, ids, channel_id)
            print(f"Fetched {len(messages)} messages for channel_id={channel_id}, ids={ids}")
            if not messages or all(msg is None for msg in messages):
                await temp_msg.edit("Failed to fetch messages. They may have been deleted or are inaccessible.")
                return
        except Exception as e:
            await temp_msg.edit(f"Something went wrong: {str(e)}")
            print(f"Error getting messages from {channel_id}: {e}")
            return
        finally:
            await temp_msg.delete()

        codeflix_msgs = []
        user_id = message.from_user.id
        
        for msg in messages:
            if not msg:
                continue
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

            # Generate caption
            caption = (
                CUSTOM_CAPTION.format(
                    previouscaption=(msg.caption.html if msg.caption else "🔥 𝐇𝐈𝐃𝐃𝐄𝐍𝐒 🔥"),
                    filename=filename,
                    mediatype=media_type,
                )
                if bool(CUSTOM_CAPTION)
                else (msg.caption.html if msg.caption else "")
            )

            # Create individual access button
            base64_string2 = await encode_new(f"HACKHEIST-{user_id}-{msg.id}-{channel_id}")
            individual_button = InlineKeyboardButton("😁 𝗖𝗟𝗜𝗖𝗞 𝗧𝗢 𝗦𝗔𝗩𝗘 📥", url=f"https://t.me/{client.username}?start={base64_string2}")

            # Handle reply_markup
            if DISABLE_CHANNEL_BUTTON:
                reply_markup = None
            elif msg.reply_markup:
                if msg.reply_markup.inline_keyboard:
                    new_keyboard = msg.reply_markup.inline_keyboard.copy()
                    new_keyboard.append([individual_button])
                    reply_markup = InlineKeyboardMarkup(new_keyboard)
                else:
                    reply_markup = InlineKeyboardMarkup([[individual_button]])
            else:
                reply_markup = InlineKeyboardMarkup([[individual_button]])

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
                except Exception as e:
                    print(f"Failed to send message after waiting: {e}")
            except Exception as e:
                print(f"Failed to send message: {e}")

        # Notify user about auto-deletion
        k = await client.send_message(
            chat_id=message.from_user.id,
            text=f"<b>‼️ 𝐓𝐡𝐞𝐬𝐞 𝐋𝐄𝐂𝐓𝐔𝐑𝐄𝐒/𝐏𝐃𝐅𝐬 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐜 𝐃𝐞𝐥𝐞𝐭𝐢𝐧𝐠 𝐢𝐧 𝟰 �_H𝗼𝘂𝗿𝘀 🔥</b>\n\n"
                 f"<b>𝘚𝘰 𝘍𝘰𝘳 𝘚𝘢𝘷𝘪𝘯𝘨 𝘓𝘦𝘤𝘵𝘶𝘳𝘦/𝘗𝘥𝘧 𝘤𝘭𝘪𝘤𝘬 𝘰𝘯 𝘣𝘦𝘭𝘰𝘸 𝘣𝘶𝘁𝘵𝘰𝘯(😁 𝗖𝗟𝗜𝗖𝗞 𝗧𝗢 𝗦𝗔𝗩𝗘 📥) 𝘰𝘧 𝘸𝘩𝘪𝘤𝘩 𝘓𝘦𝘤𝘵𝘶𝘳𝘦/𝘗𝘥𝘧 𝘺𝘰𝘶 𝘸𝘢𝘯𝘵 𝘵𝘰 𝘴𝘢𝘷𝘦 𝘣𝘺 𝘵𝘩𝘪𝘴 𝘵𝘩𝘢𝘵 𝘭𝘦𝘤𝘵𝘶𝘳𝘦/𝘗𝘥𝘧 𝘠𝘰𝘶 𝘤𝘢𝘯 𝘚𝘢𝘷𝘦 𝘪𝘯 𝘎𝘢𝘭𝘭𝘦𝘳𝘺 😊</b>\n\n"
                 f"<b>ʙᴜᴛ ᴅᴏɴ'ᴛ ᴡᴏʀʀʏ 😁 ᴀғᴛᴇʀ ᴅᴇʟᴇᴛᴇᴅ ʏᴏᴜ ᴄᴀɴ ᴀɢᴀɪɴ ᴀᴄᴄᴇss ᴛʜʀᴏᴜɢʜ ᴏᴜʀ ᴡᴇʙsɪᴛᴇs 😘</b>\n\n"
                 f"<b> <a href=https://yashyasag.github.io/hiddens_officials>🌟 𝗢𝗧𝗛𝗘𝗥 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦 🌟</a></b>",
        )

        codeflix_msgs.append(k)
        asyncio.create_task(delete_files(codeflix_msgs, client, message, k, BULK_DELETE_TIME))
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
            InlineKeyboardButton(text="🌟 𝗝𝗼𝗶𝗻 𝟭𝘀𝘁 🌟", url=client.invitelink),
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

    try:
        seconds = int(message.text.split(maxsplit=1)[1])
    except (IndexError, ValueError):
        seconds = None

    query = await full_userbase()
    broadcast_msg = message.reply_to_message
    total = 0
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0
    sent_messages = []

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

    if seconds:
        await asyncio.sleep(seconds)
        for chat_id, msg_id in sent_messages:
            try:
                await client.delete_messages(chat_id, msg_id)
            except:
                pass

async def delete_files(codeflix_msgs, client, message, k, delete_time=None):
    if delete_time is None:
        delete_time = FILE_AUTO_DELETE
    
    await asyncio.sleep(delete_time)
    
    for msg in codeflix_msgs:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            print(f"The attempt to delete the media {msg.id} was unsuccessful: {e}")
