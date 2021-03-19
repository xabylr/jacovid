import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CallbackContext

from persistence import database
from persistence.models import Measures, Place

logger = logging.getLogger()


def start(update: Updater, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    kb = [[KeyboardButton("Option 1")],
          [KeyboardButton("Option 2")]]
    kb_markup = ReplyKeyboardMarkup(kb,
                                    resize_keyboard=True,
                                    one_time_keyboard=True)

    update.message.edit_reply_markup(kb_markup)


    update.message.reply_text('¡Hola!')

    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=[kb_markup, reply_markup])

def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")


def help(update, context):
    """Send a message when the command /help is issued."""

    update.message.reply_text('Help!')


def casos(update, context):
    """Send a message when the command /casos is issued."""
    session = database.get_session()
    # moto = session.query(Moto).filter_by(id=1).one()

    pdia_14d_malaga = session.query(Measures).filter_by(
            place_code = '29067', place_type = 'M'
            ).order_by(Measures.date_reg.desc()).first().pdia_14d_rate

    logger.info("PDIA 14d "+str(pdia_14d_malaga))

    update.message.reply_text(
        f'''Casos por 100.000 habitantes acumulados en 14 días en Málaga capital:
            {str(pdia_14d_malaga)}''')

    session.close()

def search(update, context):
    """Search municipality."""
    session = database.get_session()
    usertext = "%"+update.message.text+"%"

    response = "No se ha encontrado la ubicación"

    found_place = session.query(Place).filter(Place.name.ilike(usertext)).first()

    if found_place:
        name = found_place.name
        pdia_14d= session.query(Measures).filter_by(
            place_code = found_place.code, place_type = found_place.type
            ).order_by(Measures.date_reg.desc()).first().pdia_14d_rate

        response =  f'''Casos por 100.000 habitantes acumulados en 14 días en {name}:
            {str(pdia_14d)}'''

    update.message.reply_text(response)


def error(update, context):
    """Log Errors caused by Updates."""

    logger.warning('Update "%s" caused error "%s"', update, context.error)
