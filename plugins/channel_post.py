import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
import requests 
from bot import Bot
from config import ADMINS, OWNER_ID, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode

@Bot.on_message(filters.private & ~filters.command(['upload','users','broadcast','files','file']))
async def channel_post(client: Client, message: Message):
    id = message.from_user.id
    reply_text = await message.reply_text("<b>Vui lòng chờ...!</b>", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("<b>Đã xảy ra lỗi...!</b>")
        return
    converted_id = post_message.message_id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    if id not in ADMINS:
        url = f"https://t.me/{client.username}?start={base64_string}"
        link1s=requests.get(f"https://link1s.com/api?api=9e9c26d7a2a2759289d9f95c84931a0471da7243&url={url}").json()["shortenedUrl"]
        link=requests.get(f"https://link.olacity.com/api/?api=46e2243ee2307a5d62bd7afa560150fec8f9d05d&url={link1s}").json()["shortenedUrl"]
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("📽️ Hướng dẫn lấy Link", url=f'https://telegram.me/share/url?url={link}')]])
    await reply_text.edit(f"<b>✅ LƯU TRỮ THÀNH CÔNG \n\n🔗 Your URL : {link}</b>\n(Mở link trên để lấy URL dẫn đến file đã lưu trữ)\n(Tạo BOT lưu trữ tự quản lý hoặc xoá link rút gọn liên hệ <a href='https://fb.com/sang1900'>Nguyễn Sáng</a>)", reply_markup=reply_markup, disable_web_page_preview = True)

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID) & ~filters.edited)
async def new_post(client: Client, message: Message):
    if DISABLE_CHANNEL_BUTTON:
        return
    converted_id = message.message_id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
