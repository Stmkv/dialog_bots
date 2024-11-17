import random

import vk_api
from environs import Env
from google.cloud import dialogflow
from telegram import Bot
from vk_api.longpoll import VkEventType, VkLongPoll

from logging_config import start_logger


def message(event, vk_api):
    message = event.message
    user_id = f"vk-{event.user_id}"
    reply_user = get_message_dealog_flow(
        dialog_flow_project_id, user_id, [message], "ru-RU"
    )
    if not reply_user:
        return
    vk_api.messages.send(
        user_id=event.user_id, message=reply_user, random_id=random.randint(1, 1000)
    )


def get_message_dealog_flow(project_id, session_id, messages, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    for message in messages:
        user_message = dialogflow.TextInput(text=message, language_code=language_code)
        query_input = dialogflow.QueryInput(text=user_message)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        if response.query_result.intent.is_fallback:
            return
        return response.query_result.fulfillment_text


if __name__ == "__main__":
    env = Env()
    env.read_env()
    vk_token_group = env.str("VK_BOT_TOKEN")
    dialog_flow_project_id = env.str("DIALOG_FLOW_PROJECT_ID")

    telegram_bot_token = env.str("TELEGRAM_BOT_TOKEN")
    bot = Bot(telegram_bot_token)
    tg_chat_id = env.str("TG_CHAT_ID")
    logger = start_logger(bot, tg_chat_id)
    logger.info("Бот запущен")
    try:
        vk_session = vk_api.VkApi(token=vk_token_group)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                message(event, vk_api)
    except Exception as e:
        logger.error(f"Произошла ошибка при работе Vk бота: {e}")
