from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import API_TOKEN
from database import init_db
import sqlite3
from datetime import datetime

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

init_db()

def save_file(user_id, file_id, file_type, caption, category):
    conn = sqlite3.connect("files.db")
    cur = conn.cursor()
    cur.execute('INSERT INTO files (user_id, file_id, file_type, caption, category, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                (user_id, file_id, file_type, caption, category, datetime.utcnow()))
    conn.commit()
    conn.close()

def detect_category(mime):
    if not mime:
        return "Другое"
    if "image" in mime:
        return "Фото"
    if "video" in mime:
        return "Видео"
    if "audio" in mime:
        return "Аудио"
    if "application" in mime:
        return "Документы"
    return "Другое"

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("👋 Привет! Отправь мне файл с подписью — я сохраню его для тебя.")

@dp.message_handler(content_types=types.ContentType.ANY)
async def handle_files(msg: types.Message):
    file = msg.document or (msg.photo[-1] if msg.photo else None) or msg.video or msg.audio
    if not file:
        await msg.reply("⛔️ Файл не распознан.")
        return

    file_id = file.file_id
    file_type = getattr(file, 'mime_type', 'unknown')
    caption = msg.caption or "Без описания"
    category = detect_category(file_type)

    save_file(msg.from_user.id, file_id, file_type, caption, category)
    await msg.reply(f"✅ Файл сохранён!\n📂 Категория: {category}")

if __name__ == "__main__":
    executor.start_polling(dp)
