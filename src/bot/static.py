import logging

from persistence.database import Session
from persistence.models import Measures, Place
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      Update)
from telegram.ext import CallbackContext, Updater

from bot import places

logger = logging.getLogger()

reply_keyboard = [
    ['Añadir sitio', 'Eliminar sito'],
    ['No, gracias'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(update: Updater, _: CallbackContext):
    """Send a message when the command /start is issued."""

    welcome_message = ('Escribe un nombre de un municipio para comprobar su información actualizada.'
                       'Fuente de los datos: https://www.juntadeandalucia.es/institutodeestadisticaycartografia/salud/static/index.html5')

    update.message.reply_text(welcome_message)


def add_place(update: Updater, _: CallbackContext):
    update.message.reply_text(f'Has elegido {update.message.text}')


def prueba_botones(update: Updater, _: CallbackContext):
    kb = [
        [KeyboardButton("Option 1")],
        [KeyboardButton("Option 2")]
    ]
    kb_markup = ReplyKeyboardMarkup(
        kb, resize_keyboard=True, one_time_keyboard=True)

    update.message.edit_reply_markup(kb_markup)

    update.message.reply_text('¡Hola!')

    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='1'),
         InlineKeyboardButton("Option 2", callback_data='2')],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=[
                              kb_markup, reply_markup])


def button(update: Update, _: CallbackContext):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")


def help(update, _):
    """Send a message when the command /help is issued."""

    update.message.reply_text('Help!')


def query_cases(update, context):
    """Search cases"""
    place = places.search_place(update, context)

    if(place):
          with Session() as session:
            # moto = session.query(Moto).filter_by(id=1).one()
            cases = session.query(Measures).filter_by(
                place_code=place.code,
            ).order_by(Measures.date_reg.desc()).first()

            update.message.reply_text(f'Casos por 100.000 habitantes acumulados en 14 días en {place.name}:\n'
                                    f'{str(cases.pdia_14d_rate)}',
                                    reply_markup=ReplyKeyboardRemove())


def error(update, context):
    """Log Errors caused by Updates."""

    logger.warning('Update "%s" caused error "%s"', update, context.error)
