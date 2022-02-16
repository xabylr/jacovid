import enum
import logging
from bot.static import error

from persistence.database import Session
from persistence.models import Measures, Place
from persistence.models.user_tracking import UserTracking
from persistence.utils import user_transactions
from persistence.utils.bot_utils import KeyboardMap
from sqlalchemy import and_
from sqlalchemy.sql.sqltypes import Numeric
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler, Updater
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler

from bot import static

logger = logging.getLogger()


class State(enum.Enum):
    CHOOSING = enum.auto()
    ADD_PLACE = enum.auto()
    REMOVE_PLACE = enum.auto()


spanish_places_options = KeyboardMap([
    [('ADD', 'Añadir sitio'), ('DELETE', 'Eliminar sito')],
    [('NO', 'No, gracias')]
])


def crud(update: Updater, context: CallbackContext):
    kbmap = spanish_places_options
    context.user_data['keyboard_map'] = kbmap.map

    places_text = ''

    results = user_transactions.user_places(update.message.from_user.id)

    if(results):
        logger.info(results)
        for place, tracking in results:
                if(tracking.notification):
                    places_text+='🔔 '
                else:
                    places_text+='   '
                places_text+=f'{place.name}\n'

        update.message.reply_text(
            'Tus sitios:\n' +
            places_text +
            'Puedes editar la lista de sitios con las opciones del teclado',
            reply_markup=ReplyKeyboardMarkup(
                kbmap.keyboard, one_time_keyboard=True)
        )
    else:
        update.message.reply_text(
            'Ahora mismo no tienes ningún sitio añadido a la lista. '
            '¿Quieres añadir uno?',
            reply_markup=ReplyKeyboardMarkup(
                kbmap.keyboard, one_time_keyboard=True)
        )
    return State.CHOOSING


def choose_option(update: Updater, context: CallbackContext):
    answer = context.user_data['keyboard_map'].get(update.message.text)

    if answer == 'NO':
        update.message.reply_text('A mandar!',
                                    reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    elif answer == 'ADD':
        update.message.reply_text(
            'Escribe el nombre de una Provincia, Distrito, '
            'Zona Básica de Salud o Municipio. También puedes utilizar "Andalucía" como lugar',
            reply_markup=ReplyKeyboardRemove()
        )
        return State.ADD_PLACE

    elif answer == 'DELETE':
        update.message.reply_text(
            'Elige un municipio para borrar',
            reply_markup=ReplyKeyboardRemove()
        )
        return State.REMOVE_PLACE
    else:
        fallback(update, context)


def remove_place(update: Updater, context: CallbackContext):
    update.message.reply_text('Aún no implementado :(')
    return crud(update, context)


def add_place(update: Updater, context: CallbackContext):
    place = static.search_place(update, context)

    if (place):
        try:
            user_transactions.track_place(update.message.from_user.id, place.id)
            update.message.reply_text(f'Guardado lugar con id {place.id}', 
                                        reply_markup=ReplyKeyboardRemove())
        except:
            update.message.reply_text(f'Error guardando lugar {place.id}', 
                                        reply_markup=ReplyKeyboardRemove())
        return crud(update, context)

def fallback(update: Updater, context: CallbackContext):
    update.message.reply_text('Lo siento, no entendí eso :(')

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('places', crud)],
    states={
        State.CHOOSING: [
            MessageHandler(Filters.text, choose_option)
        ],
        State.ADD_PLACE: [
            MessageHandler(Filters.text, add_place)
        ],
        State.REMOVE_PLACE: [
            MessageHandler(Filters.text, remove_place)
        ]
    },
    fallbacks=[MessageHandler(Filters.all, fallback)]
)
