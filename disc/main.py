import json
import os
from typing import Optional

import discord
import httpx
from discord import TextChannel, Message
from discord.abc import GuildChannel
from discord_slash import SlashCommand, SlashContext
import re
import logging

from discord_slash.utils.manage_commands import create_option, create_permission
from httpx import Response

from common.common import get_youtube_data

from disc.customBot import CustomBot

# https://open.spotify.com/track/69HEUcXd73lvnQVb34m53L?si=e3bc5abb45c44178
url_regex = re.compile(r"http[s]*://(open.)*spotify.com/track/[\w?=]*")

bot: CustomBot = CustomBot(command_prefix="}", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

headers = {
    'Content-Type': 'application/json',
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64'
}


async def send_diagnostics(identifier):
    async with httpx.AsyncClient() as client:
        payload = {
            'payload': {
                'website': "f43ac577-0c33-4eaf-bc20-993bd3ebb94c",
                'url': f"/{identifier}",
                'referrer': "",
                'hostname': "cobular.com",
                'language': "en-US",
                'screen': "1920x1080"
            },
            'type': "pageview",
        }
        r: Response = await client.post('https://umami.cobular.com/api/collect', data=json.dumps(payload),
                                        headers=headers)


@slash.slash(
    name="convert",
    description="Used to convert a spotify song link to youtube, if possible",
    options=[
        create_option(
            name="spotify_song_url",
            description="A spotify song url like https://open.spotify.com/track/69HEUcXd73lvnQVb34m53L?si=e3bc5abb45c44178",
            option_type=3,
            required=True
        )
    ]
)
async def convert(ctx: SlashContext, spotify_song_url):
    """Command to convert a single link"""
    # Need to verify how this works / what the right regex search func is
    if url_regex.search(spotify_song_url):
        await ctx.defer()
        yt_data = get_youtube_data(spotify_song_url)
        await ctx.send(yt_data.yt_url)
    else:
        await ctx.send("Uh oh, that doesn't seem to be a Spotify link!")
    await send_diagnostics("convert")


@slash.slash(
    name="add_channel",
    description="Adds the current channel to the watchlist",
    options=[
        create_option(
            name="channel",
            description="The channel to enable song autoconversion",
            required=False,
            option_type=7
        )
    ]
)
async def add_channel(ctx: SlashContext, channel: Optional[GuildChannel] = None):
    """Command to add a new channel to the database"""
    if channel is None:
        channel = ctx.channel
    if isinstance(channel, TextChannel):
        bot.channel_shelf[f"{channel.guild.id}-{channel.id}"] = 0
        bot.channel_shelf.sync()
        await ctx.send("👍", hidden=True)
    else:
        await ctx.send("Please send a text channel", hidden=True)
    await send_diagnostics("add channel")


@slash.slash(
    name="remove_channel",
    description="Removes the current channel to the watchlist",
    options=[
        create_option(
            name="channel",
            description="The channel to enable song autoconversion",
            required=False,
            option_type=7
        )
    ]
)
async def remove_channel(ctx: SlashContext, channel: Optional[GuildChannel] = None):
    """Command to remove a channel from the database"""
    if channel is None:
        channel = ctx.channel
    if isinstance(channel, TextChannel):
        try:
            del bot.channel_shelf[f"{channel.guild.id}-{channel.id}"]
            bot.channel_shelf.sync()
        except KeyError:
            pass
        await ctx.send("👍", hidden=True)
    else:
        await ctx.send("Please send a text channel", hidden=True)
    await send_diagnostics("delete channel")


def is_in_channel_shelf(channel: TextChannel) -> bool:
    return f"{channel.guild.id}-{channel.id}" in bot.channel_shelf


def is_not_bot(ctx: Message) -> bool:
    return not ctx.author.bot


@bot.event
async def on_message(message: Message):
    """Auto convert spotify links in certain channels"""
    if is_not_bot(message) and \
            is_in_channel_shelf(message.channel) and \
            (spotify_url := url_regex.search(message.content).group(0)) is not None:
        yt_data = get_youtube_data(spotify_url)
        await message.reply(yt_data.yt_url, mention_author=False)


@bot.event
async def on_ready():
    logging.warning("bot is awake")


if __name__ == "__main__":
    bot.run(os.environ.get("DISCORD_BOT_TOKEN"))
