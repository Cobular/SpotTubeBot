import logging
from os import environ

from spotdl.search.spotifyClient import SpotifyClient
from telegram.ext import CommandHandler, InlineQueryHandler
from telegram.ext import Updater

from tg.commands import inline, start

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

SpotifyClient.init(
    client_id=environ.get("SPOTIFY_CLIENT_ID"),
    client_secret=environ.get("SPOTIFY_CLIENT_SECRET"),
    user_auth=False
)

updater = Updater(token=environ.get("TELEGRAM_BOT_TOKEN"))
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start.start)
dispatcher.add_handler(start_handler)

inline_handler = InlineQueryHandler(inline.inline_query)
dispatcher.add_handler(inline_handler)

updater.start_polling()
