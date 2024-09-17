import discord
from discord.ext import commands
import asyncio
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
from datetime import timedelta

# Securely store your token in an environment variable in production
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'  # Replace with your bot token
POST_CHANNEL_ID = YOUR_POST_CHANNEL_ID  # Replace with the ID of the channel where you want to post
COMMAND_CHANNEL_ID = YOUR_COMMAND_CHANNEL_ID  # Replace with the ID of the channel where you want to accept commands
EXTRA_CLEAR_CHANNEL_ID = YOUR_EXTRA_CLEAR_CHANNEL_ID  # Replace with the ID of the additional channel for the !clear command
QP_ROLE_NAME = 'YOUR_QP_ROLE_NAME'  # Replace with the name of the role you want to manage
MOD_ROLES = ['MOD_ROLE_1', 'MOD_ROLE_2', 'MOD_ROLE_3']  # Roles that can use the lock and unlock commands
BOT_LOGS_CHANNEL_ID = YOUR_BOT_LOGS_CHANNEL_ID  # Replace with the ID of your bot logs channel

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.messages = True  # Enable message intents to fetch message history
intents.guilds = True  # Enable guilds intent to manage roles
intents.members = True  # Enable members intent to manage members

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

def has_mod_role(ctx):
    user_roles = [role.name for role in ctx.author.roles]
    return any(role in user_roles for role in MOD_ROLES)

@bot.command()
async def post(ctx):
    # Check if the command is in the designated command channel
    if ctx.channel.id != COMMAND_CHANNEL_ID:
        await ctx.send('This command can only be used in the designated command channel.')
        return

    await ctx.send('Please upload an image.')

    def check_image(m):
        return m.author == ctx.author and len(m.attachments) > 0 and m.channel.id == COMMAND_CHANNEL_ID

    try:
        image_msg = await bot.wait_for('message', timeout=60.0, check=check_image)
        image = image_msg.attachments[0]
    except asyncio.TimeoutError:
        await ctx.send('You took too long to send an image.')
        return

    await ctx.send('Now, please provide the context for the image.')

    def check_context(m):
        return m.author == ctx.author and m.content and m.channel.id == COMMAND_CHANNEL_ID

    try:
        context_msg = await bot.wait_for('message', timeout=60.0, check=check_context)
        context = context_msg.content
    except asyncio.TimeoutError:
        await ctx.send('You took too long to provide context.')
        return

    post_channel = bot.get_channel(POST_CHANNEL_ID)
    
    if not post_channel:
        await ctx.send('Post channel not found.')
        return

    await post_channel.send(content=context, file=await image.to_file())
    await ctx.send('Your image and context have been posted.')

    # Clear messages in the command channel
    if ctx.channel.id == COMMAND_CHANNEL_ID:
        await asyncio.sleep(2)  # Optional: wait for the message to be sent

        # Fetch and delete messages asynchronously
        async for message in ctx.channel.history(limit=100):
            try:
                await message.delete()
            except discord.Forbidden:
                await ctx.send('I do not have permission to delete some messages.')
            except discord.HTTPException as e:
                await ctx.send(f'Failed to delete a message due to HTTP exception: {e}')

@bot.command()
@commands.check(has_mod_role)
async def lockch(ctx):
    if ctx.channel.id != COMMAND_CHANNEL_ID:
        await ctx.send('This command can only be used in the designated command channel.')
        return

    qp_role = discord.utils.get(ctx.guild.roles, name=QP_ROLE_NAME)
    if not qp_role:
        await ctx.send(f'Role "{QP_ROLE_NAME}" not found.')
        return

    count = 0
    for member in ctx.guild.members:
        if qp_role in member.roles:
            try:
                await member.remove_roles(qp_role)
                count += 1
            except discord.Forbidden:
                await ctx.send(f'Failed to remove role from {member.name}. Check role hierarchy and permissions.')
            except discord.HTTPException as e:
                await ctx.send(f'HTTP exception: {e}')
    
    await ctx.send(f'Role "{QP_ROLE_NAME}" has been removed from {count} members.')

@bot.command()
@commands.check(has_mod_role)
async def unlockch(ctx):
    if ctx.channel.id != COMMAND_CHANNEL_ID:
        await ctx.send('This command can only be used in the designated command channel.')
        return

    qp_role = discord.utils.get(ctx.guild.roles, name=QP_ROLE_NAME)
    if not qp_role:
        await ctx.send(f'Role "{QP_ROLE_NAME}" not found.')
        return

    count = 0
    for member in ctx.guild.members:
        try:
            await member.add_roles(qp_role)
            count += 1
        except discord.Forbidden:
            await ctx.send(f'Failed to add role to {member.name}. Check role hierarchy and permissions.')
        except discord.HTTPException as e:
            await ctx.send(f'HTTP exception: {e}')
    
    await ctx.send(f'Role "{QP_ROLE_NAME}" has been added to {count} members.')

