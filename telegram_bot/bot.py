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
import config as keys
import keyboards as kb

# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler
# from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from bs4 import BeautifulSoup
import requests
from pprint import pprint

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
# def caps_command(update: Update, context: CallbackContext):
#     text_caps = ' '.join(context.args).upper()
#     context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
#
#
# def inline_caps(update: Update, context: CallbackContext):
#     query = update.inline_query.query
#     if not query:
#         return
#     results = []
#     results.append(
#         InlineQueryResultArticle(
#             id=query.upper(),
#             title='Caps',
#             input_message_content=InputTextMessageContent(query.upper())
#         )
#     )
#     context.bot.answer_inline_query(update.inline_query.id, results)
#
#
# def unknown_command(update: Update, context: CallbackContext):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
#
#
# def error(update: Update, context: CallbackContext):
#     """Log Errors caused by Updates."""
#     logger.warning(f'Update {update} caused error {context.error}')
#
#
# def handle_message(update: Update, context: CallbackContext):
#     text = str(update.message.text).lower()
#     response = resp.sample_responses(text)
#     update.message.reply_text(response)
#
#
# def getBikes(text):
#     url = 'https://bikefair.org/listings?currency=EUR&cash_payments=false&country_code=&delivery_distance=10&price%5B0%5D=29&price%5B1%5D=6119&frame_size%5B0%5D=481&frame_size%5B1%5D=549&wheel_size%5B0%5D=534&wheel_size%5B1%5D=548&height=&bike_brand%5B0%5D=80&page=1&sort%5Bkey%5D=best_match&sort%5Bdirection%5D=asc'

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    bot = Bot(token=keys.TOKEN)

    # Get the dispatcher to register handlers
    dp = Dispatcher(bot)

    ##
    @dp.callback_query_handler(lambda c: c.data == 'button1')
    async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'First button pressed!')

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
    async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
        code = callback_query.data[-1]
        if code.isdigit():
            code = int(code)
        if code == 2:
            await bot.answer_callback_query(callback_query.id, text='Second button pressed')
        elif code == 5:
            await bot.answer_callback_query(
                callback_query.id,
                text='Button 5 pressed.\nAnd this text can be up to 200 characters long 😉', show_alert=True)
        else:
            await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, f'Inline button pressed! code={code}')

    ##
    # on different commands - answer in Telegram
    @dp.message_handler(commands=['start'])
    async def process_start_command(message: types.Message):
        await message.reply("Hi!", reply_markup=kb.greet_kb)

    @dp.message_handler(commands=['hi1'])
    async def process_hi1_command(message: types.Message):
        await message.reply("First - change the size of keyboard", reply_markup=kb.greet_kb1)

    @dp.message_handler(commands=['hi2'])
    async def process_hi2_command(message: types.Message):
        await message.reply("Second - hide the keyboard after one press", reply_markup=kb.greet_kb2)

    @dp.message_handler(commands=['hi3'])
    async def process_hi3_command(message: types.Message):
        await message.reply("Third - add more buttons", reply_markup=kb.markup3)

    @dp.message_handler(commands=['hi4'])
    async def process_hi4_command(message: types.Message):
        await message.reply("Fourth - arrange the buttons in a row", reply_markup=kb.markup4)

    @dp.message_handler(commands=['hi5'])
    async def process_hi5_command(message: types.Message):
        await message.reply("Fifth - add rows of buttons", reply_markup=kb.markup5)

    @dp.message_handler(commands=['hi6'])
    async def process_hi6_command(message: types.Message):
        await message.reply("Sixth - request contact and geolocation\nThese two buttons are independent of each other.",
                            reply_markup=kb.markup_request)

    @dp.message_handler(commands=['hi7'])
    async def process_hi7_command(message: types.Message):
        await message.reply("Seventh - all methods together", reply_markup=kb.markup_big)

    @dp.message_handler(commands=['rm'])
    async def process_rm_command(message: types.Message):
        await message.reply("Removing message templates", reply_markup=kb.ReplyKeyboardRemove())

    @dp.message_handler(commands=['1'])
    async def process_command_1(message: types.Message):
        await message.reply("First inline button", reply_markup=kb.inline_kb1)

    @dp.message_handler(commands=['2'])
    async def process_command_2(message: types.Message):
        await message.reply("Send all possible buttons", reply_markup=kb.inline_kb_full)

    @dp.message_handler(commands=['help'])
    async def process_help_command(message: types.Message):
        await message.reply("Write me something and I will send this text back to you!")

    # # on noncommand i.e message - echo the message on Telegram
    # @dp.message_handler()
    # async def echo_message(msg: types.Message):
    #     await bot.send_message(msg.from_user.id, msg.text)

    # on noncommand message - reply the message
    # reply_handler = MessageHandler(Filters.text, handle_message)
    # dispatcher.add_handler(reply_handler)
    #
    # # reply text in CAPS
    # caps_handler = CommandHandler('caps', caps_command)
    # inline_caps_handler = InlineQueryHandler(inline_caps)
    #
    # dispatcher.add_handler(caps_handler)
    # dispatcher.add_handler(inline_caps_handler)
    #
    # # log all errors
    # dispatcher.add_error_handler(error)
    #
    # # command filter  to reply to all commands that were not recognized by the previous handlers
    # unknown_handler = MessageHandler(Filters.command, unknown_command)
    # dispatcher.add_handler(unknown_handler)

    # Start the Bot
    executor.start_polling(dp)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()


if __name__ == '__main__':
    main()