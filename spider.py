from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import MessageHandler, Filters
from db import *
from parser import *
from telegram import Update
import re, os, urllib3
import requests
from urllib3.exceptions import InsecureRequestWarning
import time
from datetime import datetime
from compare import compare
from threading import Thread
from time import sleep

init_db()
urllib3.disable_warnings(category=InsecureRequestWarning)
os.system('rm -rf /home/lucky/Downloads/*')

def start(update: Update, context: CallbackContext):
    if not user_exist(update):
        create_user(update)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Добро пожаловать !\n\n'
        '/targets - список целей \n/add - добавить\n/delete - удалить\n\n/check - принудительная проверка\n\n/ignores - все регекспы\n/add_ignore - добавить регексп\n/delete_ignore - удалить регексп ')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Привет, ' + update.effective_user.first_name + '\n'
        'Скучал по тебе ;) \n\n/targets - список целей \n/add - добавить\n/delete - удалить \n\n/check - принудительная проверка\n\n/ignores - все регекспы\n/add_ignore - добавить регексп\n/delete_ignore - удалить регексп')


def echo(update: Update, context: CallbackContext):
    if not user_exist(update):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Я тебя не знаю, напиши /start')
    else:
        if user_is_edit(update) == 'no':
            context.bot.send_message(chat_id=update.effective_chat.id, text='Извини, я понимаю только эти команды'
            ' \n\n/targets - список целей \n/add - добавить\n/delete - удалить\n\n/check - принудительная проверка\n\n/ignores - все регекспы\n/add_ignore - добавить регексп\n/delete_ignore - удалить регексп')
        elif user_is_edit(update) == 'delete':
            if not target_name_exists(update.message.text):
                context.bot.send_message(chat_id=update.effective_chat.id, text='Этой цели нет в базе')
                user_reset(update)
            else:
                try:
                    delete_target(update.message.text)
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Удалил')
                    user_reset(update)
                except:
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Ошибка')
        elif user_is_edit(update) == 'add':
            if check_link_flag(update):
                if re.findall("(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", update.message.text, re.X):
                    name = get_temp_name(update)
                    link = update.message.text
                    try:
                        add_target(name, link)
                        context.bot.send_message(chat_id=update.effective_chat.id, text='Добавил')
                    except:
                        context.bot.send_message(chat_id=update.effective_chat.id, text='Ошибка')

                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Я поддерживаю ссылки ввида https://domain.com, http://domain.ru/admin или www.domain.ru/admin. Не могу распознать вашу ссылку.')
                user_reset(update)
            else:
                name = update.message.text
                if target_name_exists(name):
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Эта цель уже существует')
                    user_reset(update)
                else:
                    set_temp_name(update, name)
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Теперь напиши ссылку')
                    link_flag_reset(update)
        elif user_is_edit(update) == 'add_regexp':
            if check_regexp_flag(update):
                if re.compile(update.message.text):
                    name = get_temp_name(update)

                    regexp = update.message.text

                    try:
                        add_regexp(name, regexp)
                        context.bot.send_message(chat_id=update.effective_chat.id, text='Добавил')
                    except:
                        context.bot.send_message(chat_id=update.effective_chat.id, text='Ошибка')

                else:
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text='Что-то вы напортачили с регекспом')
                user_reset(update)
            else:
                name = update.message.text
                if regexp_name_exists(name):
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Название для регекспа уже занято')
                    user_reset(update)
                else:
                    set_temp_name(update, name)
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Теперь напиши регулярное выражение')
                    regexp_flag_reset(update)
        elif user_is_edit(update) == 'delete_regexp':
            if not regexp_name_exists(update.message.text):
                context.bot.send_message(chat_id=update.effective_chat.id, text='Этой цели нет в базе')
                user_reset(update)
            else:
                try:
                    delete_regexp(update.message.text)
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Удалил')
                    user_reset(update)
                except:
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Ошибка')


def add(update: Update, context: CallbackContext):
    if not user_exist(update):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Я тебя не знаю, напиши /start')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Назови цель и я добавлю её')
        user_add(update)

def add_ignore(update: Update, context: CallbackContext):
    if not user_exist(update):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Я тебя не знаю, напиши /start')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Дай регекспу название')
        regexp_add(update)

def delete_ignore(update: Update, context: CallbackContext):
    if not user_exist(update):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Я тебя не знаю, напиши /start')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Назови имя регекспа и я забуду про него')
        regexp_delete(update)

def delete(update: Update, context: CallbackContext):
    if not user_exist(update):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Я тебя не знаю, напиши /start')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Назови цель и я забуду про неё')
        user_delete(update)

