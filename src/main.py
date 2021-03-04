#!/usr/bin/env python

import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import environment
import handlers
from models import init_db

USE_PROXY = environment.get_bool('USE_PROXY')
USE_WEBHOOKS = environment.get_bool('USE_WEBHOOKS', True)
TOKEN = os.getenv('TOKEN')
APP_URL = os.getenv('APP_URL')
DB_URL = os.environ.get('DB_URL', f'sqlite:///test.db')
PORT = int(os.environ.get('PORT', '8443'))  # Port is given by Heroku
DEBUG = environment.get_bool('DEBUG', False)


def main():
    """Start the bot."""

    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", handlers.start))
    dp.add_handler(CommandHandler("help", handlers.help))
    dp.add_handler(CommandHandler("casos", handlers.casos))
    dp.add_handler(MessageHandler(Filters.text, handlers.echo))
    dp.add_error_handler(handlers.error)

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

    updater.idle()


if __name__ == '__main__':
    init_db(DB_URL, DEBUG)
    main()
