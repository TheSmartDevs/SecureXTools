# Copyright @ISmartDevs
# Channel t.me/TheSmartDev

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
from utils import LOGGER
from config import OWNER_ID, COMMAND_PREFIX
from core import auth_admins
from telegraph import Telegraph

# Initialize Telegraph client
telegraph = Telegraph()
telegraph.create_account(
    short_name="SmartUtilBot",
    author_name="SmartUtilBot",
    author_url="https://t.me/TheSmartDevs"
)

def setup_logs_handler(app: Client):

    async def create_telegraph_page(content: str) -> list:
        """Create Telegraph pages with the given content, each under 20 KB, and return list of URLs"""
        try:
            # Truncate content to 40,000 characters to respect Telegraph character limits
            truncated_content = content[:40000]
            # Convert content to bytes to measure size accurately
            content_bytes = truncated_content.encode('utf-8')
            max_size_bytes = 20 * 1024  # 20 KB in bytes
            pages = []
            page_content = ""
            current_size = 0
            lines = truncated_content.splitlines(keepends=True)

            for line in lines:
                line_bytes = line.encode('utf-8')
                # Check if adding this line would exceed 20 KB
                if current_size + len(line_bytes) > max_size_bytes and page_content:
                    # Create a Telegraph page with the current content
                    response = telegraph.create_page(
                        title="SmartLogs",
                        html_content=f"<pre>{page_content}</pre>",
                        author_name="SmartUtilBot",
                        author_url="https://t.me/TheSmartDevs"
                    )
                    pages.append(f"https://telegra.ph/{response['path']}")
                    # Reset for the next page
                    page_content = ""
                    current_size = 0
                page_content += line
                current_size += len(line_bytes)

            # Create a page for any remaining content
            if page_content:
                response = telegraph.create_page(
                    title="SmartLogs",
                    html_content=f"<pre>{page_content}</pre>",
                    author_name="SmartUtilBot",
                    author_url="https://t.me/TheSmartDevs"
                )
                pages.append(f"https://telegra.ph/{response['path']}")

            return pages
        except Exception as e:
            LOGGER.error(f"Failed to create Telegraph page: {e}")
            return []

    @app.on_message(filters.command(["logs"], prefixes=COMMAND_PREFIX) & (filters.private | filters.group))
    async def logs_command(client, message):
        user_id = message.from_user.id
        auth_admins_data = auth_admins.find({}, {"user_id": 1, "_id": 0})
        AUTH_ADMIN_IDS = [admin["user_id"] for admin in auth_admins_data]
        if user_id != OWNER_ID and user_id not in AUTH_ADMIN_IDS:
            LOGGER.info("User not admin or owner, sending restricted message")
            await client.send_message(
                chat_id=message.chat.id,
                text="**✘Kids Not Allowed To Do This↯**",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        # Send a loading message
        loading_message = await client.send_message(
            chat_id=message.chat.id,
            text="**Checking The Logs...💥**",
            parse_mode=ParseMode.MARKDOWN
        )

        # Wait for 2 seconds
        await asyncio.sleep(2)

        # Check if logs exist
        if not os.path.exists("botlog.txt"):
            await loading_message.edit_text(
                text="**Sorry Bro No Logs Found**",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        LOGGER.info("User is admin or owner, sending log document")
        await client.send_document(
            chat_id=message.chat.id,
            document="botlog.txt",
            caption="""**✘ Hey Sir! Here Is Your Logs ↯**
**✘━━━━━━━━━━━━━━━━━━━━━━━━━↯**
**✘ All Logs Database Succesfully Exported! ↯**
**↯ Access Granted Only to Authorized Admins ↯**
**✘━━━━━━━━━━━━━━━━━━━━━━━━━↯**
**✘ Select an Option Below to View Logs:**
**✘ Logs Here Offer the Fastest and Clearest Access! ↯**
**✘━━━━━━━━━━━━━━━━━━━━━━━━━↯**
**✘Huge Respect For You My Master↯**""",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✘ Display Logs↯", callback_data="display_logs"),
                    InlineKeyboardButton("✘ Web Paste↯", callback_data="web_paste$")
                ],
                [InlineKeyboardButton("✘ Close↯", callback_data="close_doc$")]
            ])
        )

        # Delete the temporary "Checking The Logs..." message
        await loading_message.delete()

    @app.on_callback_query(filters.regex(r"^(close_doc\$|close_logs\$|web_paste\$|display_logs)$"))
    async def handle_callback(client: Client, query: CallbackQuery):
        user_id = query.from_user.id
        data = query.data
        LOGGER.info(f"Callback query from user {user_id}, data: {data}")
        auth_admins_data = auth_admins.find({}, {"user_id": 1, "_id": 0})
        AUTH_ADMIN_IDS = [admin["user_id"] for admin in auth_admins_data]
        if user_id != OWNER_ID and user_id not in AUTH_ADMIN_IDS:
            LOGGER.info("User not admin or owner, sending callback answer")
            await query.answer(
                text="✘Kids Not Allowed To Do This↯",
                show_alert=True
            )
            return
        LOGGER.info("User is admin or owner, processing callback")
        if data == "close_doc$":
            await query.message.delete()
            await query.answer()
        elif data == "close_logs$":
            await query.message.delete()
            await query.answer()
        elif data == "web_paste$":
            await query.answer("Uploading logs to Telegraph...")
            # Edit the main log message to show uploading status
            await query.message.edit_caption(
                caption="**✘Uploading SmartLogs To Telegraph↯**",
                parse_mode=ParseMode.MARKDOWN
            )
            # Check if logs exist
            if not os.path.exists("botlog.txt"):
                await query.message.edit_caption(
                    caption="**✘Sorry Bro Telegraph API Dead↯**",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            try:
                # Read and truncate logs
                with open("botlog.txt", "r", encoding="utf-8") as f:
                    logs_content = f.read()
                # Create Telegraph pages
                telegraph_urls = await create_telegraph_page(logs_content)
                if telegraph_urls:
                    # Create buttons with two per row
                    buttons = []
                    for i in range(0, len(telegraph_urls), 2):
                        row = [
                            InlineKeyboardButton(f"✘ View Web Part {i+1}↯", url=telegraph_urls[i])
                        ]
                        if i + 1 < len(telegraph_urls):
                            row.append(InlineKeyboardButton(f"✘ View Web Part {i+2}↯", url=telegraph_urls[i+1]))
                        buttons.append(row)
                    # Add a close button in its own row
                    buttons.append([InlineKeyboardButton("✘ Close↯", callback_data="close_doc$")])
                    await query.message.edit_caption(
                        caption="""**✘ Hey Sir! Here Is Your Logs ↯**
**✘━━━━━━━━━━━━━━━━━━━━━━━━━↯**
**✘ All Logs Database Succesfully Exported! ↯**
**↯ Access Granted Only to Authorized Admins ↯**
**✘━━━━━━━━━━━━━━━━━━━━━━━━━↯**
**✘ Select a Page Below to View Logs:**
**✘ Logs Here Offer the Fastest and Clearest Access! ↯**
**✘━━━━━━━━━━━━━━━━━━━━━━━━━↯**
**✘Huge Respect For You My Master↯**""",
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=InlineKeyboardMarkup(buttons)
                    )
                else:
                    await query.message.edit_caption(
                        caption="**✘Sorry Bro Telegraph API Dead↯**",
                        parse_mode=ParseMode.MARKDOWN
                    )
            except Exception as e:
                LOGGER.error(f"Error uploading to Telegraph: {e}")
                await query.message.edit_caption(
                    caption="**✘Sorry Bro Telegraph API Dead↯**",
                    parse_mode=ParseMode.MARKDOWN
                )
        elif data == "display_logs":
            await send_logs_page(client, query.message.chat.id)
            await query.answer()

    async def send_logs_page(client: Client, chat_id: int):
        """Send the last 20 lines of botlog.txt, respecting Telegram's 4096-character limit"""
        LOGGER.info(f"Sending latest logs to chat {chat_id}")
        if not os.path.exists("botlog.txt"):
            await client.send_message(
                chat_id=chat_id,
                text="**✘Sorry Bro No Logs Found↯**",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        try:
            with open("botlog.txt", "r", encoding="utf-8") as f:
                logs = f.readlines()
            # Get the last 20 lines (or fewer if the file is shorter)
            latest_logs = logs[-20:] if len(logs) > 20 else logs
            text = "".join(latest_logs)
            # Truncate to 4096 characters (Telegram's message limit)
            if len(text) > 4096:
                text = text[-4096:]
            await client.send_message(
                chat_id=chat_id,
                text=text if text else "No logs available.",
                parse_mode=ParseMode.DISABLED,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✘ Back↯", callback_data="close_logs$")]
                ])
            )
        except Exception as e:
            LOGGER.error(f"Error sending logs: {e}")
            await client.send_message(
                chat_id=chat_id,
                text="**✘Sorry There Was A Issue On My Server↯**",
                parse_mode=ParseMode.MARKDOWN
            )
