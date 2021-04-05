from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello\\! My interface is through inline replies, so please type `@SpotTubeBot` followed by a spotify "
             "url in another chat\\. Thanks for using me\\!\\!",
        parse_mode="MarkdownV2")
