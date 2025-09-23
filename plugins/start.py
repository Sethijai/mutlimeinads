# start.py
import random
import os
import asyncio
import humanize
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, ChannelInvalid, PeerIdInvalid
from bot import Bot
from config import *
from helper_func import subscribed, encode_link, decode_link, get_messages
from database.database import add_user, del_user, full_userbase, present_user, add_random_message, remove_random_message, get_all_random_messages

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

        try:
            link_type, user_id, f_msg_id, channel_id, s_msg_id = await decode_link(base64_string)
            print(f"Decoded link: type={link_type}, user_id={user_id}, f_msg_id={f_msg_id}, channel_id={channel_id}, s_msg_id={s_msg_id}")
        except ValueError as e:
            await message.reply_text(f"❌ Invalid link format: {str(e)}")
            return
        except Exception as e:
            await message.reply_text(f"❌ Error decoding link: {str(e)}")
            return

        if link_type == "HACKHEIST":
            if message.from_user.id != user_id:
                await message.reply_text("❌ You are not authorized to access this content!")
                return
            
            temp_msg = await message.reply("𝗥𝘂𝗸 𝗘𝗸 𝗦𝗲𝗰 👽..")
            try:
                messages = await get_messages(client, [f_msg_id], channel_id)
                if not messages or all(msg is None for msg in messages):
                    await temp_msg.edit("Failed to fetch message. It may have been deleted or is inaccessible.")
                    return
            except Exception as e:
                await temp_msg.edit(f"Something went wrong: {str(e)}")
                print(f"Error getting message {f_msg_id} from {channel_id}: {e}")
                return
            finally:
                await temp_msg.delete()

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
            
            # Send random message after main content
            random_messages = await get_all_random_messages()
            if random_messages:
                channel_id, msg_id = random.choice(random_messages)
                try:
                    random_msg = (await get_messages(client, [msg_id], channel_id))[0]
                    if random_msg:
                        copied_random = await random_msg.copy(
                            chat_id=message.from_user.id,
                            protect_content=False
                        )
                        codeflix_msgs.append(copied_random)
                except Exception as e:
                    print(f"Failed to send random message: {e}")

            # Send deletion notification
            k = await client.send_message(
                chat_id=message.from_user.id,
                text=f"<b>‼️ 𝐓𝐡𝐢𝐬 𝐋𝐄𝐂𝐓𝐔𝐑𝐄/𝐏𝐃𝐅 𝐰𝐢𝐥𝐥 𝐛𝐞 <u>𝗮𝘂𝘁𝗼-𝗱𝗲𝗹𝗲𝘁𝗲𝗱 𝗶𝗻 𝟯 𝗱𝗮𝘆𝘀</u> 💀</b>\n\n"
                     f"<b>⚡ Watch Lecture now ✅ or Save it - Forward, Download & Keep in your Gallery before time runs out!</b>\n\n"
                     f"<b>🤝 Don’t forget—share with friends, knowledge grows when shared ❣️</b>\n\n"
                     f"<b>😎 Chill! Even after deletion, you can always re-access everything on our websites 😉</b>\n\n"
                     f"<b><a href='https://yashyasag.github.io/hiddens_officials'>✨ 𝗘𝘅𝗽𝗹𝗼𝗿𝗲 𝗠𝗼𝗿𝗲 𝗪𝗲𝗯𝘀𝗶𝘁𝗲𝘀 ✨</a></b>",
            )
            
            codeflix_msgs.append(k)
            asyncio.create_task(delete_files(codeflix_msgs, client, message, k, INDIVIDUAL_DELETE_TIME))
            return

        elif link_type == "batch":
            if s_msg_id is not None:
                if f_msg_id <= s_msg_id:
                    ids = list(range(f_msg_id, s_msg_id + 1))
                else:
                    ids = list(range(f_msg_id, s_msg_id - 1, -1))
            else:
                ids = [f_msg_id]

            temp_msg = await message.reply("𝗥𝘂𝗸 𝗘𝗸 𝗦𝗲𝗰 👽..")
            try:
                messages = await get_messages(client, ids, channel_id)
                print(f"Fetched {len(messages)} messages for channel_id={channel_id}, ids={ids}")
                if not messages or all(msg is None for msg in messages):
                    await temp_msg.edit("Failed to fetch messages. They may have been deleted or is inaccessible.")
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

                caption = (
                    CUSTOM_CAPTION.format(
                        previouscaption=(msg.caption.html if msg.caption else "🔥 𝐇𝐈𝐃𝐃𝐄𝐍𝐒 🔥"),
                        filename=filename,
                        mediatype=media_type,
                    )
                    if bool(CUSTOM_CAPTION)
                    else (msg.caption.html if msg.caption else "")
                )

                base64_string2 = await encode_link(user_id=user_id, f_msg_id=msg.id, channel_id=channel_id)
                individual_button = InlineKeyboardButton("😁 𝗖𝗟𝗜𝗖𝗞 𝗧𝗢 𝗦𝗔𝗩𝗘 📥", url=f"https://t.me/{client.username}?start={base64_string2}")

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

            # Send random message after main content
            random_messages = await get_all_random_messages()
            if random_messages:
                channel_id, msg_id = random.choice(random_messages)
                try:
                    random_msg = (await get_messages(client, [msg_id], channel_id))[0]
                    if random_msg:
                        copied_random = await random_msg.copy(
                            chat_id=message.from_user.id,
                            protect_content=PROTECT_CONTENT
                        )
                        codeflix_msgs.append(copied_random)
                except Exception as e:
                    print(f"Failed to send random message: {e}")

            # Send deletion notification
            k = await client.send_message(
                chat_id=message.from_user.id,
                text=f"<b>🔥 Hurry! These Lectures/PDFs will be <u>deleted automatically in 4 hours</u> ⏳</b>\n\n"
                     f"<b>𝘚𝘰 𝘍𝘰𝘳 𝘚𝘢𝘷𝘪𝘯𝘨 𝘓𝘦𝘤𝘵𝘶𝘳𝘦/𝘗𝘥𝘧 𝘤𝘭𝘪𝘤𝘬 𝘰𝘯 𝘣𝘦𝘭𝘰𝘸 𝘣𝘶𝘵𝘵𝘰𝘯(😁 𝗖𝗟𝗜𝗖𝗞 𝗧𝗢 𝗦𝗔𝗩𝗘 📥) then 𝘠𝘰𝘶 𝘤𝘢𝘯 𝘚𝘢𝘷𝘦 𝘪𝘯 𝘎𝘢𝘭𝘭𝘦𝘳𝘺 😊</b>\n\n"
                     f"<b>😎 Don’t worry! Even after deletion, you can still re-access everything anytime through our websites 😘</b>\n\n"
                     f"<b> <a href=https://yashyasag.github.io/hiddens_officials>🌟 𝗩𝗶𝘀𝗶𝘁 �_M𝗼𝗿𝗲 𝗪𝗲𝗯𝘀𝗶𝘁𝗲𝘀 🌟</a></b>",
            )

            codeflix_msgs.append(k)
            asyncio.create_task(delete_files(codeflix_msgs, client, message, k, BULK_DELETE_TIME))
            return

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
    msg = await client.send_message(chat_id=message.chat.id, text="Processing...")
    users = await full_userbase()
    await msg.edit(f"{len(users)} Users Are Using This Bot")

