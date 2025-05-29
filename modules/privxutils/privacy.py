# Copyright @ISmartDevs
# Channel t.me/TheSmartDev

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import COMMAND_PREFIX
from utils import LOGGER  # (optional, for logging consistency)
from core import banned_users  

# Define your privacy policy text
PRIVACY_POLICY = """
<b>📜 Privacy Policy for SecureXTools 💥</b>
━━━━━━━━━━━━━━━━━

Welcome to SecureXTools 💥. By using our services, you agree to this privacy policy.

<b>1. Information We Collect:</b>
   - <b>Personal Information:</b> User ID and username for personalization.
   - <b>Usage Data:</b> Information on how you use the app to improve our services.

<b>2. Usage of Information:</b>
   - <b>Service Enhancement:</b> To provide and improve SecureXTools.
   - <b>Communication:</b> Updates and new features.
   - <b>Security:</b> To prevent unauthorized access.
   - <b>Advertisements:</b> Display of promotions.

<b>3. Data Security:</b>
   - These tools do not store any data, ensuring your privacy.
   - We use strong security measures, although no system is 100% secure.

Thank you for using SecureXTools 💥. We prioritize your privacy and security.
"""

def setup_privacy_handler(app: Client):
    @app.on_message(filters.command(["privacy"], prefixes=COMMAND_PREFIX) & (filters.private | filters.group))
    async def show_privacy_policy(client, message):
        user_id = message.from_user.id if message.from_user else None
        if user_id and banned_users.find_one({"user_id": user_id}):
            await client.send_message(message.chat.id, "**✘Sorry You're Banned From Using Me↯**")
            return

        await client.send_message(
            message.chat.id,
            PRIVACY_POLICY,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Close", callback_data="close_privacy_policy")]
            ])
        )

    @app.on_callback_query(filters.regex("close_privacy_policy"))
    async def close_privacy_policy(client, callback_query):
        await callback_query.message.delete()