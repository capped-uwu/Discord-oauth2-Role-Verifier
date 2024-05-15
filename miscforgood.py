# REMOVE THE UNWANTED MESSAGE IN VERIFY CHANNEL

import discord
from discord.ext import tasks, commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='notuseprefixlolololololololo!', intents=intents)

TOKEN = your-bot-token'
CHANNEL_ID = your_verify_channel_id

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.playing, name="Verify Please!")
    await bot.change_presence(activity=activity)
    print(f'Bot is ready. Logged in as {bot.user}')
    clear_and_send.start()

@tasks.loop(seconds=0.1)
async def clear_and_send():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        def check(message):
            if message.embeds:
                return False
            if "gv!oauth" in message.content:
                return False
            return True
        
        await channel.purge(check=check)

        existing_embed = False
        async for message in channel.history(limit=100):
            if message.author == bot.user and message.embeds:
                embed = message.embeds[0]
                if (embed.title == "How to verify" and
                    "1. use the command called **gv!oauth**" in embed.description and
                    "2. click the link" in embed.description and
                    "3. complete!" in embed.description):
                    existing_embed = True
                    break

        if not existing_embed:
            embed = discord.Embed(
                title="How to verify",
                description=(
                    "1. use the command called **gv!oauth**\n"
                    "2. click the link\n"
                    "3. complete!"
                ),
                color=0x98fb98
            )

            await channel.send(embed=embed)

bot.run(TOKEN)
