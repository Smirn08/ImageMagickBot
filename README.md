# Image Magick Bot

Привет! 

Это телеграм бот - мой зачетный проект 1ой части курса [Deep Learning School при ФПМИ МФТИ](https://www.dlschool.org/)

Вы можете заценть его в Telegram: [ImageMagick](https://t.me/pic_magic_bot)
---

## Что умеет?

- Содержит в себе набор магии для применения стиля к отправленным ему картинкам;
- Даеет возможность создать свой собственный стиль.

---

## Принцип работы:

  1. Выбираешь стиль, который хочешь применить к картинке 
  2. Загружаешь картинку
  3. ...
  4. Получаешь красоту (но это не точно :>)
---

## Что использовал?

- [python 3.6.8](https://www.python.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [PyTorch](https://pytorch.org/)
    - [Torchvision](https://pytorch.org/docs/stable/torchvision/index.html)
    - [Fast Neural Style](https://github.com/pytorch/examples/tree/master/fast_neural_style)
- etc...
---

## Как запустить у себя
### Шаг 1
- Пишем [BotFather](https://t.me/BotFather) в Telegram
- Создаем нового бота и получаем `token`
### Шаг 2
```
1. git clone https://github.com/Smirn08/ImageMagickBot.git
2. python -m venv env
2. pip install -r requirements.txt.
```
### Шаг 3
- Редактируем `my_token_proxy.py`. Необходимо прописать свой `token` и `proxy`

### Шаг 4
```
1. .\env\Scripts\activate
2. python main_bot.py
```
---

## Подробнее о файлах:

- `main_bot.py` - main файл бота;
- `bot_model.py` - модель переноса стиля на картинку (на основе vgg19);
- `model_backend.py` - вспомогательные функции для модели;
- `settings.py` - файл с настройками бота;
- `fast_neural_style.py` и `transformer_net.py` - модель для быстрого переноса стиля;
- `my_token_proxy.py` - шаблон для TOKEN и PROXY

- в папке `saved_models` предобученные модели на основе [fast-neural-style-pytorch](https://github.com/rrmina/fast-neural-style-pytorch)

---

***Maksim Smirnov*** - <smirn08m@gmail.com>