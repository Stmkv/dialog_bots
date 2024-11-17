import logging

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Здравствуйте")


def message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_message = update.message.text
    user_answer = get_message_dealog_flow(
        dialog_flow_project_id, user_id, [user_message], "ru-RU"
    )

    update.message.reply_text(user_answer)


def get_message_dealog_flow(project_id, session_id, messages, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    for message in messages:
        user_message = dialogflow.TextInput(text=message, language_code=language_code)
        query_input = dialogflow.QueryInput(text=user_message)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        return response.query_result.fulfillment_text


if __name__ == "__main__":
    env = Env()
    env.read_env()
    telegram_bot_token = env.str("TELEGRAM_BOT_TOKEN")
    dialog_flow_project_id = env.str("DIALOG_FLOW_PROJECT_ID")

    updater = Updater(telegram_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message))

    updater.start_polling()
    updater.idle()
