# pip install pytelegrambotapi

import config
import telebot
from time import time

bot = telebot.TeleBot(config.token)


def get_language(lang_code):
    # Иногда language_code может быть None
    if not lang_code:
        return "en"
    if "-" in lang_code:
        lang_code = lang_code.split("-")[0]
    if lang_code == "ru":
        return "ru"
    else:
        return "en"


@bot.message_handler(func=lambda message: message.entities is not None and message.chat.id == config.GROUP_ID)
def delete_links(message):
    for entity in message.entities:  # Пройдёмся по всем entities в поисках ссылок
        # url - обычная ссылка, text_link - ссылка, скрытая под текстом
        if entity.type in ["url", "text_link"]:
            # Мы можем не проверять chat.id, он проверяется ещё в хэндлере
            bot.delete_message(message.chat.id, message.message_id)
        else:
            return


# Выдаём Read-only за определённые фразы
@bot.message_handler(
    func=lambda
            message: message.text and message.text.lower() in config.restricted_messages and message.chat.id == config.GROUP_ID)
def set_ro(message):
    print(message.from_user.language_code)
    bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time() + 600)
    bot.send_message(message.chat.id, config.strings.get(get_language(message.from_user.language_code)).get("ro_msg"),
                     reply_to_message_id=message.message_id)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bot.infinity_polling()
