import telebot
import os
from telebot import types
from datetime import datetime
from Data_stein import Data
from telebot.util import quick_markup
import time

# ESTO ES UNA PRUEBA
MONTH = datetime.now().strftime("%m")
MES = datetime.now().strftime("%b")
TOKEN_TELEGRAM = os.environ.get("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TOKEN_TELEGRAM, parse_mode="html")
data = Data()


def menu(mensaje):
    texto_menu = """<b>💸💸CUENTAS FAMILIARES💸💸</b>
    
    --Usa el menú para elegir qué hacer.--
    
    🔴Si has gastado algo de dinero y quieres apuntarlo, haz click en Registrar gasto.
    
    🔴Hacer cuentas muestra un resumen de lo que hemos gastado cada una este mes.
    
    🔴Apañar cuentas sirve para registrar cuando ya has hecho bizum o algo así.
    
    🔴Ver ayuda muestra la ayuda.
    
    🔴Ver datos en excel muestra un link para acceder al excel donde se guardan los datos."""
    markup = types.ReplyKeyboardMarkup()
    fila1a = types.KeyboardButton('Registrar gasto\n💸')
    fila1b = types.KeyboardButton('Hacer Cuentas\n📄')
    fila2a = types.KeyboardButton('Apañar Cuentas\n⚖️')
    fila2b = types.KeyboardButton('Ver ayuda\n⁇')
    fila2c = types.KeyboardButton('Ver datos en excel\n👁️')
    markup.row(fila1a, fila1b)
    markup.row(fila2a, fila2b, fila2c)
    bot.send_message(mensaje.from_user.id, texto_menu, reply_markup=markup)


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




def apanar_cuentas(mensaje):
    markup = types.ReplyKeyboardMarkup()
    fila1a = types.KeyboardButton('Sí, ya he hecho bizum')
    fila1b = types.KeyboardButton('Nop, aún no.')
    markup.row(fila1a, fila1b)
    bot.send_message(mensaje.from_user.id, """<b>¿SEGURO?</b>
    
    
     Si continúas, en el excel se escribirá un gasto en tu nombre.
     
     
     Dale a Sí sólo si ya has hecho bizum o transferencia. """, reply_markup=markup)


@bot.message_handler(commands=["menu"])
def empezar(message):
    menu(message)


@bot.message_handler(func=lambda m: True)
def gestionar_mensajes(message):
    if message.text == "Registrar gasto\n💸":
        menu_gasto(message)
    elif message.text == "100€" or message.text == "50€" or message.text == "479,58€" or message.text.replace("€",
                                                                                                              "").replace(
        ",", ".").replace(".", "").strip().isdigit():
        gasto = float(message.text.replace("€", "").replace(",", "."))
        nombre = str(message.from_user.first_name)
        data.write(gasto, nombre, MONTH)
        if data.response.status_code == 200:
            bot.send_message(message.from_user.id, '⚡⚡Gasto añadido.⚡⚡️')
            time.sleep(3)
            menu(message)
        else:
            bot.send_message(message.from_user.id, 'Algo ha fallado, no se ha añadido el gasto.')

    elif message.text == 'Otra cantidad':
        bot.send_message(message.from_user.id, 'Cuánto?')

    elif message.text == 'Hacer Cuentas\n📄':
        data.get_data()
        data.hacer_cuentas()
        bot.send_message(message.from_user.id,
                         f'''En el mes de {MES}:
 ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯                            
            🐚🐚Gasto Esti🐚🐚

{data.cuentas_Esti} 

                            <b>TOTAL:{data.gasto_esti}€</b>

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
             🖤🖤Gasto Quique🖤🖤

{data.cuentas_qq}

                            <b>TOTAL:{data.gasto_qq}€</b>
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯''')
        bot.send_message(message.from_user.id, data.quien_debe())

    elif message.text == 'Volver al Menú' or message.text == 'Nop, aún no.':
        menu(message)

    elif message.text == 'Sí, ya he hecho bizum':
        data.apañar_cuentas()
        bot.send_message(message.from_user.id,
                         f'✅✅✅¡Apañado!✅✅✅')
        time.sleep(3)
        menu(message)
    elif message.text == 'Ver datos en excel\n👁️':
        bot.send_message(message.from_user.id,
                         "<a href='https://docs.google.com/spreadsheets/d/1u0aClkvLhxBOBDwAE660FBIjixGPzZO7oOqhAWwkf1Y/edit#gid=0'>👁️VER EXCEL👁️</a>")

    elif message.text == 'Apañar Cuentas\n⚖️':
        apanar_cuentas(message)

    elif message.text == 'Ver ayuda\n⁇':
        bot.send_message(message.from_user.id, 'Escribe aquí ➡️ @this_Is_Fine86\n\nSi te has equivocado en un gasto, puedes borrarlo desde el excel, por ahora.')



bot.infinity_polling(interval=0, timeout=20)
