import os

from discord.ext import commands
from discord.ext.commands import Context
import re

from common.common import get_youtube_data

# https://open.spotify.com/track/69HEUcXd73lvnQVb34m53L?si=e3bc5abb45c44178
url_regex = re.compile(r"http[s]*://(open.)*spotify.com/track/[\w?=]*")

bot = commands.Bot(command_prefix="}")

def is_allowed_channel(guild_id):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id
    return commands.check(predicate)

@bot.command()
async def convert(ctx: Context):
    # Need to verify how this works / what the right regex search func is
    if url_regex.search(ctx.message):
        yt_data = get_youtube_data(ctx.message)
        await ctx.send(yt_data.yt_url)
    else:
        await ctx.send("Uh oh, that doesn't seem to be a Spotify link!")


@bot.event()
async def on_message_receive(ctx: Context):
    # Need to decide how to maintain the channels to watch, maybe redis?
    # Best would be some python object that replicates itself to disk.
    # Needs to be O(1) lookup as well, or at least O(logN), so maybe a tree or hashmap?
    if True and (spotify_url := url_regex.search(ctx.message).group()) is not None:
        yt_data = get_youtube_data(ctx.message)
        await ctx.reply(yt_data.yt_url)


if __name__ == "__main__":
    bot.run(os.environ.get("DISCORD_BOT_TOKEN"))
