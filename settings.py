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
        InlineKeyboardButton('Свой стиль', callback_data='self')
    ]
]

MODE = None
STATUS = None
