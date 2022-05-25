import logging
import requests
from datetime import date

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Olá {user.mention_markdown_v2()}\!, eu sou o bot AcharMinhaFoto, eu procuro fotos baseado em uma data, caso precise de ajuda digite /help',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Para ver a mídia de hoje digite /hoje')
    update.message.reply_text('Para ver a mídia de uma data especifica informe a data da seguinte forma: ano/mês/dia, Ex: 2022-02-16')


def echo(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(fr'{user.mention_markdown_v2()}\ {update.message.text}')

def take_midia(update: Update, context: CallbackContext) -> None:
    data = context.args[0]
    response = requests.get(fr"https://api.nasa.gov/planetary/apod?api_key=fe7GZ9AemfAvLPRuSPtee3bGL82hFBAAHIg33YT4&date={data}")
    json = response.json()
    update.message.reply_text(fr'Data: {json["date"]}')
    update.message.reply_text(fr'Título: {json["title"]}')
    update.message.reply_text(fr'Explicação: {json["explanation"]}')
    update.message.reply_text(fr'{json["hdurl"]}')

def today(update: Update, context: CallbackContext) -> None:
    date_hoje = date.today()
    response = requests.get(fr"https://api.nasa.gov/planetary/apod?api_key=fe7GZ9AemfAvLPRuSPtee3bGL82hFBAAHIg33YT4&date={date_hoje}")
    json = response.json()
    update.message.reply_text(fr'Data: {json["date"]}')
    update.message.reply_text(fr'Título: {json["title"]}')
    update.message.reply_text(fr'Explicação: {json["explanation"]}')
    update.message.reply_text(fr'{json["hdurl"]}')

def main() -> None:
    updater = Updater("5384518261:AAG0uUF4xssoRWiQUC7jOPDlPB9CSclr0bo")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("midia", take_midia))
    dispatcher.add_handler(CommandHandler("hoje", today))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()