@Bot.on_message(filters.command('broadcast') & filters.private & filters.user(ADMINS))
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

    pls_wait = await message.reply("<i>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴘʀᴏᴄᴇꜱꜱɪɴɢ ᴛɪʟʟ ᴡᴀɪᴛ ʙʀᴏᴏ...</i>")

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

@Bot.on_message(filters.command('add_random_message') & filters.private & filters.user(ADMINS))
async def add_random_message(client: Bot, message: Message):
    try:
        # Extract message link
        link = message.text.split(maxsplit=1)[1]
        if not link.startswith("https://t.me/c/"):
            await message.reply("❌ Please provide a valid Telegram message link (https://t.me/c/...)")
            return
        
        # Parse link: https://t.me/c/2493255368/46223
        parts = link.split('/')
        if len(parts) < 6:
            await message.reply("❌ Invalid link format. Expected: https://t.me/c/channel_id/message_id")
            return
        channel_id = parts[4]
        msg_id = int(parts[5])

        # Validate message existence (optional, skip in offline mode)
        try:
            messages = await get_messages(client, [msg_id], channel_id)
            if not messages or messages[0] is None:
                await message.reply(f"❌ Message {msg_id} in channel {channel_id} is inaccessible or does not exist")
                return
        except (ChannelInvalid, PeerIdInvalid):
            await message.reply(f"❌ Invalid channel ID: {channel_id}. Ensure the bot has access to the channel.")
            return
        except Exception as e:
            await message.reply(f"❌ Failed to validate message: {str(e)}. Adding anyway (offline mode).")
            # Proceed to add even if validation fails (offline scenario)

        # Add to database
        await add_random_message(channel_id, msg_id)
        await message.reply(f"✅ Added message {link} to random messages")
    except IndexError:
        await message.reply("❌ Please provide a message link after the command")
    except ValueError:
        await message.reply("❌ Invalid message ID in the link")
    except Exception as e:
        await message.reply(f"❌ Error adding message: {str(e)}")

@Bot.on_message(filters.command('remove_random_message') & filters.private & filters.user(ADMINS))
async def remove_random_message(client: Bot, message: Message):
    try:
        # Extract message link
        link = message.text.split(maxsplit=1)[1]
        if not link.startswith("https://t.me/c/"):
            await message.reply("❌ Please provide a valid Telegram message link (https://t.me/c/...)")
            return
        
        # Parse link: https://t.me/c/2493255368/46223
        parts = link.split('/')
        if len(parts) < 6:
            await message.reply("❌ Invalid link format. Expected: https://t.me/c/channel_id/message_id")
            return
        channel_id = parts[4]
        msg_id = int(parts[5])
        
        await remove_random_message(channel_id, msg_id)
        await message.reply(f"✅ Removed message {link} from random messages")
    except IndexError:
        await message.reply("❌ Please provide a message link after the command")
    except ValueError:
        await message.reply("❌ Invalid message ID in the link")
    except Exception as e:
        await message.reply(f"❌ Error removing message: {str(e)}")

async def delete_files(codeflix_msgs, client, message, k, delete_time=None):
    if delete_time is None:
        delete_time = FILE_AUTO_DELETE
    
    await asyncio.sleep(delete_time)
    
    for msg in codeflix_msgs:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            print(f"The attempt to delete the media {msg.id} was unsuccessful: {e}")
