import logging
from io import BytesIO

import settings
import fast_neural_style
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


def antispam(bot, update):
    # удаляет вест флуд пользователя
    chat_id = update.message.chat_id
    bot.delete_message(
        chat_id=chat_id, message_id=update.message.message_id
    )
    print(update.message.text)


def start(bot, update):
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
    query = update.callback_query
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Выбирай, что хочешь сделать?',
        reply_markup=InlineKeyboardMarkup(settings.ACTION_KEYS),
        parse_mode='Markdown'
    )


def handle_operation(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    mode = update.callback_query.data
    if mode == "self":
        bot.send_message(chat_id=chat_id,
                         text=f'''Грузи две картинки!
Первая - к которой хочешь применить стиль, вторая - сам стиль''')
        settings.MODE = 'self'
        print(f'{settings.MODE}')
    if mode == "candy":
        bot.send_message(chat_id=chat_id,
                         text=f'''Хороший выбор. Грузи картинку. Попробуем...''')
        settings.MODE = 'candy'
        print(f'{settings.MODE}')
    if mode == "mosaic":
        bot.send_message(chat_id=chat_id,
                         text=f'''Это будет легко. Давай сюда картинку...''')
        settings.MODE = 'mosaic'
        print(f'{settings.MODE}')
    if mode == "udnie":
        bot.send_message(chat_id=chat_id,
                         text=f'''Какое то странное название, вроде бы известная картина. Но да ладно, грузи картинку...''')
        settings.MODE = 'udnie'
        print(f'{settings.MODE}')
    if mode == "princess":
        bot.send_message(chat_id=chat_id,
                         text=f'''Мое любимое. Давай картинку, покажу как у меня получается творить!''')
        settings.MODE = 'princess'
        print(f'{settings.MODE}')


def style_operation(bot, update):
    """Выбор действия с картинкой"""

    settings.STATUS = None

    chat_id = update.message.chat_id
    print("Got image from {}".format(chat_id))

    # получаем информацию о картинке
    image_info = update.message.photo[-1]
    image_file = bot.get_file(image_info)
    print(f'pic info:{image_file}')

    if settings.MODE is None:
        bot.send_message(
                chat_id=chat_id,
                message_id=update.message.message_id,
                text=f'''Стоп, стоп, стоп! Так не пойдет! А что делать то? Не выбрал!''',
                reply_markup=InlineKeyboardMarkup(settings.START_KEY),
                parse_mode='Markdown'
        )
    elif settings.MODE == 'self':
        print(f'Проверка_0: {first_image_file}')
        if chat_id in first_image_file:
            # первая картинка, которая к нам пришла станет content image, а вторая style image
            content_image_stream = BytesIO()
            print(f'main pic bytes info:{content_image_stream}')
            first_image_file[chat_id].download(out=content_image_stream)
            del first_image_file[chat_id]
            print(f'Проверка_2: {first_image_file}')
            style_image_stream = BytesIO()
            print(f'style pic bytes info:{content_image_stream}')
            image_file.download(out=style_image_stream)
            print(f'Проверка_3: {first_image_file}')
            bot.send_message(
                chat_id=chat_id,
                message_id=update.message.message_id,
                text=f'''Ну теперь жди ~ 2.5 минуты результат. Процесс не быстрый, сам понимаешь :>''',
                parse_mode='Markdown'
            )

            output = model.transfer_style(content_image_stream, style_image_stream)

            # теперь отправим назад фото
            output_stream = BytesIO()
            output.save(output_stream, format='PNG')
            output_stream.seek(0)
            bot.send_photo(chat_id, photo=output_stream)

            print("Sent Photo to user")
            settings.MODE = None
            settings.STATUS = 'DONE'
        else:
            first_image_file[chat_id] = image_file
            print(f'Проверка_1: {first_image_file}')
    else:
        first_image_file[chat_id] = image_file
        content_image_stream = BytesIO()
        print(f'main pic bytes info:{content_image_stream}')
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

        print(f'{output}')

        output_stream = BytesIO()
        output.save(output_stream, format='PNG')
        output_stream.seek(0)
        bot.send_photo(chat_id, photo=output_stream)

        print("Sent Photo to user")
        print('>UDNIE<')

        settings.MODE = None
        settings.STATUS = 'DONE'
    print(f'SS:{settings.STATUS}')
    if settings.STATUS == 'DONE':
        bot.send_message(
                chat_id=chat_id,
                message_id=update.message.message_id,
                text=f'''По мне так прикольно получилось. Еще попробуем?''',
                reply_markup=InlineKeyboardMarkup(settings.ACTION_KEYS),
                parse_mode='Markdown'
        )


def main():
    mybot = Updater(TOKEN, request_kwargs=PROXY)

    logging.info('Бот запускается')

    dp = mybot.dispatcher

    dp.add_handler(MessageHandler(Filters.text, antispam))
    dp.add_handler(MessageHandler(Filters.photo, style_operation))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(menu_operation, pattern='menu'))
    dp.add_handler(CallbackQueryHandler(handle_operation))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
