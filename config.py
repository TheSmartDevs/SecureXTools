# Copyright @ISmartDevs
# Channel t.me/TheSmartDev

# Note: Configure via .env (VPS/Heroku local), direct edits to this file (VPS), or Heroku config vars (app.json/dashboard).
import os
from dotenv import load_dotenv

# Load .env file if it exists (for VPS or local Heroku testing), but allow Heroku config vars to take precedence
load_dotenv()

def get_env_or_default(key, default=None, cast_func=str):
    """Helper function to load environment variables with type casting and default values."""
    value = os.getenv(key)
    if value is not None and value.strip() != "":
        try:
            return cast_func(value)
        except (ValueError, TypeError) as e:
            print(f"Error casting {key} with value '{value}' to {cast_func.__name__}: {e}")
            return default
    return default

# TELEGRAM WITH PYROGRAM MTPROTO API CONNECTION AND AUTHORIZATION SETUP
API_ID = get_env_or_default("API_ID", "Your_API_ID_Here")
API_HASH = get_env_or_default("API_HASH", "Your_API_HASH_Here")
BOT_TOKEN = get_env_or_default("BOT_TOKEN", "Your_BOT_TOKEN_Here")
BOT_USERNAME = get_env_or_default("BOT_USERNAME", "@YourBotUsername")
BOT_NAME = get_env_or_default("BOT_NAME", "YourBotName")

# ADMINS AND SUDO USERS FOR BROADCAST AND OTHER SUDO WORKS
OWNER_ID = get_env_or_default("OWNER_ID", "Your_OWNER_ID_Here", int)
DEVELOPER_USER_ID = get_env_or_default("DEVELOPER_USER_ID", "Your_OWNER_ID_Here", int)

# MONGODB URL AND DATABASE URL FOR USER DATABASE AND GROUP SETTINGS DATABASE
MONGO_URL = get_env_or_default("MONGO_URL", "Your_MONGO_URL_Here")
DATABASE_URL = get_env_or_default("DATABASE_URL", "Your_MONGO_URL_Here")

# ALL COMMANDS PREFIXES FOR ALLOWING ALL COMMANDS SUPPORT
raw_prefixes = get_env_or_default("COMMAND_PREFIX", "!|.|#|,|/")
COMMAND_PREFIX = [prefix.strip() for prefix in raw_prefixes.split("|") if prefix.strip()]

# BOT DEVS CHANNEL URL AND PROFILE ERROR URL
UPDATE_CHANNEL_URL = get_env_or_default("UPDATE_CHANNEL_URL", "t.me/TheSmartDev")

# MAX FILE SIZE LIMITS FOR OCR TOOLS AND IMGAI
IMGAI_SIZE_LIMIT = get_env_or_default("IMGAI_SIZE_LIMIT", 5242880, int)
MAX_TXT_SIZE = get_env_or_default("MAX_TXT_SIZE", 15728640, int)
MAX_VIDEO_SIZE = get_env_or_default("MAX_VIDEO_SIZE", 2147483648, int)

# YOUTUBE COOKIES PATH
YT_COOKIES_PATH = get_env_or_default("YT_COOKIES_PATH", "./cookies/ItsSmartToolBot.txt")

# VIDEO RESOLUTION FOR YOUTUBE DOWNLOADS
VIDEO_RESOLUTION = get_env_or_default("VIDEO_RESOLUTION", "1280x720", lambda x: tuple(map(int, x.split('x'))))

# PROXY CHECK LIMIT
PROXY_CHECK_LIMIT = get_env_or_default("PROXY_CHECK_LIMIT", 20, int)

# Validation for critical variables
required_vars = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "BOT_USERNAME": BOT_USERNAME,
    "OWNER_ID": OWNER_ID,
    "DEVELOPER_USER_ID": DEVELOPER_USER_ID,
    "MONGO_URL": MONGO_URL
}

for var_name, var_value in required_vars.items():
    if var_value is None or var_value == f"Your_{var_name}_Here" or (isinstance(var_value, str) and var_value.strip() == ""):
        raise ValueError(f"Required variable {var_name} is missing or invalid. Set it in .env (VPS), config.py (VPS), or Heroku config vars.")

# Logging for debugging
print("Loaded COMMAND_PREFIX:", COMMAND_PREFIX)

if not COMMAND_PREFIX:
    raise ValueError("No command prefixes found. Set COMMAND_PREFIX in .env, config.py, or Heroku config vars.")