import telebot
import parser
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Чем могу помочь?')

@bot.message_handler(commands=['sales'])
def sales_handler(message):
    sales = parser.get_sales()
    bot.send_message(message.chat.id, sales)

@bot.message_handler(commands=['checks'])
def sales_handler(message):
    checks = parser.get_checks()
    bot.send_message(message.chat.id, checks)

@bot.message_handler(commands=['test'])
def sales_handler(message):
    test = parser.get_test()
    bot.send_message(message.chat.id, test)

bot.polling()