def targets(update: Update, context: CallbackContext):
    targets = get_targets()
    if len(targets) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='В моём списке ещё нет целей')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='В моём списке есть такие цели -->\n\n' + str(targets))

def regexp_ignores(update: Update, context: CallbackContext):
    ignores = get_ignores()
    if len(ignores) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='В моём списке ещё нет регулярных выражений')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='В моём списке есть такие регулярные выражения -->\n\n' + str(ignores))


def check(update: Update, context: CallbackContext):
    os.system('rm -rf /home/lucky/Downloads/*')
    targets = get_targets()
    if len(targets) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Мне нечего чекать ;(')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Начинаю чекать...')

        for link in get_links():
            os.system('rm -rf /home/lucky/Downloads/*')
            url = link[0]

            error = False

            try:
                requests.get(url, timeout=(3,3), verify=False)
            except:
                error = True

            if error == True:
                context.bot.send_message(chat_id=update.effective_chat.id, text=url + ' недоступен')
            else:
                try:
                    download(url)

                    name = re.search("^https?:\/\/?([\w-]{1,32})\.[\w-]{1,32}[^\s@]*$", url).group(1)

                    dir_name = '/tmp/temp/' + name + '_' + str(int(time.time()))
                    os.mkdir(dir_name)
                    os.system('mv /home/lucky/Downloads/* ' + dir_name)

                    context.bot.send_message(chat_id=update.effective_chat.id, text=url + ' успешно')

                    result = compare(name)
                    if result == None:
                        pass
                    else:
                        f = open('logs.txt', 'a')
                        f.write('\n' + str(datetime.now().date()) + ' ' + result + '\n---------------------------------------------')

                        f.close()
                        context.bot.send_message(chat_id=update.effective_chat.id, text=result)


                except Exception as e:
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Не смог прочекать ;(\n\n' + str(e))


def notifications(notify='test'):
    chats = get_chats()
    for chat in chats:
        requests.get('https://api.telegram.org/bot/sendMessage?chat_id={}&text={}'.format(chat[0],notify))
        sleep(0.5)

def parser():
    while True:
        sleep(60*60*24)

        os.system('rm -rf /home/lucky/Downloads/*')
        targets = get_targets()

        for link in get_links():
            os.system('rm -rf /home/lucky/Downloads/*')
            url = link[0]

            error = False

            try:
                requests.get(url, timeout=(3,3), verify=False)
            except:
                error = True

            if error == True:
                f = open('logs.txt', 'a')
                f.write('\n' + str(
                    datetime.now().date()) + ' ' + link + ' недоступен' '\n---------------------------------------------')
                f.close()
            else:
                try:
                    download(url)
                    name = re.search("^https?:\/\/?([\w-]{1,32})\.[\w-]{1,32}[^\s@]*$", url).group(1)

                    dir_name = '/tmp/temp/' + name + '_' + str(int(time.time()))
                    os.mkdir(dir_name)
                    os.system('mv /home/lucky/Downloads/* ' + dir_name)

                    result = compare(name)
                    if result == None:
                        pass
                    else:
                        f = open('logs.txt', 'a')
                        f.write('\n' + str(datetime.now().date()) + ' ' + result + '\n---------------------------------------------')
                        note = '\n' + str(datetime.now().date()) + ' ' + result + '\n---------------------------------------------'
                        notifications(notify=note)
                        f.close()
                except Exception as e:
                    f = open('logs.txt', 'a')
                    f.write('\n' + str(
                        datetime.now().date()) + ' ' + link + ' ошибка ' + str(e) + '\n---------------------------------------------')
                    f.close()






def logs(update: Update, context: CallbackContext):
    f = open('logs.txt', 'r')
    lines = f.readlines()
    f.close()

    buf = ''
    for line in lines:
        buf += line

    slash_split = buf.split('---------------------------------------------\n')

    done = ''

    count = 0
    for line in reversed(slash_split):
        if count >= 10:
            break
        count += 1
        done += line
        done += '\n'


    context.bot.send_message(chat_id=update.effective_chat.id, text=done)

def main():
    updater = Updater(token='', use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler('targets', targets))
    dispatcher.add_handler(CommandHandler('add', add))
    dispatcher.add_handler(CommandHandler('delete', delete))

    dispatcher.add_handler(CommandHandler('ignores', regexp_ignores))
    dispatcher.add_handler(CommandHandler('add_ignore', add_ignore))
    dispatcher.add_handler(CommandHandler('delete_ignore', delete_ignore))

    dispatcher.add_handler(CommandHandler('check', check))

    dispatcher.add_handler(CommandHandler('logs', logs))

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()

    parse_thread = Thread(target=parser)
    parse_thread.setDaemon(True)
    parse_thread.start()
    parse_thread.join()

if __name__ == '__main__':
    main()
