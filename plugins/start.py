import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
import time
from bot import Bot
from config import *
from helper_func import *
from database.database import *




@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
            # Handle WEBSITE_URL_MODE HACKHEIST parameter
            if base64_string.startswith("HACKHEIST="):
                base64_string = base64_string.split("HACKHEIST=", 1)[1]
            await message.reply_text(f"Processing link with base64: {base64_string}")
        except IndexError:
            await message.reply_text("Welcome to the bot!")
            return
        
        # Try decoding the string
        is_new_format = False
        try:
            string = await decode(base64_string)
            await message.reply_text(f"Decoded string: {string}")
            
            # Check for new format: get-HACKHEIST_{f_encoded}-{s_encoded}
            if string.startswith("get-HACKHEIST-"):
                is_new_format = True
                # Check premium status
                is_premium, remaining_time = await is_premium_user(id)
                current_time = int(time.time())
                if is_premium:
                    await message.reply_text("𝐘𝐨𝐮 𝐚𝐫𝐞 𝐚 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐔𝐬𝐞𝐫 🥰")
                else:
                    # Check if user was previously premium (has an expired entry)
                    user_doc = premium_users.find_one({'_id': id})
                    if user_doc and 'expiration_time' in user_doc and user_doc['expiration_time'] <= current_time:
                        await message.reply_text(f"ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴇxᴘɪʀᴇᴅ 🥲" 
                                                 f"𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐟𝐨𝐫 𝐛𝐮𝐲 𝐚𝐠𝐚𝐢𝐧 - ")
                    else:
                        await message.reply_text(f"<b>𝐘𝐨𝐮 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐚 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐮𝐬𝐞𝐫 🥺</b>"
                                                 f"Contact for buy")
                    return
                try:
                    f_msg_id, s_msg_id = await decode_link(base64_string)
                    await message.reply_text(f"New format decoded: {f_msg_id}, {s_msg_id}")
                    if f_msg_id <= s_msg_id:
                        ids = range(f_msg_id, s_msg_id + 1)
                    else:
                        ids = []
                        i = f_msg_id
                        while True:
                            ids.append(i)
                            i -= 1
                            if i < s_msg_id:
                                break
                except ValueError as e:
                    await message.reply_text(f"Error parsing new format: {str(e)}")
                    return
            else:
                # Process old format: get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}
                argument = string.split("-")
                if len(argument) == 3:
                    try:
                        start = int(int(argument[1]) / abs(client.db_channel.id))
                        end = int(int(argument[2]) / abs(client.db_channel.id))
                        await message.reply_text(f"Old format IDs: {start} to {end}")
                    except (ValueError, IndexError) as e:
                        await message.reply_text(f"Error parsing old format: {str(e)}")
                        return
                    if start <= end:
                        ids = range(start, end + 1)
                    else:
                        ids = []
                        i = start
                        while True:
                            ids.append(i)
                            i -= 1
                            if i < end:
                                break
                elif len(argument) == 2:
                    try:
                        ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                        await message.reply_text(f"Old format single ID: {ids[0]}")
                    except (ValueError, IndexError) as e:
                        await message.reply_text(f"Error parsing old format single ID: {str(e)}")
                        return
                else:
                    await message.reply_text("Invalid old format structure")
                    return
        except ValueError as e:
            await message.reply_text(f"Failed to decode string: {str(e)}")
            return

        temp_msg = await message.reply("Wait A Second...")
        try:
            messages = await get_messages(client, ids)
            await temp_msg.edit("Messages fetched successfully!")
        except Exception as e:
            await temp_msg.edit(f"Something went wrong: {str(e)}")
            return
        await temp_msg.delete()

        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                # Use protect_content=True for new format, PROTECT_CONTENT for old format
                protect_content = True if is_new_format else PROTECT_CONTENT
                await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=protect_content
                )
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=protect_content
                )
            except Exception as e:
                await message.reply_text(f"Error copying message: {str(e)}")
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗔𝗣𝗣𝗦 🥰', url='https://t.me/LCONETWORK'),
                    InlineKeyboardButton('🍁 𝐂𝐎𝐃𝐄𝐑𝐒𝐎𝐏', url='https://t.me/CODERSOP')
                ]
            ]
                )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return   


#=====================================================================================##

WAIT_MSG = """"<b>Processing ....</b>"""

