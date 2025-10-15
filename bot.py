import os
import telebot
from telebot import types

# ====== CONFIGURAÇÕES ======
TOKEN = os.getenv("BOT_TOKEN")  # Defina no ambiente da Vercel/Fly.io
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # Seu ID (para logs e avisos)
BANNED_WORDS = ["palavrão1", "proibido", "spam", "linkerrado"]  # Edite suas palavras

# ====== BOT ======
bot = telebot.TeleBot(TOKEN)

# ====== SISTEMA DE PUNIÇÕES ======
def aplicar_punicao(message, motivo):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    try:
        # Exemplo: apaga a mensagem
        bot.delete_message(chat_id, message.message_id)

        # Exemplo: aplica banimento temporário
        bot.restrict_chat_member(
            chat_id,
            user_id,
            until_date=None,  # None = permanente, ou use int(time.time()) + segundos
            permissions=types.ChatPermissions(can_send_messages=False)
        )

        # Envia aviso no grupo
        bot.send_message(chat_id, f"⚠️ @{username} foi silenciado por usar palavra proibida.\nMotivo: {motivo}")

        # Loga para o admin
        if ADMIN_ID:
            bot.send_message(ADMIN_ID, f"[LOG] @{username} foi punido em {chat_id} - Motivo: {motivo}")

    except Exception as e:
        print(f"Erro ao aplicar punição: {e}")

# ====== MONITORAMENTO ======
@bot.message_handler(func=lambda m: True)
def monitorar_mensagens(message):
    texto = message.text.lower()
    for palavra in BANNED_WORDS:
        if palavra in texto:
            aplicar_punicao(message, f"Usou a palavra '{palavra}'")
            break

# ====== COMANDO /start ======
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "🤖 Olá! Sou o bot de moderação. Envio aviso e punições automáticas.")

# ====== RODAR LOCALMENTE ======
if __name__ == "__main__":
    print("Bot rodando...")
    bot.infinity_polling(skip_pending=True)
