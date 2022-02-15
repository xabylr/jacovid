import enum
import logging

from persistence.database import Session
from persistence.models import Measures, Place
from persistence.utils.bot_utils import KeyboardMap
from sqlalchemy import and_
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Numeric
from telegram import ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, Updater
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler

logger = logging.getLogger()


class State(enum.Enum):
    CHOOSING = enum.auto()
    ADD_PLACE = enum.auto()
    REMOVE_PLACE = enum.auto()


spanish_places_options = KeyboardMap([
    [('ADD', 'Añadir sitio'), ('DELETE', 'Eliminar sito')],
    [('NO', 'No, gracias')]
])


def places_crud(update: Updater, context: CallbackContext):
    kbmap = spanish_places_options

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
            'Escribe el nombre de una Provincia, Distrito, '
            'Zona Básica de Salud o Municipio. También puedes utilizar "Andalucía" como lugar',
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


def remove_place(update: Updater, context: CallbackContext):
    update.message.reply_text('Aún no implementado :(')
    return places_crud(update, context)


def add_place(update: Updater, context: CallbackContext):
    place = search_place(update, context)

    if (place):
        update.message.reply_text(f'Guardando lugar con id {place.id}')
        return places_crud(update, context)


def search_place(update: Updater, context: CallbackContext) -> Place:
    """Search places and return multiple matches as buttons."""
    place_map = context.user_data.get('place_map', {})

    place = place_map.get(update.message.text)
    if (place):
        del context.user_data['place_map']
        return place

    with Session() as session:
        likesearch = f'%{update.message.text}%'

        coincidences = session.query(Place.name, func.count('name').label('coincidences')).\
            group_by(Place.name).subquery()

        results = session.query(Place, coincidences.c.coincidences).\
            join(coincidences, Place.name == coincidences.c.name).\
            filter(Place.name.ilike(likesearch)).\
            order_by(Place.name)

        if (results.count() == 1):
            place, _ = results[0]
            try:
                del context.user_data['place_map']
            except KeyError:
                pass
            return place
        else:
            place_map = {}

            for place, coincidences in results:
                place_name = place.name
                if coincidences > 1:
                    place_name += f' ({place.type})'

                place_map[place_name] = place

            context.user_data['place_map'] = place_map

            if(place_map):
                update.message.reply_text("Elige un sitio",
                                            reply_markup=ReplyKeyboardMarkup(
                                                [[row] for row in place_map.keys()],
                                                one_time_keyboard=True)
                                            )
            else: 
                update.message.reply_text("No se ha encontrado ningún sitio :(",
                                            reply_markup=None)


        # if len(found_places) > 0:
        #         if len(found_places) == 0:
        #             response = 'No se ha encontrado ningún municipio coincidente con la búsqueda'
        #         elif len(found_places) == 1:
        #             place = found_places[0]
        #             name = place.name
        #             pdia_14d = session.query(Measures).filter_by(
        #                 place_code=place.code, place_type=place.type
        #             ).order_by(Measures.date_reg.desc()).first().pdia_14d_rate

        #             response = (f'Casos por 100.000 habitantes acumulados en 14 días en {name}:\n'
        #                         f'{pdia_14d:.2f}')
        #         elif len(found_places) < 50:
        #             response = 'Varias coincidencias, por favor escribe un nombre más largo.\n'
        #             for place in found_places:
        #                 response += f'- {place.name}\n'
        #         else:
        #             response = f'Se han encontrado {len(found_places)} lugares coincidentes, por favor escribe un nombre más largo.'

        #     update.message.reply_text(response)


def fallback(update: Updater, context: CallbackContext):
    update.message.reply_text('Lo siento, no entendí eso :(')


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('places', places_crud)],
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
