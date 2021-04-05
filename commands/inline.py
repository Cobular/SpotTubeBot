import urllib.parse as urlparse
import urllib.request
from urllib.parse import parse_qs
from os import environ

import pyyoutube
from spotdl.search.utils import *
from telegram import InlineQueryResultVideo, Update, InputTextMessageContent
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown as em

youtube_api = pyyoutube.Api(api_key=environ.get("GOOGLE_API_KEY"))


def get_thumbnail(id: str):
    return f"https://img.youtube.com/vi/{id}/0.jpg"


def get_data(id: str):
    data = urllib.request.urlopen(f"http://youtube.com/get_video_info?video_id={id}")
    for line in data:  # files are iterable
        print(line)


# https://stackoverflow.com/a/19839257/5623598
def pretty_join(lst, cutoff=3):
    if not lst:
        return ""
    # One item form
    elif len(lst) == 1:
        return str(lst[0])
    # Two through `cutoff` artists use the long form
    elif 1 < len(lst) <= cutoff:
        return "{} and {}".format(", ".join(lst[:-1]), lst[-1])
    # More than `cutoff` artists and we cut it off
    return "{} and others".format(", ".join(lst))


def get_youtube_data(spotify_url: str):
    song = None
    # Catch spotify failing to find song
    try:
        song = SongObj.from_url(spotify_url)
    except Exception:
        return None

    # Catch no youtube url
    if song.get_youtube_link() is None:
        return None

    # Parse for youtube info
    parsed = urlparse.urlparse(song.get_youtube_link())
    id = parse_qs(parsed.query)['v'][0]
    videos = youtube_api.get_video_by_id(video_id=id).items

    # Catch when video ID fails
    if len(videos) == 0:
        return None

    # If all that passes, return the found information
    return {
        "title": videos[0].snippet.title,
        "thumbnail": videos[0].snippet.thumbnails.maxres.url,
        "yt_url": song.get_youtube_link(),
        "artists_5": pretty_join(song.get_contributing_artists(), cutoff=5),
        "artists_3": pretty_join(song.get_contributing_artists()),
        "sp_url": spotify_url
    }


def inline_query(update: Update, context: CallbackContext):
    query = update.inline_query.query

    # Catch null query
    if not query:
        return

    info = get_youtube_data(query)

    # Catch youtube data failure
    if info is None:
        return

    # Parse song into telegram's format
    results = list()
    results.append(
        InlineQueryResultVideo(
            id="0",
            title=f'{info["title"]}',
            video_url=info["yt_url"],
            mime_type="text/html",
            thumb_url=info["thumbnail"],
            description=f'by {info["artists_3"]}',
            input_message_content=InputTextMessageContent(
                message_text=f"""@
*{em(info["title"], version=2)}* — {em(info["artists_5"], version=2)}
[YouTube]({em(info["yt_url"], version=2)})
[Spotify]({em(info["sp_url"], version=2)})
                """,
                parse_mode="MarkdownV2"
            )
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)
