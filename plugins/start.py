import random
import os, asyncio, humanize
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import *
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user

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
        
        ids = []
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))  # Subtract 1 to send one less message
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

        temp_msg = await message.reply("Wait A Sec..")
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


    # Generate caption
            caption = (
                CUSTOM_CAPTION.format(
                    previouscaption=(msg.caption.html if msg.caption else "No caption"),
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


        # List of multiple special message IDs
        special_msg_ids = [44219, 44224, 44225, 44226, 44227, 44228, 44229, 44230, 44231, 44232, 44234, 44235, 44237, 44238, 44240, 44242, 44243, 44244, 44245, 44247, 44248, 44249, 44250, 44251, 44253, 44254, 44255, 44256, 44257, 44258, 44259, 44260, 44261, 44262, 44263, 44264, 44265, 44266, 44267, 44268]  # Replace with actual message IDs

# Select a random message ID from the list
        random_msg_id = random.choice(special_msg_ids)

        try:
            special_msg = await client.get_messages(client.db_channel.id, random_msg_id)

            if not special_msg:
                await client.send_message(chat_id=message.from_user.id, text="⚠️ Special message not found!")
            else:
                if special_msg.sticker:
                    special_copied_msg = await client.send_sticker(
                        chat_id=message.from_user.id,
                        sticker=special_msg.sticker.file_id
                    )
                else:
                    await client.send_message(chat_id=message.from_user.id, text="⚠️ Unsupported message type!")
        except Exception as e:
            await client.send_message(chat_id=message.from_user.id, text=f"Error: {str(e)}")
            print(f"Failed to fetch special message: {e}")
        # Notify user about auto-deletion
        k = await client.send_message(
            chat_id=message.from_user.id,
            text=f"<b>𝗕𝘂𝗱𝗱𝘆 𝘆𝗼𝘂𝗿 𝗿𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗺𝗮𝘁𝗲𝗿𝗶𝗮𝗹 𝗴𝗼𝗻𝗲 𝗱𝗲𝗹𝗲𝘁𝗲 😕 𝗶𝗻 {file_auto_delete}</b>\n\n"
                 f"<b>But Don,t worry 🥰 you again access through my websites 🌟</b>\n\n"
                 f"<b>𝗔𝗹𝗹 𝗖𝗿𝗲𝗱𝗶𝘁𝘀 𝗳𝗼𝗿 𝘁𝗵𝗶𝘀 𝗺𝗮𝘁𝗲𝗿𝗶𝗮𝗹 𝗴𝗼𝗲𝘀 𝘁𝗼 ℍ𝔸ℂ𝕂ℍ𝔼𝕀𝕊𝕋 😈</b>",
        )

        # Include notification message in the deletion list
        codeflix_msgs.append(k)

        
        # Schedule auto-deletion
        asyncio.create_task(delete_files(codeflix_msgs, client, special_copied_msg, message, k, random_msg_id))
        return

    else:
        reply_markup = InlineKeyboardMarkup(
            [[
            InlineKeyboardButton("𝗠𝗔𝗜𝗡 𝗪𝗘𝗕𝗦𝗜𝗧𝗘 😁", url="https://t.me/HIDDEN_OFFICIALS_5/3")
            ],[
            InlineKeyboardButton("𝐀𝐏𝐍𝐈 𝐊𝐀𝐊𝐒𝐇𝐀 𝗪𝗘𝗕𝗦𝗜𝗧𝗘 😱", url="https://yashyasag.github.io/tesetoss")
            ],[
            InlineKeyboardButton("MIT SCHOOL 😁", url="https://mits-ak.github.io/mitbyhh/")
            ]]
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

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="1st Channel", url=client.invitelink),
            InlineKeyboardButton(text="2nd Channel", url=client.invitelink2),
        ],
        [
            InlineKeyboardButton(text="3rd channel", url=client.invitelink3),
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='ʀᴇʟᴏᴀᴅ',
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
            except Exception as e:
                print(f"Failed to send message to {chat_id}: {e}")
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u></b>

<b>Total Users :</b> <code>{total}</code>
<b>Successful :</b> <code>{successful}</code>
<b>Blocked Users :</b> <code>{blocked}</code>
<b>Deleted Accounts :</b> <code>{deleted}</code>
<b>Unsuccessful :</b> <code>{unsuccessful}</code>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(f"Use This Command As A Reply To Any Telegram Message Without Any Spaces.")
        await asyncio.sleep(8)
        await msg.delete()

# Function to handle file deletion
async def delete_files(codeflix_msgs, client, special_copied_msg, message, k, random_msg_id):
    await asyncio.sleep(FILE_AUTO_DELETE)  # Wait for the duration specified in config.py
    
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            print(f"The attempt to delete the media {msg.id} was unsuccessful: {e}")

    # Safeguard against k.command being None or having insufficient parts
    command_part = k.command[1] if k.command and len(k.command) > 1 else None

    if command_part:
        button_url = f"https://t.me/{client.username}?start={command_part}"
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!", url=button_url)]
            ]
        )
    else:
        keyboard = None

    # Edit message with the button
    await k.edit_text("<b><i>Your Video / File Is Successfully Deleted ✅</i></b>", reply_markup=keyboard)
