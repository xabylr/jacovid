#!/usr/bin/env python
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import persistence.database as db
import config.environment as env
import bot.handlers as handlers


def start_bot():
    """Start the bot"""

    db.connect(env.DB_URL, env.DEBUG)

    updater = Updater(env.TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", handlers.start))
    dp.add_handler(CommandHandler("help", handlers.help))
    dp.add_handler(CommandHandler("casos", handlers.casos))
    dp.add_handler(MessageHandler(Filters.text, handlers.echo))
    dp.add_error_handler(handlers.error)

    # Decide whether to use webhooks or polling
    if env.USE_WEBHOOKS:
        parameters = {
            "listen": "0.0.0.0",
            "port": env.PORT,
            "url_path": env.TOKEN
        }

        if env.USE_PROXY:
            updater.start_webhook(**parameters)
            updater.bot.set_webhook(f'{env.APP_URL}{env.TOKEN}')
        else:
            updater.start_webhook(
                **parameters,
                webhook_url=f'{env.APP_URL}{env.TOKEN}',
                key='private.key',
                cert='cert.pem'
            )
    else:
        updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    start_bot()
