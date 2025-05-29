# Copyright @ISmartDevs
# Channel t.me/TheSmartDev

import asyncio
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.enums import ParseMode
from datetime import datetime, timedelta
from config import OWNER_ID, UPDATE_CHANNEL_URL, COMMAND_PREFIX, DEVELOPER_USER_ID
from core import auth_admins, user_activity_collection
from utils import LOGGER

# Function to update user activity in the MongoDB database
def update_user_activity(user_id, is_group=False):
    try:
        now = datetime.utcnow()
        user = user_activity_collection.find_one({"user_id": user_id})
        if not user:
            user_activity_collection.insert_one({
                "user_id": user_id,
                "is_group": is_group,
                "last_activity": now,
                "daily": 0,
                "weekly": 0,
                "monthly": 0,
                "yearly": 0
            })
            LOGGER.info(f"Inserted new user activity for user_id {user_id}, is_group={is_group}")
        else:
            user_activity_collection.update_one(
                {"user_id": user_id},
                {"$set": {"last_activity": now}},
                upsert=True
            )
            user_activity_collection.update_one(
                {"user_id": user_id},
                {"$inc": {"daily": 1, "weekly": 1, "monthly": 1, "yearly": 1}},
            )
            LOGGER.debug(f"Updated activity for user_id {user_id}, is_group={is_group}")
    except Exception as e:
        LOGGER.error(f"Error updating user activity for user_id {user_id}: {e}")

def is_admin(user_id):
    auth_admins_data = auth_admins.find({}, {"user_id": 1, "_id": 0})
    AUTH_ADMIN_IDS = [admin["user_id"] for admin in auth_admins_data]
    return user_id == OWNER_ID or user_id in AUTH_ADMIN_IDS

