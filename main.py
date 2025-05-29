#Copyright @ISmartDevs
#Channel t.me/TheSmartDev

from app import app
from utils import LOGGER
from core import setup_start_handler
from modules import setup_modules_handlers
from sudoers import setup_sudoers_handlers
from callback import handle_callback_query
from pyrogram import filters

setup_start_handler(app)
setup_modules_handlers(app)
setup_sudoers_handlers(app)

@app.on_callback_query()
async def handle_callback(client, callback_query):
    await handle_callback_query(client, callback_query)

if __name__ == "__main__":
    LOGGER.info("SecureXTools Successfully Started!🔥")
    app.run()