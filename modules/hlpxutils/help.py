#Copyright @ISmartDevs
#Channel t.me/TheSmartDev

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode, ChatType
from config import BOT_USERNAME, OWNER_ID, UPDATE_CHANNEL_URL, BOT_NAME, COMMAND_PREFIX
from utils import LOGGER
from core import banned_users
from pyrogram import filters
import os

def setup_help_handler(app):
    @app.on_message(filters.command(["help", "tutorial"], prefixes=COMMAND_PREFIX) & (filters.private | filters.group))
    async def help_message(client, message):
        user_id = message.from_user.id if message.from_user else None
        if user_id and banned_users.find_one({"user_id": user_id}):
            await client.send_message(message.chat.id, "**✘ Sorry You're Banned From Using Me↯**")
            return

        user = message.from_user
        full_name = (user.first_name or "") + (f" {user.last_name}" if user and user.last_name else "")
        full_name = full_name.strip() or "User"
        user_mention = f"[{full_name}](tg://user?id={user.id})" if user else "User"

        if message.chat.type == ChatType.PRIVATE:
            help_text = (
                f"**This bot helps you manage your groups and provides various tools.**\n\n"
                "**Here are the available commands:**\n"
                "**━━━━━━━━━━━━━━━━**\n"
                "**/info** - **Get User Information.**\n"
                "**/id** - **Get Group & Channel Information.**\n"
                "**/ip** - **Get IP information.**\n"
                "**/px** - **Http/Https Proxy Checker.**\n"
                "**/ss** - **Take Screenshot of Website.**\n"
                "**/fb** - **Download Facebook video.**\n"
                "**/in** - **Download Instagram Photos, Reel Or Stories.**\n"
                "**/sp Or Send Direct Url** - **Download Spotify Track/Album Or Playlist.**\n"
                "**/song** - **Download Music or Youtube as Mp3 Format.**\n"
                "**/video** - **Download Youtube Video.**\n"
                "**/tt** - **Download Tiktok Video.**\n"
                "**/pnt** - **Download Pinterest Video.**"
            )
        else:
            group_name = message.chat.title if message.chat.title else "this group"
            help_text = (
                f"**Hey {user_mention}, Welcome to {group_name}!**\n"
                f"**This bot helps you manage your groups and provides various tools.**\n\n"
                "**Here are the available commands:**\n"
                "**━━━━━━━━━━━━━━━━**\n"
                "**/info** - **Get User Information.**\n"
                "**/id** - **Get Group & Channel Information.**\n"
                "**/ip** - **Get IP information.**\n"
                "**/px** - **Http/Https Proxy Checker.**\n"
                "**/ss** - **Take Screenshot of Website.**\n"
                "**/fb** - **Download Facebook video.**\n"
                "**/in** - **Download Instagram Photos, Reel Or Stories.**\n"
                "**/sp Or Send Direct Url** - **Download Spotify Track/Album Or Playlist.**\n"
                "**/song** - **Download Music or Youtube as Mp3 Format.**\n"
                "**/video** - **Download Youtube Video.**\n"
                "**/tt** - **Download Tiktok Video.**\n"
                "**/pnt** - **Download Pinterest Video.**"
            )

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Back to Start", callback_data="backtostartmsg"),
                InlineKeyboardButton("Close", callback_data="Closemsg")
            ]
        ])

        await client.send_message(
            chat_id=message.chat.id,
            text=help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=buttons,
            disable_web_page_preview=True,
        )
        LOGGER.info(f"Sent help message to chat {message.chat.id}")

    @app.on_callback_query(filters.regex("backtostartmsg|helpmenu|Closemsg"))
    async def handle_callback_query(client, callback_query):
        LOGGER.info(f"Processing callback '{callback_query.data}' from user {callback_query.from_user.id}")

        user = callback_query.from_user
        full_name = (user.first_name or "") + (f" {user.last_name}" if user.last_name else "")
        full_name = full_name.strip() or "User"
        user_mention = f"[{full_name}](tg://user?id={user.id})"

        if callback_query.data == "helpmenu":
            help_text = (
                "**This bot helps you manage your groups and provides various tools.**\n\n"
                "**Here are the available commands:**\n"
                "**━━━━━━━━━━━━━━━━**\n"
                "**/info** - **Get User Information.**\n"
                "**/id** - **Get Group & Channel Information.**\n"
                "**/ip** - **Get IP information.**\n"
                "**/px** - **Http/Https Proxy Checker.**\n"
                "**/ss** - **Take Screenshot of Website.**\n"
                "**/fb** - **Download Facebook video.**\n"
                "**/in** - **Download Instagram Photos, Reel Or Stories.**\n"
                "**/sp ** - **Download Spotify Track/Album Or Playlist.**\n"
                "**/song** - **Download Music or Youtube as Mp3 Format.**\n"
                "**/video** - **Download Youtube Video.**\n"
                "**/tt** - **Download Tiktok Video.**\n"
                "**/pnt** - **Download Pinterest Video.**"
            )
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Back", callback_data="backtostartmsg"),
                        InlineKeyboardButton("Close", callback_data="Closemsg")
                    ]
                ]
            )
            await client.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.id,
                text=help_text,
                reply_markup=buttons,
                parse_mode=ParseMode.MARKDOWN
            )
            LOGGER.info(f"Edited message to show help menu for user {user.id}")

        elif callback_query.data == "backtostartmsg":
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
            photo_path = "assets/wlc.jpg"
            
            if os.path.exists(photo_path):
                await client.send_photo(
                    chat_id=callback_query.message.chat.id,
                    photo=photo_path,
                    caption=welcome_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=buttons
                )
                await client.delete_messages(
                    chat_id=callback_query.message.chat.id,
                    message_ids=callback_query.message.id
                )
                LOGGER.info(f"Sent welcome photo message and deleted original for user {user.id}")
            else:
                await client.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.id,
                    text=welcome_text,
                    reply_markup=buttons,
                    parse_mode=ParseMode.MARKDOWN
                )
                LOGGER.warning(f"Photo {photo_path} not found, edited message to show welcome message for user {user.id}")

        elif callback_query.data == "Closemsg":
            await client.delete_messages(
                chat_id=callback_query.message.chat.id,
                message_ids=callback_query.message.id
            )
            LOGGER.info(f"Deleted message for user {user.id}")
