import secrets
import logging
import threading
from io import BytesIO

import settings
import fast_neural_style
from my_token_proxy import TOKEN, PROXY
from bot_model import StyleTransferModel


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


def antispam(bot, update):
    """Удаляет вест флуд пользователя."""

    chat_id = update.message.chat_id
    bot.delete_message(
        chat_id=chat_id, message_id=update.message.message_id
    )
    print(update.message.text)


def information(bot, update):
    """Страница ИНФО."""

    query = update.callback_query
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=settings.ABOUT,
        reply_markup=InlineKeyboardMarkup(settings.INFO_KEYS),
        parse_mode='Markdown',
    )


def start(bot, update):
    """Приветствие пользователя."""

    settings.STATUS = None
    settings.MODE = None
    text = f'''Хм, здорова *{update.message.chat.first_name}*, покреативим?
Я тут с картинками балуюсь, присоединяйся :>
Выбирай, что хочешь сделать?'''
    chat_id = update.message.chat_id
    bot.send_message(
        chat_id=chat_id,
        message_id=update.message.message_id,
        text=text,
        reply_markup=InlineKeyboardMarkup(settings.ACTION_KEYS),
        parse_mode='Markdown'
    )


def menu_operation(bot, update):
    """Главное меню с выбором стилей."""

    settings.STATUS = None
    settings.MODE = None
    print(f'user style: {settings.MODE}')
    query = update.callback_query
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Выбирай, что хочешь сделать?',
        reply_markup=InlineKeyboardMarkup(settings.ACTION_KEYS),
        parse_mode='Markdown'
    )


def handle_operation(bot, update):
    """Обработчик выбора стиля."""

    query = update.callback_query
    chat_id = query.message.chat_id
    mode = query.data
    if mode == "self":
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=query.message.message_id,
            text=f'''{secrets.choice(settings.SELF_PHRASE)}''',
            reply_markup=InlineKeyboardMarkup(settings.CHANGE_KEY)
        )
        settings.MODE = 'self'
        print(f'user style: {settings.MODE}')
    if mode == "candy":
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=query.message.message_id,
            text=f'''{secrets.choice(settings.CHOICE_PHRASES)}''',
            reply_markup=InlineKeyboardMarkup(settings.CHANGE_KEY)
        )
        settings.MODE = 'candy'
        print(f'user style: {settings.MODE}')
    if mode == "mosaic":
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=query.message.message_id,
            text=f'''{secrets.choice(settings.CHOICE_PHRASES)}''',
            reply_markup=InlineKeyboardMarkup(settings.CHANGE_KEY)
        )
        settings.MODE = 'mosaic'
        print(f'user style: {settings.MODE}')
    if mode == "udnie":
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=query.message.message_id,
            text=f'''{secrets.choice(settings.CHOICE_PHRASES)}''',
            reply_markup=InlineKeyboardMarkup(settings.CHANGE_KEY)
        )
        settings.MODE = 'udnie'
        print(f'user style: {settings.MODE}')
    if mode == "princess":
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=query.message.message_id,
            text=f'''{secrets.choice(settings.CHOICE_PHRASES)}''',
            reply_markup=InlineKeyboardMarkup(settings.CHANGE_KEY)
        )
        settings.MODE = 'princess'
        print(f'user style: {settings.MODE}')


def style_operation(bot, update):
    """Выбор действия с картинкой."""

    chat_id = update.message.chat_id
    fn = update.message.from_user['first_name']
    un = update.message.from_user['username']

    print(f'Got image from {fn} | @{un} ({chat_id})')

    # получаем информацию о картинке
    image_info = update.message.photo[-1]
    image_file = bot.get_file(image_info)
    print(f'Image info: {image_file}')

    if settings.MODE is None:
        bot.send_message(
                chat_id=chat_id,
                message_id=update.message.message_id,
                text=f'''{secrets.choice(settings.STOP_PHRASES)}''',
                reply_markup=InlineKeyboardMarkup(settings.START_KEY),
                parse_mode='Markdown'
        )
    elif settings.MODE == 'self':
        if chat_id in first_image_file:
            # первая картинка, которая к нам пришла станет content image, а вторая style image
            content_image_stream = BytesIO()
            first_image_file[chat_id].download(out=content_image_stream)
            del first_image_file[chat_id]

            style_image_stream = BytesIO()
            image_file.download(out=style_image_stream)
            bot.send_message(
                chat_id=chat_id,
                message_id=update.message.message_id,
                text=f'''{secrets.choice(settings.WAIT_PHRASES)}''',
                parse_mode='Markdown'
            )

            output = model.transfer_style(
                content_image_stream, style_image_stream
            )

            # теперь отправим назад фото
            output_stream = BytesIO()
            output.save(output_stream, format='PNG')
            output_stream.seek(0)
            bot.send_photo(chat_id, photo=output_stream)

            print(f'Sent style image to {fn} | @{un} ({chat_id})')
            settings.MODE = None
            settings.STATUS = 'DONE'
        else:
            first_image_file[chat_id] = image_file
    else:
        first_image_file[chat_id] = image_file
        content_image_stream = BytesIO()
        first_image_file[chat_id].download(out=content_image_stream)
        del first_image_file[chat_id]
        if settings.MODE == 'candy':
            output = fast_neural_style.stylize(content_image_stream, 'candy.pth')
        if settings.MODE == 'mosaic':
            output = fast_neural_style.stylize(content_image_stream, 'mosaic.pth')
        if settings.MODE == 'udnie':
            output = fast_neural_style.stylize(content_image_stream, 'rain_princess.pth')
        if settings.MODE == 'princess':
            output = fast_neural_style.stylize(content_image_stream, 'udnie.pth')

        output_stream = BytesIO()
        output.save(output_stream, format='PNG')
        output_stream.seek(0)
        bot.send_photo(chat_id, photo=output_stream)

        print(f'Sent style image to {fn} | @{un} ({chat_id})')
        settings.MODE = None
        settings.STATUS = 'DONE'

    if settings.STATUS == 'DONE':
        bot.send_message(
                chat_id=chat_id,
                message_id=update.message.message_id,
                text=f'''{secrets.choice(settings.END_PHRASES)}''',
                reply_markup=InlineKeyboardMarkup(settings.ACTION_KEYS),
                parse_mode='Markdown'
        )
        settings.STATUS = None


def shutdown():
    """Завершение работы."""
    mybot.stop()
    mybot.is_idle = False


def stop(bot, update):
    """Завершение работы."""
    threading.Thread(target=shutdown).start()


def main():

    logging.info('Бот запускается')

    dp = mybot.dispatcher

    dp.add_handler(MessageHandler(Filters.text, antispam))
    dp.add_handler(MessageHandler(Filters.photo, style_operation))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('forcestoponpc', stop))  # secret :>
    dp.add_handler(CallbackQueryHandler(menu_operation, pattern='menu'))
    dp.add_handler(CallbackQueryHandler(information, pattern='info'))
    dp.add_handler(CallbackQueryHandler(handle_operation))

    mybot.start_polling()
    mybot.idle()


mybot = Updater(TOKEN, request_kwargs=PROXY)


if __name__ == '__main__':
    main()
