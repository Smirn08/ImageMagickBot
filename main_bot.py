import logging
import numpy as np
from PIL import Image
from io import BytesIO
from functools import wraps

import settings
from bot_model import StyleTransferModel
from my_token_proxy import TOKEN, PROXY

from telegram import InlineKeyboardMarkup

from telegram.ext import CallbackQueryHandler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')]
)


model = StyleTransferModel()
first_image_file = {}


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func
    return decorator


# @send_action(ChatAction.TYPING)
# def my_handler(bot, update):
#     pass


# @send_action(ChatAction.UPLOAD_VIDEO)
# def my_handler(bot, update):
#     pass


# @send_action(ChatAction.UPLOAD_PHOTO)
# def my_handler(bot, update):
#     pass


def start(bot, update):
    """Приветствие нового пользователя"""
    text = f'''Хм, здорова *{update.message.chat.first_name}*, покреативим?
Я тут с картинками балуюсь, присоединяйся :>'''
    update.message.reply_text(
        text, reply_markup=InlineKeyboardMarkup(settings.FIRST_KEYS),
        parse_mode='Markdown'
    )


def pic_request(bot, update):
    """Запрос загрузки картинки"""
    query = update.callback_query
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=f'''Ну дело такое значит. Грузи картинку, а там посмотрим что можно с ней сделать''',
        parse_mode='Markdown'
    )


def send_prediction_on_photo(bot, update):
    """Загрузка картинки"""
    chat_id = update.message.chat_id
    print("Got image from {}".format(chat_id))

    # получаем информацию о картинке
    image_info = update.message.photo[-1]
    image_file = bot.get_file(image_info)
    print(f'pic info:{image_file}')

    if chat_id in first_image_file:
        # первая картинка, которая к нам пришла станет content image, а вторая style image
        content_image_stream = BytesIO()
        print(f'main pic bytes info:{content_image_stream}')
        first_image_file[chat_id].download(out=content_image_stream)
        del first_image_file[chat_id]

        style_image_stream = BytesIO()
        print(f'style pic bytes info:{content_image_stream}')
        image_file.download(out=style_image_stream)

        output = model.transfer_style(content_image_stream, style_image_stream)

        # теперь отправим назад фото
        output_stream = BytesIO()
        output.save(output_stream, format='PNG')
        output_stream.seek(0)
        bot.send_photo(chat_id, photo=output_stream)
        print("Sent Photo to user")
    else:
        first_image_file[chat_id] = image_file


def main():
    mybot = Updater(TOKEN, request_kwargs=PROXY)

    logging.info('Бот запускается')

    dp = mybot.dispatcher

    dp.add_handler(MessageHandler(Filters.photo, send_prediction_on_photo))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(pic_request, pattern='pic_menu'))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
