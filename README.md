Here’s a basic `README.md` file for your Discord bot that includes setup instructions, features, and usage details.

---

# Discord Music & Moderation Bot

This is a Python-based Discord bot that includes music playback features, moderation commands, and custom role management. The bot uses `discord.py` for interaction with Discord and `yt-dlp` for downloading and playing audio from YouTube.

## Features

- 🎵 **Music Player**:
  - Play songs from YouTube using voice commands.
  - Supports queue management, volume control, and stop functionality.
- 🔒 **Moderation Commands**:
  - Lock and unlock roles (e.g., remove/add roles from multiple members).
  - Channel clear functionality to remove messages.
  - Scheduled message deletion in specified channels.
- 📷 **Image Posting**:
  - Post images with context to a designated channel.
- 🧹 **Message Cleanup**:
  - Clear messages from command or specified channels.
- 🔊 **Voice Channel Support**:
  - Play audio in voice channels directly from YouTube.

## Prerequisites

- **Python 3.8+**
- **FFmpeg**: Required for playing audio in voice channels.
- **yt-dlp**: Required for YouTube audio extraction.
- **discord.py**: For interacting with Discord's API.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/discord-bot.git
cd discord-bot
```

### 2. Install Required Python Packages

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

1. Download FFmpeg from [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
   - Download the latest **"ffmpeg-release-full.7z"** from the Release Builds section.
2. Extract the archive using [7-Zip](https://www.7-zip.org/download.html).
3. Add the `ffmpeg/bin` folder to your system's PATH environment variable.
4. Verify the installation by running:

   ```bash
   ffmpeg -version
   ```

### 4. Set up Bot Token and Channel IDs

Create a `.env` file or replace the `TOKEN`, `POST_CHANNEL_ID`, `COMMAND_CHANNEL_ID`, `QP_ROLE_NAME`, and other channel/role settings directly in the `main.py` script.

```env
DISCORD_TOKEN=your-discord-bot-token
POST_CHANNEL_ID=' '
COMMAND_CHANNEL_ID=' '
EXTRA_CLEAR_CHANNEL_ID=' '
QP_ROLE_NAME= ROLE_NAME
MOD_ROLES=["ROLE 1", "ROLE N"]
BOT_LOGS_CHANNEL_ID=' '
```

### 5. Running the Bot

After setting up your bot token and channel IDs, you can start the bot by running:

```bash
python main.py
```

## Usage

### Music Commands

- **`!sing <song_name>`**: Search for a song on YouTube and play it in your current voice channel.
- **`!queue`**: Display the current song queue.
- **`!skip`**: Skip the currently playing song.
- **`!stop`**: Stop playing music and clear the queue.
- **`!volume <1-100>`**: Adjust the playback volume.

### Moderation Commands

- **`!post`**: Upload and post an image with context to a designated channel.
- **`!lockch`**: Remove the specified role (e.g., QP role) from all members in the server.
- **`!unlockch`**: Add the specified role (e.g., QP role) to all members in the server.
- **`!clear`**: Clear recent messages from the command channel or the specified channel.
- **`!stdelete <time>`**: Schedule a message deletion in command and post channels after a specified time.

### Example

- **Post Command**:
  ```
  !post
  ```
  Prompts the user to upload an image and then asks for context to post both in a designated channel.

- **Play Music**:
  ```
  !sing despacito
  ```
  Plays "Despacito" from YouTube in your current voice channel.

## Configuration

- Modify the bot token and channel IDs to fit your server setup.
- Customize the role names and channel permissions as needed.

## License

This project is licensed under the MIT License.

---

