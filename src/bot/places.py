import logging
import enum

from telegram import ReplyKeyboardMarkup
from telegram.ext import CallbackContext, Updater, ConversationHandler
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler

from persistence.utils.bot_utils import KeyboardMap

logger = logging.getLogger()


class State(enum.Enum):
    CHOOSING, ADD_PLACE, REMOVE_PLACE = range(3)


spanish_places_kbmap = KeyboardMap([
    [('ADD', 'Añadir sitio'), ('DELETE', 'Eliminar sito')],
    [('NO', 'No, gracias')]
])


def places(update: Updater, context: CallbackContext):
    kbmap = spanish_places_kbmap

    context.user_data['keyboard_map'] = kbmap.map

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
        update.message.reply_text('A mandar!')

        return ConversationHandler.END

    elif answer == 'ADD':
        update.message.reply_text(
            'Escribe el nombre de un municipio para añadirlo a la lista',
            reply_markup=None
        )
        return State.ADD_PLACE

    elif answer == 'DELETE':
        update.message.reply_text(
            'Elige un municipio para borrar',
            reply_markup=None
        )
        return State.REMOVE_PLACE
    else:
        fallback(update, context)

def add_place( update: Updater, context: CallbackContext):
    update.message.reply_text('Aún no implementado :(')
    return places(update, context)

def remove_place( update: Updater, context: CallbackContext):
    update.message.reply_text('Aún no implementado :(')
    return places(update, context)


def fallback(update: Updater, context: CallbackContext):
    update.message.reply_text('Lo siento, no entendí eso :(')


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('places', places)],
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
