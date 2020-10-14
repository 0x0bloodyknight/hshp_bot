# -*- coding: utf-8 -*-

# pyTelegramBotAPI
import telebot

import threading

import logging
import traceback


import config  # config with bot api token

help_text = '''\n/isup - перевірка працездатності бота. Показує де бот зараз працює. \n/purge_nsfw - пересилає в хшп нсфв, а згодом видаляє всі повідомлення від даного до того на яке відповіли.\n/nsfw - пересилає в хшп нсфв, а згодом видаляє повідомлення на яке відповіли.\n'''

logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.

bot = telebot.AsyncTeleBot(config.token, parse_mode=None)


def forward_to_nsfw(message):
    try:
        bot.forward_message(chat_id=config.hshp_nsfw_id,
                            from_chat_id=config.hshp_id, message_id=message.reply_to_message.message_id).wait()
        bot.delete_message(
            config.hshp_id, message.reply_to_message.message_id)
    except AttributeError:
        bot.reply_to(
            message, text='ТИ ЛЮДИНА ЧИ КОМПЮТОР?')


@bot.message_handler(commands=['nsfw'], func=lambda message: message.chat.id == config.hshp_id)
def forward_to_nsfw_handler(message):
    forward_to_nsfw_thread = threading.Thread(
        target=forward_to_nsfw, args=(message,))
    forward_to_nsfw_thread.start()


def forward_to_nsfw_with_purge(message):
    try:
        message_id_to = message.message_id
        purge_range = 0
        try:
            message_id_from = message.reply_to_message.message_id
            purge_range = range(message_id_from, message_id_to)
        except AttributeError:
            bot.reply_to(
                message, text='ТИ ЛЮДИНА ЧИ КОМПЮТОР?')
        if purge_range != 0:
            for i in purge_range:
                try:
                    bot.forward_message(
                        chat_id=config.hshp_nsfw_id, from_chat_id=config.hshp_id, message_id=i).wait()
                    bot.delete_message(config.hshp_id, i)
                except Exception as e:
                    logger.error(type(e).__name__ + " occurred, args=" +
                                str(e.args) + "\n" + traceback.format_exc())
    except Exception as e:
        logger.error(type(e).__name__ + " occurred, args=" +
                    str(e.args) + "\n" + traceback.format_exc())


@bot.message_handler(commands=['purge_nsfw'], func=lambda message: message.chat.id == config.hshp_id)
def forward_to_nsfw_with_purge_handler(message):
    forward_to_nsfw_with_purge_thread = threading.Thread(
        target=forward_to_nsfw_with_purge, args=(message,))
    forward_to_nsfw_with_purge_thread.start()


def is_up_bot(message):
    bot.reply_to(message, text='Так! Бот працює на: {}'.format(config.host))


@bot.message_handler(commands=['isup'])
def is_bot_up_handler(message):
    is_bot_up_thread = threading.Thread(target=is_up_bot, args=(message,))
    is_bot_up_thread.start()


def help_message(message):
    bot.reply_to(message, text=help_text)


@bot.message_handler(commands=['help'])
def help_message_handler(message):
    help_message_thread = threading.Thread(
        target=help_message, args=(message,))
    help_message_thread.start()

bot.polling()
