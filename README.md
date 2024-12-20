# Телеграм & ВКонтакте бот

Пример работы Telegram бота:


https://github.com/user-attachments/assets/b07f5ee4-4ab2-4474-9533-44a409fdae39

Пример работы Vkontakte бота:

https://github.com/user-attachments/assets/5f6969bb-5aa2-41cb-938c-2cad88ab68ad


Репозиторий представляет собой двух ботов, которых можно обучить отвечать на определенные фразы, боты работают с помощью сервиса [DialogFlow](https://dialogflow.cloud.google.com/)

Чтобы запустить ботов вам нужно будет:

- Создать [агента](https://dialogflow.cloud.google.com/)
- Создать [проект](https://cloud.google.com/dialogflow/es/docs/quick/setup)

ID проекта GoogleCloud совпадают с ProjectID на DialogFlolw.

Получить токен бота VK и Telegram.

## Запуск

У вас уже должен быть установлен python3.

```
pip intsall -r requirements.txt
```

Создайте `.env` файл и поместите туда следующие строки:

```
TELEGRAM_BOT_TOKEN=<Token бота телеграм>
VK_BOT_TOKEN=<Token бота ВКонтакте>
TG_CHAT_ID=<Ваш id телеграм для отправки сообщений о логировании>
DIALOG_FLOW_PROJECT_ID=<Id проекта на DialogFlow>
GOOGLE_APPLICATION_CREDENTIALS=<Путь к файлу c сервисным ключем от Google Cloud>

```

## Обучение ботов

Чтобы обучить бота нужно запустить файл `dialog_flow_learning_script.py`

Перед запуском создайте файл в формате `.json` и назовите его `trenings_fraze.json`

Туда нужно поместить данные следующей структурой:

```
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
```
