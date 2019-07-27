from pathlib import Path
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import urllib.request
import json

OWNER ='@Valery_Selikhov'
TOKEN_FILE = 'token.txt'
token = Path(TOKEN_FILE).read_text().strip()

EXCHANGE_RATE_URL = 'http://resources.finance.ua/ua/public/currency-cash.json'


def start(update, context):
    """Command handler for command /start"""
    print('Command /start')
    update.message.reply_text(f'Привет, я персональный бот, мой шеф {OWNER}')


def buy_usd(update, context):
    """Message handler for buying USD"""

    msq = update.message
    msq.bot.send_message(msq.chat_id, 'Я знаю, чего ты хочешь!')

    text = urllib.request.urlopen(EXCHANGE_RATE_URL).read()
    data = json.loads(text)
    sellers = [o for o in data['organizations'] if 'USD' in o['currencies']]
    sellers.sort(key=lambda o: float(o['currencies']['USD']['ask']))
    best = sellers[0]

    msq.bot.send_message(msq.chat_id, f'Лучший курс:  {best["currencies"]["USD"]["ask"]}\n{best["link"]}')

def main():

    updater = Updater(token=token, use_context=True)
    dp  = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.regex('Купить доллары'), buy_usd))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()



# import pdb; pdb.set_trace()

