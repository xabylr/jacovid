import logging

from persistence import database
from persistence.models.measures import Measures

logger = logging.getLogger()


def start(update, context):
    """Send a message when the command /start is issued."""

    update.message.reply_text('Hi!')


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

def echo(update, context):
    """Echo the user message."""

    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""

    logger.warning('Update "%s" caused error "%s"', update, context.error)
