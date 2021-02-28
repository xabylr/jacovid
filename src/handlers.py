import logging

import web_scrapper

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""

    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""

    update.message.reply_text('Help!')


def casos(update, context):
    """Send a message when the command /casos is issued."""
    # session = get_session()
    # moto = session.query(Moto).filter_by(id=1).one()

    update.message.reply_text(
        f'''Casos por 100.000 habitantes acumulados en 14 días:
            {web_scrapper.get_malaga_pdia_14d()}''')


def echo(update, context):
    """Echo the user message."""

    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""

    logger.warning('Update "%s" caused error "%s"', update, context.error)
