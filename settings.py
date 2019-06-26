from telegram import InlineKeyboardButton

START_KEY = [
    [
        InlineKeyboardButton('Выбрать стиль', callback_data='menu')
    ]
]

ACTION_KEYS = [
    [
        InlineKeyboardButton('Candy', callback_data='candy'),
        InlineKeyboardButton('Mosaic', callback_data='mosaic'),
        InlineKeyboardButton('Udnie', callback_data='udnie')
    ],
    [
        InlineKeyboardButton('Rain princess', callback_data='princess'),
        InlineKeyboardButton('Свой стиль', callback_data='self'),
        InlineKeyboardButton('ИНФО', callback_data='info')
    ]
]

INFO_KEYS = [
    [
        InlineKeyboardButton('<', callback_data='menu'),
        InlineKeyboardButton(
            'Bot Parking :>',
            url='https://github.com/Smirn08/ImageMagickBot'
        ),
        InlineKeyboardButton(
            'press F to pay respect',
            url='https://t.me/Smirn08'
        )
    ]
]

CHANGE_KEY = [
    [
        InlineKeyboardButton('Изменить выбор', callback_data='menu')
    ]
]

ABOUT = '''Данный бот написан как завершающий проект курса по Deep Learning School при ФПМИ МФТИ.
Подробнее можно почитать на Github или спросить у автора в telegram, выразив ему респект :P'''

CHOICE_PHRASES = [
    'Хороший выбор. Грузи картинку. Попробуем...',
    'Это будет легко. Давай сюда картинку...',
    'Какое то странное название, вроде бы известная картина. Но да ладно, грузи картинку...',
    'Мое любимое. Давай картинку, покажу как у меня получается творить!'
]

SELF_PHRASE = [
    'Грузи две картинки! Первая - к которой хочешь применить стиль, вторая - сам стиль'
]

END_PHRASES = [
    'По мне так прикольно получилось. Еще попробуем?',
    'Ну думаю сойдет. Давай еще?',
    'Выглядит прикольно. Выбирай еще!'
]

WAIT_PHRASES = [
    'Ну теперь жди несколько минут результат. Процесс не быстрый, сам понимаешь :>',
    'Нужно будет подождать несколько минуток. Я все таки стараюсь!',
    'Мде ну и выбор у тебя конечно. Ладно. Жди. Скоро пришлю результат.'
]

STOP_PHRASES = [
    'Стоп, стоп, стоп! Так не пойдет! А что делать то? Не выбрал!',
    'Да погоди ты! Выбирай сначала что сделать!',
    'Не торопись, выбери стиль!'
]


MODE = None
STATUS = None
