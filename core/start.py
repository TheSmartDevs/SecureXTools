#Copyright @ISmartDevs
#Channel t.me/TheSmartDev

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_USERNAME, OWNER_ID, UPDATE_CHANNEL_URL, COMMAND_PREFIX, BOT_NAME
from utils import LOGGER

def setup_start_handler(app):
    @app.on_message(filters.command(["start"], prefixes=COMMAND_PREFIX) & filters.private)
    async def start_command(client, message):
        LOGGER.info(f"Received /start command from user {message.from_user.id}")
        
        user = message.from_user
        full_name = (user.first_name or "") + (f" {user.last_name}" if user.last_name else "")
        full_name = full_name.strip() or "User"
        user_mention = f"[{full_name}](tg://user?id={user.id})"
        
        welcome_text = (
            f"**◑ ʜᴇʏ {user_mention}, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʙᴏᴛ**\n"
            f"**➻ ᴛʜɪs ɪs [{BOT_NAME}](t.me/{BOT_USERNAME.lstrip('@')}), ᴀ ғᴀsᴛ & ᴘᴏᴡᴇʀғᴜʟ ᴛᴏᴏʟᴋɪᴛ.**\n"
            "**━━━━━━━━━━━━━━━━━━━━━━**\n"
            "**Tᴏᴏʟs:** ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀ ɪɴғᴏ ᴄʜᴇᴄᴋᴇʀ, ɪᴘ ᴄʜᴇᴄᴋᴇʀ, ᴘʀᴏxʏ ᴄʜᴇᴄᴋᴇʀ, sᴄʀᴇᴇɴsʜᴏᴛ.\n\n"
            "**ᴅᴏᴡɴʟᴏᴀᴅ ᴘʟᴀᴛғᴏʀᴍs:** ʏᴏᴜᴛᴜʙᴇ, ғᴀᴄᴇʙᴏᴏᴋ, ɪɴsᴛᴀɢʀᴀᴍ, ᴘɪɴᴛᴇʀᴇsᴛ, sᴘᴏᴛɪғʏ, ᴛɪᴋᴛᴏᴋ."
        )
        
        buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("➕ Add Me", url=f"https://t.me/{BOT_USERNAME.lstrip('@')}?startgroup=true")],
                [
                    InlineKeyboardButton("🔧 Developer", user_id=OWNER_ID),
                    InlineKeyboardButton("✍🏻 Support", url=UPDATE_CHANNEL_URL)
                ],
                [InlineKeyboardButton("ℹ️ Help & Command", callback_data="helpmenu")]
            ]
        )
        
        await client.send_photo(
            chat_id=message.chat.id,
            photo="assets/wlc.jpg",
            caption=welcome_text,
            reply_markup=buttons
        )
        LOGGER.info(f"Sent welcome message to user {message.from_user.id}")