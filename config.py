#(©)CodeXBotz
#By @Codeflix_Bots



import os
import logging
from logging.handlers import RotatingFileHandler



#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "29626867"))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "82b19751497d00e47c3032409d130423")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "0"))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

#Port
PORT = os.environ.get("PORT", "8080")

#Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://namanjain123eudhc:opmaster@cluster0.5iokvxo.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

#force sub channel id, if you want enable force sub
FORCESUB_CHANNEL = int(os.environ.get("FORCESUB_CHANNEL", ""))
FORCESUB_CHANNEL2 = int(os.environ.get("FORCESUB_CHANNEL2", ""))
FORCESUB_CHANNEL3 = int(os.environ.get("FORCESUB_CHANNEL3", ""))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

#start message
START_MSG = os.environ.get("START_MESSAGE", "<b>ʜᴇʟʟᴏ 🥰 {first}\n\n ɪ ᴀᴍ ᴍᴀᴛᴇʀɪᴀʟ ᴘʀᴏᴠɪᴅᴇʀ ʙᴏᴛ , ɪ ᴀᴍ ᴘʀᴏᴠɪᴅɪɴɢ ʏᴏᴜ ᴍᴀᴛᴇʀɪᴀʟ ᴡʜɪᴄʜ ʜᴇʟᴘs ʏᴏᴜ ɪɴ ʏᴏᴜʀ ᴘʀᴇᴘᴀʀᴛɪᴏɴ 🤩 » @opmaster_provides</b>")
try:
    ADMINS=[6376328008]
    for x in (os.environ.get("ADMINS", "5115691197 6273945163 6103092779 2005714953 5231212075 6497757690").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "𝐒𝐨𝐫𝐫𝐲 {first} 𝐁𝐫𝐨/𝐒𝐢𝐬 𝐲𝐨𝐮 𝐡𝐚𝐯𝐞 𝐭𝐨 𝐣𝐨𝐢𝐧 𝐦𝐲 𝐜𝐡𝐚𝐧𝐧𝐞𝐥𝐬 𝐟𝐢𝐫𝐬𝐭 𝐭𝐨 𝐚𝐜𝐜𝐞𝐬𝐬 𝐌𝐚𝐭𝐞𝐫𝐢𝐚𝐥 \n\n ☠️𝗜 𝗵𝗮𝘃𝗲 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗲𝘀𝗲 𝗰𝗵𝗮𝗻𝗻𝗲𝗹𝘀 𝗶𝗻 𝘄𝗵𝗶𝗰𝗵 𝘄𝗲 𝗮𝗹𝘄𝗮𝘆𝘀 𝘀𝘁𝗮𝘆 𝗮𝘄𝗮𝘆 𝗳𝗿𝗼𝗺 𝗰𝗼𝗽𝘆𝗿𝗶𝗴𝗵𝘁 🙏 \n\n𝐒𝐨 𝐩𝐥𝐞𝐚𝐬𝐞 𝐣𝐨𝐢𝐧 𝐦𝐲 𝐜𝐡𝐚𝐧𝐧𝐞𝐥𝐬 𝐟𝐢𝐫𝐬𝐭 𝐚𝐧𝐝 𝐜𝐥𝐢𝐜𝐤 𝐨𝐧 “𝐍𝐨𝐰 𝐂𝐥𝐢𝐜𝐤 𝐡𝐞𝐫𝐞” 𝐛𝐮𝐭𝐭𝐨𝐧....!")
#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "")

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "ᴍʏ ᴅᴇᴀʀ ғʀɪᴇɴᴅ , ʏᴏᴜ ᴄᴀɴ'ᴛ ɢɪᴠᴇ ᴍᴇ ᴀɴʏ ᴍᴇssᴀɢᴇ ᴏʀ ᴄᴏᴍᴍᴀɴᴅ ɪ ᴀᴍ ᴏɴʟʏ ᴀᴄᴄᴇssᴀʙʟᴇ ғᴏʀ ᴍᴀᴛᴇʀɪᴀʟ\n\n» ᴀɴʏ ᴘʀᴏʙʟᴇᴍ :- Solve yourself bcz i don't have a time for that"

ADMINS.append(OWNER_ID)
ADMINS.append(6497757690)

LOG_FILE_NAME = "codeflixbots.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
