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

import pandas as pd

import responses as resp
import config as keys
import keyboards as kb

# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler
# from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData

from bs4 import BeautifulSoup
import requests
from pprint import pprint

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# def error(update: Update, context: CallbackContext):
#     """Log Errors caused by Updates."""
#     logger.warning(f'Update {update} caused error {context.error}')


class Auto(StatesGroup):
    waiting_for_brand = State()
    waiting_for_model = State()


dbs = []
def main():
    db = pd.read_csv('autos.csv')
    dbs = []
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        srch = types.KeyboardButton('/search')
        markup.add(srch)
        await bot.send_message(message.chat.id, 'Привет! Я бот для поиска авто на auto.ria.com\nЧтобы создать запрос '
                                                'нажми на кнопку поиска', reply_markup=markup)

    @dp.message_handler(commands=['rm'])
    async def process_rm_command(message: types.Message):
        await message.reply("Removing message templates", reply_markup=kb.ReplyKeyboardRemove())

    @dp.message_handler(commands=['help'])
    async def process_help_command(message: types.Message):
        await message.reply("Write me something and I will send this text back to you!")

    #####
    @dp.message_handler(commands=['search'])
    async def search(message: types.Message):
        await bot.send_message(message.chat.id, 'Какая марка Вас интересует?')
        brands = [
            b.replace('-', '_').replace('ЗАЗ', 'ZAZ').replace('ВАЗ', 'VAZ').replace('ГАЗ', 'GAZ')
            for b in db["Brand"].unique()
        ]
        brands = sorted(brands)
        brands[0] = '/' + brands[0]

        await message.answer(
            '/'.join([f'{b}\n' for b in brands])
        )

    @dp.message_handler(content_types=['text'])
    async def models(message):
        # if message.text == 'Поиск авто! 🚗':
        #     await search(message)
        if message.text[1::].replace('_', '-') in db['Brand'].unique():
            brand = message.text[1::]
            brand = brand.replace('_', '-')
            print(brand)

            await bot.send_message(message.chat.id, "Какая модель Вас интересует?")

            models = []
            for model in db[db['Brand'] == brand]['Model'].values:
                model = model.split()[0].replace("-", "_")
                if model not in models:
                    models.append(model)
            models = sorted(models)
            models[0] = '/' + models[0]

            await message.answer(
                '/'.join([f'{m}\n' for m in models])
            )

        elif message.text[1::].replace('_', '-') in db['Model'].str.split(' ', 1, expand=True)[0].values:
            model = message.text[1::]
            model = model.replace('_', '-')
            print(model)
            dbs.append(db[db['Model'].str.split(' ', 1, expand=True)[0].values == model])

            await bot.send_message(message.chat.id, 'Какой год выпуска Вас интересует?')

            years = []
            for year in db[db['Model'].str.split(' ', 1, expand=True)[0].values == model]['Year'].values:
                if year not in years:
                    years.append(year)
            years = sorted(years)
            years[0] = '/' + years[0].astype(str)

            await message.answer(
                '/'.join([f'{str(years[i])}\n' for i in range(0, len(years))])
            )

        elif int(message.text[1::]) in db['Year'].values:
            year = int(message.text[1::])
            print(year)

            await bot.send_message(message.chat.id, 'Предложения по вашему запросу')
            dbs.append(dbs[0][db['Year'] == year]['Link'])
            for link in dbs[0][db['Year'] == year]['Link']:

                await bot.send_message(message.chat.id, f'{link}')

            dbs.clear()


    #########
    # # log all errors
    # dispatcher.add_error_handler(error)

    # Start the Bot
    executor.start_polling(dp)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()


if __name__ == '__main__':
    main()
