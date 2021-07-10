from telegram import InlineQueryResultVideo, Update, InputTextMessageContent
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown as em

from common.common import get_youtube_data

# TODO: Figure out error states for bot, how to specify that a link is invalid vs not found.
# TODO: Use the buttons system for the two links
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
                message_text=f"""
*{em(info["title"], version=2)}* — {em(info["artists_5"], version=2)}
[YouTube]({em(info["yt_url"], version=2)})
[Spotify]({em(info["sp_url"], version=2)})
                """,
                parse_mode="MarkdownV2"
            )
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)
