import logging
import traceback

from persistence.database import Session
from persistence.models import Measures, Place, User
from persistence.utils import user_transactions
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      Update)
from telegram.ext import CallbackContext, Updater, conversationhandler

logger = logging.getLogger()

reply_keyboard = [
    ['Añadir sitio', 'Eliminar sito'],
    ['No, gracias'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(update: Updater, context: CallbackContext):
    """Send a message when the command /start is issued."""

    tg_user = update.message.from_user
    model_user = User(id=tg_user.id)
    user_transactions.update_user_registration(model_user)

    return help(update, context)


def add_place(update: Updater, _: CallbackContext):
    update.message.reply_text(f'Has elegido {update.message.text}')




def help(update: Updater, _: CallbackContext):
    """Send a message when the command /help is issued."""
    welcome_message = ( 'Escribe un nombre de un lugar de andalucía para comprobar su última información de incidencia.\n'
                        'Usa /places para editar la lista de sitios de vigilancia y /cases para obtener '
                        'la información más reciente disponible.\n'
                        'Fuente de los datos: https://www.juntadeandalucia.es/institutodeestadisticaycartografia/salud/static/index.html5')
    update.message.reply_text(welcome_message)

def cases(update: Updater, context: CallbackContext):
    """Search cases"""
    results = user_transactions.user_places(update.message.from_user.id)
    place_ids = [t[0].id for t in results]
    reply_cases(update, place_ids)


def query_cases(update: Updater, context: CallbackContext):
    """Search cases"""
    place = search_place(update, context)

    if(place):
          with Session() as session:
            # moto = session.query(Moto).filter_by(id=1).one()
            cases = session.query(Measures).filter_by(
                place_code=place.code,
            ).order_by(Measures.date_reg.desc()).first()

            update.message.reply_text(f'Casos por 100.000 habitantes acumulados en 14 días en {place.name}:\n'
                                    f'{str(cases.pdia_14d_rate)}',
                                    reply_markup=ReplyKeyboardRemove())

def reply_cases(update: Updater, place_ids):
     with Session() as session:
        m1 = aliased(Measures)
        m2 = aliased(Measures)
        # moto = session.query(Moto).filter_by(id=1).one()
        results = session.query(m1, Place).\
            join(Place, 
                (Place.code == m1.place_code)
                            &
                (Place.type == m1.place_type), 
                isouter=True
            ).\
            join(m2, 
                (m1.place_code == m2.place_code)
                            &
                (m1.place_type == m2.place_type)
                            &
                (m1.date_reg < m2.date_reg),
                isouter=True
            ).\
            filter(m2.id == None).\
            filter(Place.id.in_(place_ids) )

        logger.info(results)

        for measures, place in results:
            update.message.reply_text(f'{measures.dt_reg} - Casos por 100.000 habitantes acumulados en 14 días en {place.name}:\n'
                                    f'{str(measures.pdia_14d_rate)}',
                                    reply_markup=ReplyKeyboardRemove())


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
                                            reply_markup=ReplyKeyboardRemove())


def error(update, context):
    """Log Errors caused by Updates."""
    logger.exception(context.error)

    update.message.reply_text('Ha habido un error :(')