@bot.command()
async def clear(ctx):
    post_stuffs_here_channel = discord.utils.get(ctx.guild.channels, name="post stuffs here")

    if ctx.channel.id != COMMAND_CHANNEL_ID and ctx.channel.id != EXTRA_CLEAR_CHANNEL_ID and ctx.channel != post_stuffs_here_channel:
        await ctx.send('This command can only be used in the designated command channel, "post stuffs here" channel, or the additional clear channel.')
        return

    await asyncio.sleep(2)  # Optional: wait for the message to be sent

    # Fetch and delete messages asynchronously
    async for message in ctx.channel.history(limit=100):
        try:
            await message.delete()
        except discord.Forbidden:
            await ctx.send('I do not have permission to delete some messages.')
        except discord.HTTPException as e:
            await ctx.send(f'Failed to delete a message due to HTTP exception: {e}')

@bot.command()
async def stdelete(ctx, *, time_str: str):
    post_channel = bot.get_channel(POST_CHANNEL_ID)
    command_channel = bot.get_channel(COMMAND_CHANNEL_ID)
    bot_logs_channel = bot.get_channel(BOT_LOGS_CHANNEL_ID)
    
    if post_channel is None or command_channel is None or bot_logs_channel is None:
        await ctx.send('Could not find one of the channels. Please check the IDs.')
        return
    
    # Parse the time from the input
    try:
        time_quantity, time_unit = time_str.split()
        time_quantity = int(time_quantity)
        
        if time_unit in ['second', 'seconds']:
            wait_time = timedelta(seconds=time_quantity)
        elif time_unit in ['minute', 'minutes']:
            wait_time = timedelta(minutes=time_quantity)
        elif time_unit in ['hour', 'hours']:
            wait_time = timedelta(hours=time_quantity)
        elif time_unit in ['day', 'days']:
            wait_time = timedelta(days=time_quantity)
        else:
            await ctx.send('Invalid time unit. Use seconds, minutes, hours, or days.')
            return
        
    except ValueError:
        await ctx.send('Invalid time format. Please use a format like "1 minute" or "2 days".')
        return
    
    # Notify that the deletion has been scheduled
    await bot_logs_channel.send(f'Deletion scheduled in {command_channel.name} and {post_channel.name} in {time_str}.')
    
    # Wait for the specified time before deleting
    await asyncio.sleep(wait_time.total_seconds())
    
    # Delete messages in both channels
    async for message in command_channel.history(limit=100):
        try:
            await message.delete()
        except discord.Forbidden:
            await bot_logs_channel.send(f'Failed to delete a message in {command_channel.name} due to permission issues.')
        except discord.HTTPException as e:
            await bot_logs_channel.send(f'HTTP exception in {command_channel.name}: {e}')

    async for message in post_channel.history(limit=100):
        try:
            await message.delete()
        except discord.Forbidden:
            await bot_logs_channel.send(f'Failed to delete a message in {post_channel.name} due to permission issues.')
        except discord.HTTPException as e:
            await bot_logs_channel.send(f'HTTP exception in {post_channel.name}: {e}')

    # Notify in bot logs channel that messages were deleted
    await bot_logs_channel.send(f'Messages from {command_channel.name} and {post_channel.name} have been deleted.')

@bot.command()
async def sing(ctx, *, search_query: str):
    voice_channel = ctx.author.voice.channel

    if not voice_channel:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    # Search for the query on YouTube
    results = YoutubeSearch(search_query, max_results=3).to_dict()

    if not results:
        await ctx.send("No results found.")
        return

    # Display the search results to the user
    result_titles = [f"{i + 1}. {result['title']}" for i, result in enumerate(results)]
    await ctx.send("\n".join(result_titles))

    def check(m):
        return m.author == ctx.author and m.content.isdigit() and int(m.content) in range(1, len(results) + 1)

    try:
        choice = await bot.wait_for('message', timeout=15.0, check=check)
        selected_result = results[int(choice.content) - 1]
    except asyncio.TimeoutError:
        await ctx.send("You took too long to choose.")
        return

    url = f"https://www.youtube.com{selected_result['url_suffix']}"

    # Join the voice channel
    voice_client = await voice_channel.connect()

    # Play the audio using yt-dlp
    YDL_OPTIONS = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['url']
        title = info.get('title')

    source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
    voice_client.play(source)
    await ctx.send(f"Now playing: {title}")

    while voice_client.is_playing():
        await asyncio.sleep(1)

    await voice_client.disconnect()

bot.run(TOKEN)
