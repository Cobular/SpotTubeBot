import os
import shelve
from os import environ

from discord.ext.commands import Bot
from spotdl.search.spotifyClient import SpotifyClient


class CustomBot(Bot):
    channel_shelf: shelve.Shelf

    def __init__(self, command_prefix, **options):
        self.channel_shelf = shelve.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "channel_shelf"))

        SpotifyClient.init(
            client_id=environ.get("SPOTIFY_CLIENT_ID"),
            client_secret=environ.get("SPOTIFY_CLIENT_SECRET"),
            user_auth=False
        )

        super().__init__(command_prefix, **options)

    def __del__(self):
        self.channel_shelf.close()