async def broadcast_handler(client: Client, message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        LOGGER.info(f"Unauthorized broadcast attempt by user_id {user_id}")
        await client.send_message(
            chat_id=message.chat.id,
            text="**✘Kids Not Allowed To Do This↯**",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    is_broadcast = message.command[0].lower() in ["broadcast", "b"]
    LOGGER.info(f"{'Broadcast' if is_broadcast else 'Send'} command initiated by user_id {user_id}")

    if message.reply_to_message:
        # Admin replies to a message with the command
        await process_broadcast(client, message.reply_to_message, is_broadcast, message.chat.id)
    elif is_broadcast and len(message.command) > 1:
        # Admin uses command with text to broadcast directly
        broadcast_text = " ".join(message.command[1:])
        await process_broadcast(client, broadcast_text, is_broadcast, message.chat.id)
    else:
        # Admin sends just the command; bot waits for a message
        action_type = "broadcast" if is_broadcast else "send"
        await client.send_message(
            chat_id=message.chat.id,
            text=f"**Please send the message you want to {action_type}.**",
            parse_mode=ParseMode.MARKDOWN
        )

        # Define the callback to handle the next message
        async def broadcast_message_callback(client: Client, broadcast_msg: Message):
            if broadcast_msg.from_user.id == message.from_user.id and broadcast_msg.chat.id == message.chat.id:
                await process_broadcast(client, broadcast_msg, is_broadcast, message.chat.id)
                client.remove_handler(broadcast_message_handler, group=1)

        # Add a temporary handler for the admin's next message
        broadcast_message_handler = MessageHandler(
            broadcast_message_callback,
            filters.user(message.from_user.id) & filters.chat(message.chat.id)
        )
        client.add_handler(broadcast_message_handler, group=1)

async def process_broadcast(client: Client, content, is_broadcast=True, chat_id=None):
    try:
        if isinstance(content, str):
            broadcast_text = content
            broadcast_msg = None
        elif isinstance(content, Message):
            broadcast_msg = content
            broadcast_text = None
        else:
            raise ValueError("Invalid content type")

        LOGGER.info(f"Processing {'broadcast' if is_broadcast else 'forward'} to users and groups")
        processing_message = await client.send_message(
            chat_id=chat_id,
            text=f'**💫 {"Broadcasting" if is_broadcast else "Sending"} Message In Progress 💫**',
            parse_mode=ParseMode.MARKDOWN
        )

        user_ids = [user["user_id"] for user in user_activity_collection.find({"is_group": False})]
        group_ids = [group["user_id"] for group in user_activity_collection.find({"is_group": True})]

        successful_users = 0
        failed_users = 0
        successful_groups = 0
        failed_groups = 0
        broadcast_start_time = datetime.now()

        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("💥 Bot Updates 💥", url=UPDATE_CHANNEL_URL)]])

        for target_chat_id in user_ids + group_ids:
            try:
                if broadcast_text:
                    await client.send_message(
                        chat_id=target_chat_id,
                        text=broadcast_text,
                        reply_markup=keyboard
                    )
                elif broadcast_msg:
                    if is_broadcast:
                        # Broadcast (copy) method
                        if broadcast_msg.text:
                            await client.send_message(
                                chat_id=target_chat_id,
                                text=broadcast_msg.text,
                                reply_markup=keyboard
                            )
                        elif broadcast_msg.photo:
                            await client.send_photo(
                                chat_id=target_chat_id,
                                photo=broadcast_msg.photo.file_id,
                                caption=broadcast_msg.caption or "",
                                reply_markup=keyboard
                            )
                        elif broadcast_msg.video:
                            await client.send_video(
                                chat_id=target_chat_id,
                                video=broadcast_msg.video.file_id,
                                caption=broadcast_msg.caption or "",
                                reply_markup=keyboard
                            )
                        elif broadcast_msg.audio:
                            await client.send_audio(
                                chat_id=target_chat_id,
                                audio=broadcast_msg.audio.file_id,
                                caption=broadcast_msg.caption or "",
                                reply_markup=keyboard
                            )
                        elif broadcast_msg.document:
                            await client.send_document(
                                chat_id=target_chat_id,
                                document=broadcast_msg.document.file_id,
                                caption=broadcast_msg.caption or "",
                                reply_markup=keyboard
                            )
                        else:
                            await client.copy_message(
                                chat_id=target_chat_id,
                                from_chat_id=broadcast_msg.chat.id,
                                message_id=broadcast_msg.id
                            )
                    else:
                        # Forward method
                        await client.forward_messages(
                            chat_id=target_chat_id,
                            from_chat_id=broadcast_msg.chat.id,
                            message_ids=broadcast_msg.id
                        )
                if target_chat_id in user_ids:
                    successful_users += 1
                else:
                    successful_groups += 1
            except Exception as e:
                LOGGER.error(f"Failed to {'broadcast' if is_broadcast else 'forward'} to chat_id {target_chat_id}: {e}")
                if target_chat_id in user_ids:
                    failed_users += 1
                else:
                    failed_groups += 1

        broadcast_end_time = datetime.now()
        time_diff = broadcast_end_time - broadcast_start_time
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_taken = f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"

        await processing_message.delete()

        action_success = "Broadcast" if is_broadcast else "Forward"
        LOGGER.info(f"{action_success} completed: {successful_users} users, {successful_groups} groups, {failed_users} failed users, {failed_groups} failed groups")

        await client.send_message(
            chat_id=chat_id,
            text=f"**💥 Hey Bro! {action_success} Successful ! 💥**\n"
                 "**✘━━━━━━━━━━━✘**\n"
                 f"**👀 To Users:** `{successful_users}` ✨\n"
                 f"**✘ Blocked Users** `{failed_users}` ❄️\n"
                 "**✘━━━━━━━━━━━✘**\n"
                 f"**🌐 To Groups** `{successful_groups}` 🌟\n"
                 f"**✘ Blocked Groups** `{failed_groups}` 💫\n"
                 "**✘━━━━━━━━━━━✘**\n"
                 f"**↯ Time Taken** `{time_taken}` 🇧🇩",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("💥 Bot Updates 💥", url=UPDATE_CHANNEL_URL)]]
            )
        )
    except Exception as e:
        LOGGER.error(f"Error processing {'broadcast' if is_broadcast else 'forward'}: {e}")
        await client.send_message(
            chat_id=chat_id,
            text="**✘ Error Processing Broadcast/Forward!**",
            parse_mode=ParseMode.MARKDOWN
        )

