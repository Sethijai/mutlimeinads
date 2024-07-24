#(©)Codeflix-Bots

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>○ Developer: <a href='http://t.me/Hidden_contact_bot'>HIDDEN</a>\n○ ᴍʏ ᴜᴘᴅᴀᴛᴇs : <a href='https://t.me/HIDDEN_OFFICIALS'>ᴛᴇᴀᴍ ʜɪᴅᴅᴇɴ</a></b>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
    
    [
                    InlineKeyboardButton("👻 ABOUT", callback_data = "about"),
                    InlineKeyboardButton('🍁 MAIN CHANNEL', url='https://t.me/HIDDEN_OFFICIALS')
        
    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
