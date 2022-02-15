#!/usr/bin/environment python
import logging

from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, MessageHandler, Updater

from bot import static, places
from config import environment

logging.basicConfig(format='%(asctime)s- %(levelname)s - %(message)s',
                    level=logging.INFO)


def start_bot():
    """Start the bot"""

    updater = Updater(environment.TOKEN)

    dp = updater.dispatcher
    dp.add_handler(places.conv_handler)
    dp.add_handler(CommandHandler('start', static.start))
    dp.add_handler(MessageHandler(Filters.text, static.query_cases))
    dp.add_handler(CallbackQueryHandler(static.button))
    dp.add_handler(CommandHandler('help', static.help))
    
    dp.add_error_handler(static.error)

    # Decide whether to use webhooks or polling
    if environment.USE_WEBHOOKS:
        parameters = {
            'listen': '0.0.0.0',
            'port': environment.PORT,
            'url_path': environment.TOKEN
        }

        if environment.USE_PROXY:
            updater.start_webhook(**parameters)
            updater.bot.set_webhook(f'{environment.APP_URL}{environment.TOKEN}')
        else:
            updater.start_webhook(
                **parameters,
                webhook_url=f'{environment.APP_URL}{environment.TOKEN}',
                key='private.key',
                cert='cert.pem'
            )
    else:
        updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    start_bot()