async def stats_handler(client: Client, message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        LOGGER.info(f"Unauthorized stats attempt by user_id {user_id}")
        await client.send_message(
            chat_id=message.chat.id,
            text="**✘Kids Not Allowed To Do This↯**",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    LOGGER.info(f"Stats command initiated by user_id {user_id}")
    try:
        now = datetime.utcnow()
        daily_users = user_activity_collection.count_documents({"is_group": False, "last_activity": {"$gt": now - timedelta(days=1)}})
        weekly_users = user_activity_collection.count_documents({"is_group": False, "last_activity": {"$gt": now - timedelta(weeks=1)}})
        monthly_users = user_activity_collection.count_documents({"is_group": False, "last_activity": {"$gt": now - timedelta(days=30)}})
        yearly_users = user_activity_collection.count_documents({"is_group": False, "last_activity": {"$gt": now - timedelta(days=365)}})
        
        total_users = user_activity_collection.count_documents({"is_group": False})
        total_groups = user_activity_collection.count_documents({"is_group": True})

        stats_text = (
            "**💥 Bot's Full Database Info 💥**\n"
            "**✘━━━━━━━━━━━✘**\n"
            "**✨ Registered Users Activity: ✨**\n"
            f"- 💫 Daily Active: {daily_users} 🔥\n"
            f"- 🌟 Weekly Active: {weekly_users} ⚡\n"
            f"- ❄️ Monthly Active: {monthly_users} 🌈\n"
            f"- 👀 Annual Active: {yearly_users} 🎯\n"
            "**✘━━━━━━━━━━━✘**\n"
            "**✘ Total Metrics: ✘**\n"
            f"- 👥 Total Users: {total_users} 💫\n"
            f"- 🌐 Total Groups: {total_groups} 🌟\n"
            f"- ↯ Database Size: {total_users + total_groups} ✨\n"
        )

        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("💥 Bot Updates 💥", url=UPDATE_CHANNEL_URL)]])
        await client.send_message(
            chat_id=message.chat.id,
            text=stats_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        LOGGER.info("Stats command completed successfully")
    except Exception as e:
        LOGGER.error(f"Error processing stats: {e}")
        await client.send_message(
            chat_id=message.chat.id,
            text="**✘ Error Processing Stats!**",
            parse_mode=ParseMode.MARKDOWN
        )

async def group_added_handler(client: Client, message: Message):
    try:
        for new_member in message.new_chat_members:
            if new_member.is_self:
                chat_id = message.chat.id
                update_user_activity(chat_id, is_group=True)
                await client.send_message(
                    chat_id=chat_id,
                    text="**💥 Thank You For Adding Me In This Group! 💫**\n"
                         "**✘ ━━━━━━━━━━━━━━━━━━ ✘**\n"
                         "**✨ I'm here to assist you with various tasks and make your group experience better.\n"
                         "↯ Feel free to explore my features and let me know if you need any help! 🌟**\n"
                         "**✘ ━━━━━━━━━━━━━━━━━━ ✘**",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("➕ Add Me 💥", url="https://t.me/ItsSmartToolBot?startgroup=new&admin=post_messages+delete_messages+edit_messages+pin_messages+change_info+invite_users+promote_members"),
                         InlineKeyboardButton("My Dev 💫", user_id=DEVELOPER_USER_ID)]
                    ])
                )
                LOGGER.info(f"Bot added to group {chat_id}")
    except Exception as e:
        LOGGER.error(f"Error in group_added_handler for chat_id {message.chat.id}: {e}")

def setup_admin_handler(app: Client):
    """
    Set up command handlers for the Pyrogram bot.
    This includes specific commands like /broadcast and /stats, as well as general activity tracking.
    """
    app.add_handler(
        MessageHandler(
            broadcast_handler,
            (filters.command(["broadcast", "b"]) | filters.command(["broadcast", "b"], prefixes=COMMAND_PREFIX) |
             filters.command(["send", "s"]) | filters.command(["send", "s"], prefixes=COMMAND_PREFIX)) & 
            (filters.private | filters.group)
        ),
        group=1,
    )
    
    app.add_handler(
        MessageHandler(
            stats_handler,
            (filters.command(["stats", "report", "status"]) | 
             filters.command(["stats", "report", "status"], prefixes=COMMAND_PREFIX)) & 
            (filters.private | filters.group)
        ),
        group=1,
    )
    
    app.add_handler(
        MessageHandler(
            lambda client, message: update_user_activity(message.from_user.id) if message.from_user else None,
            filters.all
        ),
        group=2,
    )

    app.add_handler(
        MessageHandler(
            group_added_handler,
            filters.group & filters.new_chat_members
        ),
        group=1
    )
