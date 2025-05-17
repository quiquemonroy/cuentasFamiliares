# 💰 Bot de Gestión de Gastos Familiares 🤖
<img width="460" alt="image" src="https://github.com/user-attachments/assets/9c254459-5660-41e3-84f9-735fad6cba93" />

Un bot de Telegram para registrar y gestionar gastos compartidos entre parejas/familiares, con integración directa a Google Sheets.

![Captura del bot](https://via.placeholder.com/400x200?text=Interfaz+del+Bot+de+Gastos)

## ✨ Características principales

- 📊 Registro automático de gastos en una hoja de cálculo compartida
- ⚖️ Sistema de balance para saber quién debe a quién
- 💰 Preconfiguración de cantidades frecuentes
- 🔔 Notificaciones al otro miembro cuando se registra un gasto
- 📅 Organización por meses automática
- 📱 Interfaz intuitiva mediante menús interactivos

## 🔧 Requisitos técnicos

- Python 3.7+
- Librerías: `python-telegram-bot`, `gspread`
- Cuenta de servicio de Google Sheets API
- Token de bot de Telegram

## 🚀 Configuración inicial

1. Crear un bot de Telegram con @BotFather y obtener el token
2. Configurar las variables de entorno necesarias:
   ```bash
   export TELEGRAM_TOKEN="tu_token_aqui"
   export ID_QUIQUE="tu_chat_id"
   export ID_ESTI="otro_chat_id"
   export ID_COMPARAR="chat_id_comparacion"
   ```
3. Instalar dependencias:
   ```bash
   pip install python-telegram-bot gspread oauth2client
   ```

## 🛠 Funcionalidades principales

### 📝 Registrar gastos
- Menú con cantidades predefinidas para registro rápido
- Opción para introducir cantidades personalizadas
- Notificación automática al otro usuario

### 📊 Hacer cuentas
- Resumen mensual de gastos por persona
- Cálculo automático de balances
- Visualización clara de quién debe a quién

### ⚖ Apañar cuentas
- Registro de pagos entre miembros
- Confirmación para evitar errores
- Notificación al otro usuario

## 📂 Estructura del código

- **Integración con Telegram**: Uso de `python-telegram-bot` para manejar comandos y mensajes
- **Google Sheets**: Clase `Data` para interactuar con la hoja de cálculo
- **Menús interactivos**: Teclados personalizados para mejor experiencia de usuario
- **Gestión de tiempo**: Filtrado automático por mes actual

## 📌 Notas importantes

- El bot requiere configuración previa de la API de Google Sheets
- Los IDs de chat son necesarios para las notificaciones
- La hoja de cálculo debe tener una estructura específica

## 📜 Licencia

Este proyecto está bajo licencia MIT.

---

🤖 Desarrollado por Quique para gestión familiar de gastos compartidos.