REPLY_ERROR = """<code>Use this command as a reply to any telegram message with out any spaces.</code>"""

#=====================================================================================##

chat_data_cache = {}

        
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    temp = await message.reply("<b><i>Checking Subscription...</i></b>")

    user_id = message.from_user.id
    buttons = []
    count = 0

    try:
        all_channels = await db.show_channels()  # Should return list of (chat_id, mode) tuples
        for total, chat_id in enumerate(all_channels, start=1):
            mode = await db.get_channel_mode(chat_id)  # fetch mode 

            await message.reply_chat_action(ChatAction.TYPING)

            if not await is_sub(client, user_id, chat_id):
                try:
                    # Cache chat info
                    if chat_id in chat_data_cache:
                        data = chat_data_cache[chat_id]
                    else:
                        data = await client.get_chat(chat_id)
                        chat_data_cache[chat_id] = data

                    name = data.title

                    # Generate proper invite link based on the mode
                    if mode == "on" and not data.username:
                        invite = await client.create_chat_invite_link(
                            chat_id=chat_id,
                            creates_join_request=True,
                            expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                            )
                        link = invite.invite_link

                    else:
                        if data.username:
                            link = f"https://t.me/{data.username}"
                        else:
                            invite = await client.create_chat_invite_link(
                                chat_id=chat_id,
                                expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None)
                            link = invite.invite_link

                    buttons.append([InlineKeyboardButton(text=name, url=link)])
                    count += 1
                    await temp.edit(f"<b>{'! ' * count}</b>")

                except Exception as e:
                    print(f"Error with chat {chat_id}: {e}")
                    return await temp.edit(
                        f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @HACKHEISTBOT</i></b>\n"
                        f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
                    )

        # Retry Button
        try:
            buttons.append([
                InlineKeyboardButton(
                    text='♻️ Tʀʏ Aɢᴀɪɴ',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ])
        except IndexError:
            pass

        await message.reply_photo(
            photo=FORCE_PIC,
            caption=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    except Exception as e:
        print(f"Final Error: {e}")
        await temp.edit(
            f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @HACKHEISTBOT</i></b>\n"
            f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
        )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.command('addpremium') & filters.private & filters.user(ADMINS))
async def add_premium_command(client: Client, message: Message):
    try:
        args = message.text.split(" ", 2)[1:]
        if len(args) < 2:
            await message.reply_text("Usage: /addpremium {user_id} {time_in_seconds} or /addpremium All {time_in_seconds}")
            return
        
        time_seconds = int(args[1])
        if time_seconds <= 0:
            await message.reply_text("Time must be a positive number of seconds")
            return

        if args[0].lower() == "all":
            await add_all_premium(time_seconds)
            await message.reply_text(f"All users set as premium for {time_seconds} seconds")
        else:
            user_id = int(args[0])
            if not await present_user(user_id):
                await message.reply_text(f"User {user_id} not found in database")
                return
            await add_premium_user(user_id, time_seconds)
            await message.reply_text(f"User {user_id} set as premium for {time_seconds} seconds")
    except (IndexError, ValueError) as e:
        await message.reply_text(f"Error: {str(e)}. Usage: /addpremium {user_id} {time_in_seconds} or /addpremium All {time_in_seconds}")

@Bot.on_message(filters.command('removepremium') & filters.private & filters.user(ADMINS))
async def remove_premium_command(client: Client, message: Message):
    try:
        user_id = int(message.text.split(" ", 1)[1])
        await remove_premium_user(user_id)
        await message.reply_text(f"Premium status removed for user {user_id}")
    except (IndexError, ValueError) as e:
        await message.reply_text(f"Error: {str(e)}. Usage: /removepremium {user_id}")

@Bot.on_message(filters.command('listpremiumusers') & filters.private & filters.user(ADMINS))
async def list_premium_users_command(client: Client, message: Message):
    premium_list = await list_premium_users()
    if not premium_list:
        await message.reply_text("No premium users found")
        return
    
    response = "Premium Users:\n"
    for user_id, remaining_time in premium_list:
        if user_id == "All":
            response += f"All users: {remaining_time} seconds remaining\n"
        else:
            response += f"User {user_id}: {remaining_time} seconds remaining\n"
    await message.reply_text(response)
    
@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
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
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

