#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
import logging
import environment

import web_scrapper
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def casos(update, context):
    """Send a message when the command /incidencia is issued."""
    update.message.reply_text(
        f'''Casos por 100.000 habitantes acumulados en 14 días:
            {web_scrapper.get_malaga_pdia_14d()}''')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""

    USE_PROXY = environment.get_bool('USE_PROXY')
    USE_WEBHOOKS = environment.get_bool('USE_WEBHOOKS', True)
    TOKEN = os.getenv('TOKEN')
    APP_URL = os.getenv('APP_URL')

    # Port is given by Heroku
    PORT = int(os.environ.get('PORT', '8443'))

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("casos", casos))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if USE_WEBHOOKS:
        parameters = { 
            "listen": "0.0.0.0",
            "port": PORT,
            "url_path": TOKEN
        }

        if USE_PROXY:
            updater.start_webhook(**parameters)
            updater.bot.set_webhook(f'{APP_URL}{TOKEN}')

        else:
            updater.start_webhook(
                **parameters,
                webhook_url=f'{APP_URL}{TOKEN}',
                key='private.key',
                cert='cert.pem'
            )
        

    else:
        updater.start_polling()

    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
