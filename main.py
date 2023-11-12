import telebot
import os
from telebot import types
from datetime import datetime
from Data import Data

MONTH = datetime.now().strftime("%m")
MES = datetime.now().strftime("%b")
TOKEN_TELEGRAM = os.environ.get("TELEGRAM_TOKEN")
GETME = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/getMe"

bot = telebot.TeleBot(TOKEN_TELEGRAM, parse_mode=None)
data = Data()


def menu(mensaje):
    markup = types.ReplyKeyboardMarkup()
    fila1a = types.KeyboardButton('Registrar gasto')
    fila1b = types.KeyboardButton('Hacer Cuentas')
    fila2a = types.KeyboardButton('Apañar Cuentas')
    fila2b = types.KeyboardButton('Ver ayuda')
    markup.row(fila1a, fila1b)
    markup.row(fila2a, fila2b)
    bot.send_message(mensaje.from_user.id, "Elige una opción:", reply_markup=markup)


def menu_gasto(mensaje):
    markup = types.ReplyKeyboardMarkup()
    fila1a = types.KeyboardButton('160€')
    fila1b = types.KeyboardButton('150€')
    fila1c = types.KeyboardButton('140€')
    fila1d = types.KeyboardButton('130€')
    fila1e = types.KeyboardButton('120€')
    fila1f = types.KeyboardButton('110€')
    fila2a = types.KeyboardButton('100€')
    fila2b = types.KeyboardButton('90€')
    fila2c = types.KeyboardButton('80€')
    fila2d = types.KeyboardButton('70€')
    fila2e = types.KeyboardButton('60€')
    fila2f = types.KeyboardButton('50€')
    fila3a = types.KeyboardButton('479,58€')
    fila3b = types.KeyboardButton('Otra cantidad')
    fila3c = types.KeyboardButton('Volver al Menú')
    markup.row(fila1a, fila1b, fila1c, fila1d, fila1e, fila1d, fila1f)
    markup.row(fila2a, fila2b, fila2c, fila2d, fila2e, fila2f)
    markup.row(fila3a, fila3b, fila3c)
    bot.send_message(mensaje.from_user.id, "¿Cuánto te has gastado?", reply_markup=markup)


@bot.message_handler(commands=["empezar"])
def empezar(message):
    menu(message)


@bot.message_handler(func=lambda m: True)
def gestionar_mensajes(message):
    if message.text == "Registrar gasto":
        menu_gasto(message)
    elif message.text == "100€" or message.text == "50€" or message.text == "479,58€" or message.text.replace("€",
                                                                                                              "").replace(
        ",", ".").replace(".", "").strip().isdigit():
        gasto = float(message.text.replace("€", "").replace(",", "."))
        nombre = str(message.from_user.first_name)
        data.write(gasto, nombre, MONTH)
        if data.response.status_code == 201:
            bot.send_message(message.from_user.id, 'Gasto añadido.\nPulsa empezar si quieres hacer algo más.')
        else:
            bot.send_message(message.from_user.id, 'Algo ha fallado, no se ha añadido el gasto.')

    elif message.text == 'Otra cantidad':
        bot.send_message(message.from_user.id, 'Cuánto?')

    elif message.text == 'Hacer Cuentas':
        data.get_data()
        bot.send_message(message.from_user.id,
                         f'En el mes de {MES},\nGasto Esti: {data.gasto_esti}€\nGasto Quique: {data.gasto_qq}€')

    elif message.text == 'Volver al Menú':
        menu(message)

    elif message.text == 'Apañar Cuentas':
        data.apañar_cuentas()
        bot.send_message(message.from_user.id,
                         f'Apañado!')


@bot.message_handler(commands=['cuentas'])
def send_archivo(message):
    with open("texto.txt", "r") as f:
        response = f.read()
    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Esto es la ayuda.")



bot.infinity_polling(interval=0, timeout=20)

