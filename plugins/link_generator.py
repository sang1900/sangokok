from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id
import requests

@Bot.on_message(filters.private & filters.command('files'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = f"{message.from_user.id}\n{ADMINS}\nChuyển tiếp file, hình ảnh, tin nhắn... đầu tiên từ kênh Database (có trích dẫn)\n<code>(Hết hạn sau 60s)</code>", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            while True:
                try:
                    second_message = await client.ask(text = "Chuyển tiếp file, hình ảnh, tin nhắn... cuối cùng từ kênh Database (có trích dẫn)\n<code>(Hết hạn sau 60s</code>", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
                except:
                    return
                s_msg_id = await get_message_id(client, second_message)
                if s_msg_id:
                    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
                    base64_string = await encode(string)
                    url = f"https://t.me/{client.username}?start={base64_string}"
                    link1s=requests.get(f"https://link1s.com/api?api=9e9c26d7a2a2759289d9f95c84931a0471da7243&url={url}").json()["shortenedUrl"]
                    link=requests.get(f"https://link.olacity.com/api/?api=46e2243ee2307a5d62bd7afa560150fec8f9d05d&url={link1s}").json()["shortenedUrl"]
                    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
                    await second_message.reply_text(f"<b>✅ LƯU TRỮ THÀNH CÔNG \n\n🔗 Your URL : {link}</b>\n(Mở link trên để lấy URL dẫn đến file đã lưu trữ)\n(Tạo BOT lưu trữ tự quản lý hoặc xoá link rút gọn liên hệ <a href='https://fb.com/sang1900'>Nguyễn Sáng</a>)", quote=True, reply_markup=reply_markup)
                    break
                else:
                    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("💲 Mua bản Premium", url=f'https://fb.com/sang1900')]])
                    await second_message.reply("<b>Đã sảy ra lỗi </b>\nTin nhắn hoặc link này không tồn tại hoặc không được chuyển tiếp từ kênh Database!.\n<b>Chú ý:</b> chức năng này chỉ dành cho người dùng <code>Premium</code>", quote = True, reply_markup=reply_markup)
                    break
            break
        else:
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("💲 Mua bản Premium", url=f'https://fb.com/sang1900')]])
            await first_message.reply("<b>Đã sảy ra lỗi </b>\nTin nhắn hoặc link này không tồn tại hoặc không được chuyển tiếp từ kênh Database!.\n<b>Chú ý:</b> chức năng này chỉ dành cho người dùng <code>Premium</code>", quote = True, reply_markup=reply_markup)
            break


@Bot.on_message(filters.private & filters.command('file'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "Chuyển tiếp 1 file, hình ảnh, tin nhắn... từ kênh Database (có trích dẫn)\n<code>(Hết hạn sau 60s)</code>", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
            url = f"https://t.me/{client.username}?start={base64_string}"
            link1s=requests.get(f"https://link1s.com/api?api=9e9c26d7a2a2759289d9f95c84931a0471da7243&url={url}").json()["shortenedUrl"]
            link=requests.get(f"https://link.olacity.com/api/?api=46e2243ee2307a5d62bd7afa560150fec8f9d05d&url={link1s}").json()["shortenedUrl"]
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
            await channel_message.reply_text(f"<b>✅ LƯU TRỮ THÀNH CÔNG \n\n🔗 Your URL : {link}</b>\n(Mở link trên để lấy URL dẫn đến file đã lưu trữ)\n(Tạo BOT lưu trữ tự quản lý hoặc xoá link rút gọn liên hệ <a href='https://fb.com/sang1900'>Nguyễn Sáng</a>)", quote=True, reply_markup=reply_markup)
            break
        else:
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("💲 Mua bản Premium", url=f'https://fb.com/sang1900')]])
            await channel_message.reply("<b>Đã sảy ra lỗi </b>\nTin nhắn hoặc link này không tồn tại hoặc không được chuyển tiếp từ kênh Database!.\n<b>Chú ý:</b> chức năng này chỉ dành cho người dùng <code>Premium</code>", quote=True , reply_markup=reply_markup)
            break
