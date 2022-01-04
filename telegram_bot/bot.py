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

import logging
import responses as resp

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start_command(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    # update.message.reply_text('Hi!')
    context.bot.send_message(chat_id=update.effective_chat.id, text="Write something to talk to me!")


def help_command(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Do you need help? Please just use Google!')


# def echo(update: Update, context: CallbackContext):
#     """Echo the user message."""
#     # update.message.reply_text(update.message.text)
#     context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def caps_command(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def inline_caps(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


def unknown_command(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')


def handle_message(update: Update, context: CallbackContext):
    text = str(update.message.text).lower()
    response = resp.sample_responses(text)
    update.message.reply_text(response)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token="5049993571:AAGy5pmpdxx-c9bXRyEkbhfnGeoJLGuHIbA", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    start_handler = CommandHandler("start", start_command)
    help_handler = CommandHandler("help", help_command)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)

    # # on noncommand i.e message - echo the message on Telegram
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    # on noncommand message - reply the message
    reply_handler = MessageHandler(Filters.text, handle_message)
    dispatcher.add_handler(reply_handler)

    # reply text in CAPS
    caps_handler = CommandHandler('caps', caps_command)
    inline_caps_handler = InlineQueryHandler(inline_caps)

    dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(inline_caps_handler)

    # log all errors
    dispatcher.add_error_handler(error)

    # command filter  to reply to all commands that were not recognized by the previous handlers
    unknown_handler = MessageHandler(Filters.command, unknown_command)
    dispatcher.add_handler(unknown_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()