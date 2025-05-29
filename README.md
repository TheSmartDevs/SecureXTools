## SecureXTools Bot 🚀

![GitHub repo size](https://img.shields.io/github/repo-size/TheSmartDevs/SecureXTools)
![GitHub license](https://img.shields.io/github/license/TheSmartDevs/SecureXTools)
![GitHub issues](https://img.shields.io/github/issues/TheSmartDevs/SecureXTools)
![GitHub stars](https://img.shields.io/github/stars/TheSmartDevs/SecureXTools?style=social)
![Telegram](https://img.shields.io/badge/Telegram-Join%20Channel-blue?logo=telegram)

SecureXTools is a powerful, feature-rich Telegram bot designed to provide tools for media downloading, IP and proxy checking, website screenshots, and administrative controls. It supports deployment on multiple platforms, including VPS, Heroku, and Docker, with compatibility for Ubuntu, Windows, RDP, and Debian hosting.

**Project Owner:** [@ISmartDevs](https://t.me/ISmartDevs)  
**Repository:** [GitHub - SecureXTools](https://github.com/TheSmartDevs/SecureXTools)  
**Community:** Join our [Telegram Channel](https://t.me/TheSmartDev) for updates and support 📢.

## Features ✨ Of SecureXTools

SecureXTools Bot offers the following commands and functionalities:

- **/start**: Initialize the SecureXTools Bot.
- **/help**: Display the help menu and list of available commands.
- **/info**: Retrieve user information from the database.
- **/id**: Get group or channel information.
- **/ip**: Fetch details about any IP address.
- **/px**: Check proxies of any type (up to a limit of 20).
- **/ss**: Capture a screenshot of any website.
- **/fb**: Download videos from Facebook.
- **/in**: Download Instagram reels and posts.
- **/sp**: Download tracks from Spotify.
- **/song**: Download music from YouTube.
- **/video**: Download videos from YouTube.
- **/tt**: Download TikTok videos.
- **/pnt**: Download Pinterest videos.
- **/settings**: Modify bot variables (Admin only).
- **/auth**: Promote a user to sudo status (Admin only).
- **/unauth**: Demote a user from sudo status (Admin only).
- **/gban**: Ban a user from using the bot (Admin only).
- **/gunban**: Unban a user from using the bot (Admin only).
- **/logs**: Retrieve bot console logs (Admin only).
- **/restart**: Restart the bot (Admin only).
- **/speedtest**: Check the bot server’s speed (Admin only).
- **/send**: Broadcast messages to users (Admin only).
- **/stats**: View bot usage statistics (Admin only).
- **/broadcast**: Broadcast messages to users using  (Admin only).
- **/stats**: View bot usage statistics (Admin only).
- **/off**: Turn Entire Bot Off (Admin only).


## Prerequisites 🛠️ For SecureXTools Bot

Before deploying SecureXTools Bot, ensure the following dependencies are installed:

1. **Python 3.8+**: Required for running the bot.
2. **FFmpeg**: Necessary for media processing.
   - For Ubuntu/Debian:
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```
   - Note: FFmpeg cannot be installed via `pip`. Use your system’s package manager.
3. **Python Dependencies**:
   - Install required Python packages:
     ```bash
     pip3 install -r requirements.txt
     ```

## Environment Variables ⚙️

### Mandatory Variables For Bot Deployment
The following environment variables must be set for the bot to function correctly:

| Variable             | Description                                      | Example Value                                |
|----------------------|--------------------------------------------------|----------------------------------------------|
| `API_ID`             | Telegram API ID from [my.telegram.org](https://my.telegram.org). | Your_API_ID_Here                             |
| `API_HASH`           | Telegram API Hash from [my.telegram.org](https://my.telegram.org). | Your_API_HASH_Here                           |
| `BOT_TOKEN`          | Bot token from [@BotFather](https://t.me/BotFather). | Your_BOT_TOKEN_Here                          |
| `BOT_USERNAME`       | Bot’s Telegram username.                        | @YourBotUsername                            |
| `BOT_NAME`           | Bot’s display name.                             | YourBotName                                 |
| `OWNER_ID`           | Telegram ID of the bot owner.                   | Your_OWNER_ID_Here                          |
| `DEVELOPER_USER_ID`  | Telegram ID of the developer (usually same as OWNER_ID). | Your_DEVELOPER_USER_ID_Here         |
| `MONGO_URL`          | MongoDB connection URL.                         | Your_MONGO_URL_Here                         |
| `DATABASE_URL`       | Same as `MONGO_URL` for database operations.    | Your_DATABASE_URL_Here                      |

### Optional Variables For Proper Working..
The following variables are optional and have default values if not set:

| Variable             | Description                                      | Default Value                                |
|----------------------|--------------------------------------------------|----------------------------------------------|
| `COMMAND_PREFIX`     | Prefixes for bot commands.                      | `!|.|#|,|/`                                 |
| `UPDATE_CHANNEL_URL` | Telegram channel for updates.                   | `https://t.me/TheSmartDev`                  |
| `IMGAI_SIZE_LIMIT`   | Max file size for image AI tools (bytes).       | `5242880`                                   |
| `MAX_TXT_SIZE`       | Max text file size (bytes).                     | `15728640`                                  |
| `MAX_VIDEO_SIZE`     | Max video file size (bytes).                    | `2147483648`                                |
| `YT_COOKIES_PATH`    | Path to YouTube cookies file.                   | `./cookies/SecureXTools.txt`                |
| `VIDEO_RESOLUTION`   | Resolution for YouTube downloads.               | `1280x720`                                  |
| `PROXY_CHECK_LIMIT`  | Max number of proxies to check.                 | `20`                                        |

## Deployment Methods & Instructions 

SecureXTools Bot supports multiple deployment methods: VPS, Heroku, and Docker. Follow the instructions below for your preferred platform.

### 1. Deploying on a VPS with Screen

#### Install Screen
Screen allows you to run the bot in a persistent session, even after closing your terminal.

- For Ubuntu/Debian:
  ```bash
  sudo apt update
  sudo apt install screen
  ```

- Start a new screen session:
  ```bash
  screen -S SecureXTools
  ```

#### Deploy the Bot
1. Clone the repository:
   ```bash
   git clone https://github.com/TheSmartDevs/SecureXTools.git
   cd SecureXTools
   ```

2. Install dependencies:
   ```bash
   sudo apt install ffmpeg
   pip3 install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root and populate it with the variables listed above.
   - Alternatively, edit `config.py` directly with your values Or `cp sample.env .env`

4. Run the bot:
   ```bash
   python3 main.py
   ```

5. Detach from the screen session:
   - Press `Ctrl+A`, then `Ctrl+D` to detach.
   - To reattach later:
     ```bash
     screen -r SecureXTools
     ```

6. Stop the bot:
   - Reattach to the screen session (`screen -r SecureXTools`).
   - Press `Ctrl+C` to stop the bot.

### 2. Heroku Deploy Methods!!!

#### Deploy with Heroku Button
For a quick deployment, use the Heroku Deploy button:

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/TheSmartDevs/SecureXTools)

#### Manual Heroku Deployment For Professionals
1. Clone the repository:
   ```bash
   git clone https://github.com/TheSmartDevs/SecureXTools.git
   cd SecureXTools
   ```

2. Create a Heroku app:
   ```bash
   heroku create your-app-name
   ```

3. Set environment variables:
   - Use the Heroku dashboard or CLI to set the required variables:
     ```bash
     heroku config:set API_ID=Your_API_ID_Here
     heroku config:set API_HASH=Your_API_HASH_Here
     heroku config:set BOT_TOKEN=Your_BOT_TOKEN_Here
     # Add other variables as needed
     ```

4. Deploy the app:
   ```bash
   git push heroku main
   ```

5. Start the bot:
   ```bash
   heroku ps:scale worker=1
   ```

6. Install FFmpeg on Heroku:
   - Add the FFmpeg buildpack:
     ```bash
     heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
     ```

### 3. Deploying with Docker Compose Method

#### Prerequisites
- Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

#### Deploy with Docker Compose
1. Clone the repository:
   ```bash
   git clone https://github.com/TheSmartDevs/SecureXTools.git
   cd SecureXTools
   ```

2. Create a `.env` file in the project root with the required environment variables.

3. Build and run the bot:
   ```bash
   docker compose up --build --remove-orphans
   ```

4. Stop the bot:
   ```bash
   docker compose down
   ```

## Bot Father Commands Setup Easy Method

1. **First Open Bot Father**:
   - First Go To [@BotFather](https://t.me/BotFather) Then Paste The Commands By Coping From Cutting From `cmds.txt` File.
2. **Easiest Way With Sudo Mode**:
   - Just Send /set Command To Your Hosted Bot And Then Commands Will Auto Set If  You Are Owner Of The Bot Or Your UserID Is In `OWNER_ID` VAR.

## Handling YouTube Download Errors with Cookies 📄

To avoid YouTube sign-in or bot protection errors, use a cookie file for authentication. Follow these steps:

1. **Create a Dedicated Chrome Profile**:
   - Set up a new Chrome profile for the bot to manage cookies securely.

2. **Install a Cookie Management Extension**:
   - Use an extension like [Cookie Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) to export cookies.

3. **Export Cookies from YouTube**:
   - Log into YouTube using the dedicated Chrome profile.
   - Use the cookie extension to export cookies in Netscape format.

4. **Save the Cookies File**:
   - Save the exported cookies as `SecureXTools.txt` in the `./cookies/SecureXTools.txt` directory.

### Cookie Management Tips
- **Cookie Expiry**: YouTube cookies may expire. If downloads fail, export and replace the cookies file.
- **Avoid Cookie Depletion**:
  - Do not play YouTube videos on the account used for cookies.
  - Avoid signing out from the associated Gmail account on your device.
  - Minimize frequent bot restarts to prevent cookie invalidation.
- **Monitor Cookies**: Regularly check bot activity to ensure cookies remain valid.

This setup ensures reliable access to YouTube content without sign-in or bot protection errors.

## Contributing 🤝 To SecureXTools

We welcome contributions to improve SecureXTools Bot. To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a clear description of your changes.

Please ensure your code follows the project’s coding standards and includes appropriate documentation.

## Support 📞 For Any Issue

For issues, questions, or feature requests:
- Join our [Telegram Channel](https://t.me/TheSmartDev) for community support.
- Contact the project owner: [@ISmartDevs](https://t.me/ISmartDevs).
- Open an issue on the [GitHub repository](https://github.com/TheSmartDevs/SecureXTools).

## License 📝

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

SecureXTools Bot is a project by [@ISmartDevs](https://t.me/ISmartDevs). Built for the Telegram community.

## Ethical Notice 📜

Simply modifying a few lines of code does not constitute original authorship. When forking this project, always:
- Fork responsibly and give proper credit to the original creators (@ISmartDevs).
- Customize the code as needed, but do not claim it as your own without significant contributions.