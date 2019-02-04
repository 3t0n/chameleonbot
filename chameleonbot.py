import telebot
import parser
import config

from apscheduler.schedulers.background import BackgroundScheduler


subscribers = []
scheduler = BackgroundScheduler()
bot = telebot.TeleBot(config.TOKEN)

def scheduler_handler():
    sales = parser.sales()
    for s in subscribers:
        bot.send_message(s, sales)


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Чем могу помочь?')
    if message.contact:
        bot.send_message(message.chat.id, message.contact.phone_number)


@bot.message_handler(commands=['sales'])
def sales_handler(message):
    sales = parser.sales()
    bot.send_message(message.chat.id, sales)


@bot.message_handler(commands=['checks'])
def sales_handler(message):
    checks = parser.checks()
    bot.send_message(message.chat.id, checks)


@bot.message_handler(commands=['test'])
def sales_handler(message):
    test = parser.test()
    bot.send_message(message.chat.id, test)


@bot.message_handler(commands=['subscribe'])
def subscribe_handler(message):
    subscribe = 'Subscribed'
    if subscribers.count(message.chat.id) == 0:
        subscribers.append(message.chat.id)
    else:
        subscribe = 'Already subscribed'

    bot.send_message(message.chat.id, subscribe)


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe_handler(message):
    unsubscribe = 'Unsubscribed'
    if subscribers.count(message.chat.id) > 0:
        subscribers.remove(message.chat.id)
    else:
        unsubscribe = 'Already unsubscribed'

    bot.send_message(message.chat.id, unsubscribe)


@bot.message_handler(commands=['phone'])
def phone_handler(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    reg_button = telebot.types.KeyboardButton(text="Share your phone number", request_contact=True)
    keyboard.add(reg_button)
    bot.send_message(message.chat.id, "You should share your phone number", reply_markup=keyboard)

    # markup = telebot.types.ReplyKeyboardRemove(selective=False)
    # bot.send_message(message.chat.id, message, reply_markup=markup)


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    print(message.contact.phone_number)


scheduler.add_job(scheduler_handler, 'cron', hour=20, minute=15, second=0)
#scheduler.add_job(scheduler_handler, 'cron', second=0)
scheduler.start()

bot.polling(none_stop=True)
scheduler.shutdown()
