# Copyright @ISmartDevs
# Channel t.me/TheSmartDev
#This Code Basically Forked From https://github.com/abirxdhackz/RestartModule

import shutil
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID, UPDATE_CHANNEL_URL, COMMAND_PREFIX
from core import auth_admins
from utils import LOGGER

def setup_restart_handler(app: Client):

    @app.on_message(filters.command(["restart", "reboot", "reload"], prefixes=COMMAND_PREFIX) & (filters.private | filters.group))
    async def restart(client, message):
        user_id = message.from_user.id
        auth_admins_data = auth_admins.find({}, {"user_id": 1, "_id": 0})
        AUTH_ADMIN_IDS = [admin["user_id"] for admin in auth_admins_data]
        if user_id != OWNER_ID and user_id not in AUTH_ADMIN_IDS:
            LOGGER.info("User not admin or owner, sending restricted message")
            await client.send_message(
                chat_id=message.chat.id,
                text="<b>✘Kids Not Allowed To Do This↯</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("👨🏼‍💻 Developer", url="https://t.me/abirxdhackz"),
                            InlineKeyboardButton("🤖 Other Bots", url=UPDATE_CHANNEL_URL)
                        ],
                        [
                            InlineKeyboardButton("🔗 Source Code", url="https://github.com/abirxdhack/RestartModule"),
                            InlineKeyboardButton("🔔 Update News", url=UPDATE_CHANNEL_URL)
                        ]
                    ]
                )
            )
            return

        LOGGER.info(f"Restart command initiated by user {user_id}")
        response = await client.send_message(
            chat_id=message.chat.id,
            text="<b>SecureXTools Restarting....</b>",
            parse_mode=ParseMode.HTML
        )

        # Directories to be removed
        directories = ["downloads", "temp", "temp_media", "data", "repos"]
        for directory in directories:
            try:
                shutil.rmtree(directory)
                LOGGER.info(f"Removed directory: {directory}")
            except FileNotFoundError:
                LOGGER.debug(f"Directory not found: {directory}")
            except Exception as e:
                LOGGER.error(f"Failed to remove directory {directory}: {e}")

        # Delete the botlogs.txt file if it exists
        if os.path.exists("botlog.txt"):
            try:
                os.remove("botlog.txt")
                LOGGER.info("Removed botlog.txt")
            except Exception as e:
                LOGGER.error(f"Failed to remove botlog.txt: {e}")

        # Delete session files (assuming session name is "SecureXTools"; replace with actual session name or import from config if different)
        session_files = ["SecureXTools.session-journal"]
        deleted = []
        not_deleted = []
        for file in session_files:
            try:
                os.remove(file)
                deleted.append(file)
                LOGGER.info(f"Removed session file: {file}")
            except FileNotFoundError:
                LOGGER.debug(f"Session file not found: {file}")
            except Exception as e:
                not_deleted.append(file)
                LOGGER.error(f"Failed to delete session file {file}: {e}")

        # Construct status message for session file deletion
        status_parts = []
        if deleted:
            status_parts.append(f"Deleted: {', '.join(deleted)}")
        if not_deleted:
            status_parts.append(f"Failed to delete: {', '.join(not_deleted)}")
        status = "No session files to delete." if not status_parts else " ".join(status_parts)
        LOGGER.info(f"Session file deletion status: {status}")

        await asyncio.sleep(10)

        await client.edit_message_text(
            chat_id=message.chat.id,
            message_id=response.id,
            text=f"<b>SecureXTools Successfully Restarted!</b>",
            parse_mode=ParseMode.HTML
        )
        LOGGER.info("Bot restart completed, executing system restart")
        os.system(f"kill -9 {os.getpid()} && bash start.sh")

    @app.on_message(filters.command(["stop", "kill", "off"], prefixes=COMMAND_PREFIX) & (filters.private | filters.group))
    async def stop(client, message):
        user_id = message.from_user.id
        auth_admins_data = auth_admins.find({}, {"user_id": 1, "_id": 0})
        AUTH_ADMIN_IDS = [admin["user_id"] for admin in auth_admins_data]
        if user_id != OWNER_ID and user_id not in AUTH_ADMIN_IDS:
            LOGGER.info("User not admin or owner, sending restricted message")
            await client.send_message(
                chat_id=message.chat.id,
                text="<b>✘Kids Not Allowed To Do This↯</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("👨🏼‍💻 Developer", url="https://t.me/abirxdhackz"),
                            InlineKeyboardButton("🤖 Other Bots", url=UPDATE_CHANNEL_URL)
                        ],
                        [
                            InlineKeyboardButton("🔗 Source Code", url="https://github.com/abirxdhack/RestartModule"),
                            InlineKeyboardButton("🔔 Update News", url=UPDATE_CHANNEL_URL)
                        ]
                    ]
                )
            )
            return

        LOGGER.info(f"Stop command initiated by user {user_id}")
        await client.send_message(
            chat_id=message.chat.id,
            text="<b>Bot Off Successfully All Database Cleared</b>",
            parse_mode=ParseMode.HTML
        )
        LOGGER.info("Bot stop executed, terminating process")
        os.system("pkill -f main.py")
