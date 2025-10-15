import os
import telebot
from telebot import types

# ===== CONFIGURAÇÕES =====
TOKEN = os.getenv("BOT_TOKEN")  # Token do seu bot (adicione no Fly.io)
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # ID do admin (para logs)
BANNED_WORDS = ["palavrão1", "proibido", "spam", "linkerrado"]  # Liste as palavras bloqueadas

bot = telebot.TeleBot(TOKEN)

# ===== FUNÇÃO DE PUNIÇÃO =====
def aplicar_punicao(message, motivo):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    try:
        # Apaga a mensagem
        bot.delete_message(chat_id, message.message_id)

        # Silencia o usuário
        bot.restrict_chat_member(
            chat_id,
            user_id,
            permissions=types.ChatPermissions(can_send_messages=False)
        )

        # Mensagem no grupo
        bot.send_message(chat_id, f"⚠️ @{username} foi silenciado por usar palavra proibida.\nMotivo: {motivo}")

        # Log privado pro admin
        if ADMIN_ID:
            bot.send_message(ADMIN_ID, f"[LOG] @{username} punido em {chat_id} - Motivo: {motivo}")

    except Exception as e:
        print(f"Erro ao aplicar punição: {e}")

# ===== MONITORAMENTO =====
@bot.message_handler(func=lambda m: True)
def monitorar_mensagens(message):
    texto = (message.text or "").lower()
    for palavra in BANNED_WORDS:
        if palavra in texto:
            aplicar_punicao(message, f"Usou a palavra '{palavra}'")
            break

# ===== COMANDO /start =====
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "🤖 Bot de moderação ativo 24h! Mando punições automáticas conforme as regras.")

# ===== EXECUÇÃO =====
if __name__ == "__main__":
    print("Bot rodando...")
    bot.infinity_polling(skip_pending=True)
