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
BULK_DELETE_TIME = FILE_AUTO_DELETE  # For bulk downloads
try:
    INDIVIDUAL_DELETE_TIME = INDIVIDUAL_AUTO_DELETE  # For individual access
except NameError:
    INDIVIDUAL_DELETE_TIME = FILE_AUTO_DELETE  # Fallback to bulk delete time if not defined

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

        # Check if it's a "HACKHEIST-" request for individual access
        try:
            string = await decode_new(base64_string)
            if string.startswith("HACKHEIST-"):
                argument = string.split("-")
                
                if len(argument) == 4 and argument[0] == "HACKHEIST":
                    try:
                        user_id = int(argument[1])
                        msg_id = int(argument[2])
                        modified_channel_id = argument[3]
                        # Reverse the *8 multiplication
                        channel_id_without_minus_100 = str(int(modified_channel_id.replace("-100", "")) // 8)
                        channel_id = f"-100{channel_id_without_minus_100}"  # Reconstruct CHANNEL_ID
                        
                        # Check if the current user is authorized
                        if message.from_user.id != user_id:
                            await message.reply_text("❌ You are not authorized to access this content!")
                            return
                        
                        temp_msg = await message.reply("𝗥𝘂𝗸 𝗘𝗸 𝗦𝗲𝗰 👽..")
                        try:
                            messages = await get_messages(client, [msg_id], channel_id)
                        except Exception as e:
                            await message.reply_text("Something Went Wrong..!")
                            print(f"Error getting messages: {e}")
                            return
                        finally:
                            await temp_msg.delete()

                        # Send the individual message with protect_content = False
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
                                    protect_content=False,  # Changed to False for individual access
                                )
                                
                                if copied_msg:
                                    codeflix_msgs.append(copied_msg)
                                    
                            except Exception as e:
                                print(f"Failed to send individual message: {e}")
                                await message.reply_text("Failed to send the content!")
                                return
                        
                        # Notify user about auto-deletion for individual message
                        k = await client.send_message(
                            chat_id=message.from_user.id,
                            text=f"<b>‼️ 𝐓𝐡𝐢𝐬 𝐋𝐄𝐂𝐓𝐔𝐑𝐄/𝐏𝐃𝐅 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐜 𝐃𝐞𝐥𝐞𝐭𝐢𝐧𝐠 𝐢𝐧 𝟯 𝗗𝗮𝘆𝘀 💀</b>\n\n"
                                 f"<b>🥰 𝘕𝘰𝘸 𝘺𝘰𝘶 𝘤𝘢𝘯 𝘍𝘰𝘳𝘸𝘢𝘳𝘥 𝘵𝘩𝘪𝘴 𝘓𝘦𝘤𝘵𝘶𝘳𝘦/𝘗𝘥𝘧 𝘢𝘯𝘥 𝘢𝘭𝘴𝘰 𝘺𝘰𝘶 𝘤𝘢𝘯 𝘥𝘰𝘸𝘯𝘭𝘰𝘢𝘥 𝘢𝘯𝘥 𝘚𝘢𝘷𝘦 𝘪𝘯 𝘎𝘢𝘭𝘭𝘦𝘳𝘺 𝘋𝘰 𝘍𝘢𝘴𝘁 𝘧𝘰𝘳 𝘵𝘩𝘢𝘵 𝘺𝘰𝘶 𝘩𝘢𝘷𝘦 𝘰𝘯𝘭𝘺 3 𝘋𝘢𝘺𝘀.</b>\n\n"
                                 f"<b>🥺 𝐌𝐞𝐧𝐞 𝐬𝐮𝐧𝐚 𝐡𝐚𝐢 𝐭𝐮 𝐡𝐚𝐦𝐚𝐫𝐢 𝐰𝐞𝐛𝐬𝐢𝐭𝐞 𝐬𝐞 𝐋𝐞𝐜𝐭𝐮𝐫𝐞 𝐝𝐞𝐤𝐡𝐭𝐚 𝐡𝐚𝐢 𝐩𝐚𝐫 𝐖𝐞𝐛𝐬𝐢𝐭𝐞 𝐚𝐩𝐧𝐞 𝐝𝐨𝐬𝐭𝐨 𝐤𝐞 𝐬𝐚𝐭𝐡 𝐬𝐡𝐚𝐫𝐞 𝐧𝐚𝐡𝐢 𝐤𝐚𝐫𝐭𝐚 😔 𝐆𝐚𝐥𝐚𝐭 𝐛𝐚𝐚𝐭 𝐡𝐚𝐢 𝐧𝐚 𝐛𝐡𝐚𝐢 𝐜𝐡𝐚𝐥 𝐚𝐛 𝐤𝐚𝐫𝐝𝐞 𝐒𝐡𝐚𝐫𝐞 ❣️</b>\n\n"
                                 f"<b>ʙᴜᴛ ᴅᴏɴ'ᴛ ᴡᴏʀʀʏ 😁 ᴀғᴛᴇʀ ᴅᴇʟᴇᴛᴇᴅ ʏᴏᴜ ᴄᴀɴ ᴀɢᴀɪɴ ᴀᴄᴄᴇss ᴛʜʀᴏᴜɢʜ ᴏᴜʀ ᴡᴇʙsɪᴛᴇs 😘</b>\n\n"
                                 f"<b> <a href=https://yashyasag.github.io/hiddens_officials>🌟 𝗢𝗧𝗛𝗘𝗥 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦 🌟</a></b>",
                        )
                        
                        codeflix_msgs.append(k)
                        # Schedule auto-deletion for individual message with individual delete time
                        asyncio.create_task(delete_files(codeflix_msgs, client, message, k, INDIVIDUAL_DELETE_TIME))
                        
                        return
                        
                    except Exception as e:
                        print(f"Error in individual access: {e}")
                        # Fall through to normal processing if individual access fails
                        pass
        except:
            # If decode_new fails, try normal decode for batch links
            pass

        # Batch message handling
        try:
            string = await decode(base64_string)
            if string.startswith("get-"):
                argument = string.split("-")
                
                if len(argument) == 4 and argument[0] == "get":
                    try:
                        f_msg_id = int(argument[1])
                        s_msg_id = int(argument[2])
                        modified_channel_id = argument[3]
                        # Reverse the *8 multiplication
                        channel_id_without_minus_100 = str(int(modified_channel_id.replace("-100", "")) // 8)
                        channel_id = f"-100{channel_id_without_minus_100}"  # Reconstruct CHANNEL_ID
                        
                        # Generate list of message IDs
                        ids = list(range(f_msg_id, s_msg_id + 1)) if f_msg_id <= s_msg_id else list(range(f_msg_id, s_msg_id - 1, -1))
                    except Exception as e:
                        print(f"Error decoding batch IDs: {e}")
                        await message.reply_text("Something Went Wrong..!")
                        return
                else:
                    await message.reply_text("❌ Invalid batch link format!")
                    return
            else:
                await message.reply_text("❌ Invalid link format!")
                return
        except Exception as e:
            print(f"Error decoding batch link: {e}")
            await message.reply_text("Something Went Wrong..!")
            return

        temp_msg = await message.reply("𝗥𝘂𝗸 𝗘𝗸 𝗦𝗲𝗰 👽..")
        try:
            messages = await get_messages(client, ids, channel_id)
        except Exception as e:
            await message.reply_text("Something Went Wrong..!")
            print(f"Error getting messages: {e}")
            return
        finally:
            await temp_msg.delete()

        codeflix_msgs = []
        user_id = message.from_user.id
        
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

            # Create individual access button using encode_new
            modified_channel_id = int(channel_id_without_minus_100) * 8  # Apply *8 for HACKHEIST link
            base64_string2 = await encode_new(f"HACKHEIST-{user_id}-{msg.id}--100{modified_channel_id}")
            individual_button = InlineKeyboardButton("😁 𝗖𝗟𝗜�_CK 𝗧𝗢 𝗦𝗔𝗩𝗘 📥", url=f"https://t.me/{client.username}?start={base64_string2}")

            # Handle reply_markup - add individual button to existing markup or create new one
            if DISABLE_CHANNEL_BUTTON:
                reply_markup = None
            elif msg.reply_markup:
                # Add the individual button to existing markup
                if msg.reply_markup.inline_keyboard:
                    new_keyboard = msg.reply_markup.inline_keyboard.copy()
                    new_keyboard.append([individual_button])
                    reply_markup = InlineKeyboardMarkup(new_keyboard)
                else:
                    reply_markup = InlineKeyboardMarkup([[individual_button]])
            else:
                # Create new markup with just the individual button
                reply_markup = InlineKeyboardMarkup([[individual_button]])

            try:
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT,
                )
                if copied_msg:  # Ensure the message was copied successfully
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
            text=f"<b>‼️ 𝐓𝐡𝐞𝐬𝐞 𝐋𝐄𝐂𝐓𝐔𝐑𝐄𝐒/𝐏𝐃𝐅𝐬 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐜 𝐃𝐞𝐥𝐞𝐭𝐢𝐧𝐠 𝐢𝐧 𝟰 𝗛𝗼𝘂𝗿𝘀 🔥</b>\n\n"
                 f"<b>𝘚𝘰 𝘍𝘰𝘳 𝘚𝘢𝘷𝘪𝘯𝘨 𝘓𝘦𝘤𝘵𝘶𝘳𝘦/𝘗𝘥𝘧 𝘤𝘭𝘪𝘤𝘬 𝘰𝘯 𝘣𝘦𝘭𝘰𝘸 𝘣𝘶𝘵𝘵𝘰𝘯(😁 𝗖𝗟𝗜𝗖𝗞 𝗧𝗢 𝗦𝗔𝗩𝗘 📥) 𝘰𝘧 𝘸𝘩𝘪𝘤𝘩 𝘓𝘦𝘤𝘵𝘶𝘳𝘦/𝘗𝘥𝘧 𝘺𝘰𝘶 𝘸𝘢𝘯𝘵 𝘵𝘰 𝘴𝘢𝘷𝘦 𝘣𝘺 𝘵𝘩𝘪𝘴 𝘵𝘩𝘢𝘵 𝘭𝘦𝘤𝘵𝘶𝘳𝘦/𝘗𝘥𝘧 𝘠𝘰𝘶 𝘤𝘢𝘯 𝘚𝘢𝘷𝘦 𝘪𝘯 𝘎𝘢𝘭𝘭𝘦𝘳𝘺 😊</b>\n\n"
                 f"<b>ʙᴜᴛ ᴅᴏɴ'ᴛ ᴡᴏʀʀʏ 😁 ᴀғᴛᴇʀ ᴅᴇʟᴇᴛᴇᴅ ʏᴏᴜ ᴄᴀɴ ᴀɢᴀɪɴ ᴀᴄᴄᴇss ᴛʜʀᴏᴜɢʜ ᴏᴜʀ ᴡᴇʙsɪᴛᴇs 😘</b>\n\n"
                 f"<b> <a href=https://yashyasag.github.io/hiddens_officials>🌟 𝗢𝗧𝗛𝗘𝗥 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦 🌟</a></b>",
        )

        # Include notification message in the deletion list
        codeflix_msgs.append(k)

        # Schedule auto-deletion with bulk delete time
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
async def delete_files(codeflix_msgs, client, message, k, delete_time=None):
    if delete_time is None:
        delete_time = FILE_AUTO_DELETE
    
    await asyncio.sleep(delete_time)  # Wait for the specified duration
    
    for msg in codeflix_msgs:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            print(f"The attempt to delete the media {msg.id} was unsuccessful: {e}")


