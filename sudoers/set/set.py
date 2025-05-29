#Copyright @ISmartDevs
#Channel t.me/TheSmartDev

from pyrogram import filters
from pyrogram.types import BotCommand
from pyrogram.enums import ParseMode
from config import OWNER_ID
from utils import LOGGER

BOT_COMMANDS = [
    BotCommand("start", "みStart SecureXTools Bot↯"),
    BotCommand("help", "みGet Help Menu & Commands↯"),
    BotCommand("info", "みGet User Info From Database↯"),
    BotCommand("id", "みGet Group Or Channel Info↯"),
    BotCommand("ip", "みGet Any Ip Information↯"),
    BotCommand("px", "みCheck Proxy Any Type↯"),
    BotCommand("ss", "みGet SS Of Any Website↯"),
    BotCommand("fb", "みDownload Facebook Video↯"),
    BotCommand("in", "みDownload Insta Reel & Posts↯"),
    BotCommand("sp", "みDownload Spotify Track↯"),
    BotCommand("song", "みDownload Yt Music↯"),
    BotCommand("video", "みDownload Yt Video↯"),
    BotCommand("tt", "みDownload TikTok Video↯"),
    BotCommand("pnt", "みDownload Pinterest Video↯"),
    BotCommand("settings", "みChange Bot All Vars [Admin]↯"),
    BotCommand("auth", "みPromote Sudo User  [Admin]↯"),
    BotCommand("unauth", "みDemote Sudo User  [Admin]↯"),
    BotCommand("gban", "みBan User From Using Bot [Admin]↯"),
    BotCommand("gunban", "みUnban User From Using Bot [Admin]↯"),
    BotCommand("logs", "みGet Bot's Logs From Console [Admin]↯"),
    BotCommand("restart", "みRestart Bot And Freshly Start [Admin]↯"),
    BotCommand("speedtest", "みGet Bot Server Speed [Admin]↯"),
    BotCommand("send", "みSend Brodcast [Admin]↯"),
    BotCommand("stats", "みGet Statistics [Admin]↯"),
]

def setup_set_commands_handler(app):
    @app.on_message(filters.command("set") & filters.user(OWNER_ID))
    async def set_commands(client, message):
        await client.set_bot_commands(BOT_COMMANDS)
        await client.send_message(
            chat_id=message.chat.id,
            text="み  ¡**BotFather Commands Successfully Set**↯",
            parse_mode=ParseMode.MARKDOWN
        )
        LOGGER.info(f"BotFather commands set by owner {message.from_user.id}")