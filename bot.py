import asyncio
import os
import time
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile

# --- TOKЕNLAR VA SOZLAMALAR ---
# ⚠️ Render Environment bo'limiga BOT_TOKEN qo'shgan bo'lsangiz, shu qator qolsin.
# Agar u yerga qo'shmagan bo'lsangiz, os.environ.get('BOT_TOKEN') o'rniga '@BotFather'dan olgan tokeningizni yozing.
API_TOKEN ='8910821232:AAF2e_xNbWR7sDz4xu1CKr-WFEEdlDB4GMw'

# ⚠️ Bu yerga @userinfobot orqali olgan shaxsiy Telegram ID raqamingizni yozing
ADMIN_ID = 678275001  

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Foydalanuvchilar ID'sini va spam nazoratini xotirada saqlash
users_db = set()
user_spam_control = {}

# PDF fayllarni papkadan topib o'quvchiga yuboruvchi funksiya
async def send_pdf_file(callback: types.CallbackQuery, file_name: str):
    file_path = f"{file_name}.pdf"
    if os.path.exists(file_path):
        await callback.answer("Fayl yuklanmoqda...")
        document = FSInputFile(file_path)
        await callback.message.answer_document(
            document=document, 
            caption=f"📄 **{file_name.replace('_', ' ')}** fayli muvaffaqiyatli yuklandi."
        )
    else:
        await callback.answer("⚠️ Bu fayl dars davomida o'qituvchi tomonidan yuklanadi!", show_alert=True)

# Bosh menyu tugmalari
def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📝 BSB", callback_data="menu_bsb"))
    builder.row(types.InlineKeyboardButton(text="📊 CHSB", callback_data="menu_chsb"))
    builder.row(types.InlineKeyboardButton(text="💻 Amaliy ishlar", callback_data="menu_amaliy"))
    builder.row(types.InlineKeyboardButton(text="ℹ️ Bot haqida", callback_data="menu_haqida"))
    return builder.as_markup()

# Bot ishga tushganda (/start)
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    users_db.add(message.from_user.id)
    await message.reply(
        f"Salom, {message.from_user.full_name}!\n"
        f"11-sinf **Informatika** fanidan BSB va CHSB imtihonlariga tayyorgarlik botiga xush kelibsiz!\n\n"
        f"Kerakli bo'limni tanlang:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

# --- ADMIN UCHUN XABARNOMA BUYRUG'I ---
@dp.message()
async def admin_notify(message: types.Message):
    # Faqat matnli va /yangi buyrug'i bilan boshlangan xabarlarni tekshiradi
    if message.text and message.text.startswith("/yangi "):
        # Agar buyruqni admin yozmagan bo'lsa, bot e'tiborsiz qoldiradi
        if message.from_user.id != ADMIN_ID:
            return 
            
        file_name = message.text.replace("/yangi ", "").strip()
        success_count = 0
        for user_id in users_db:
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text=f"🔥 **YANGI TOPSHIRIQ!**\n\n11-sinf Informatika fanidan **{file_name.replace('_', ' ')}** botga yuklandi!\n"
                         f"Botga kirib, namuna va mavzularni yuklab oling.",
                    parse_mode="Markdown"
                )
                success_count += 1
            except Exception:
                pass
        await message.reply(f"📢 Xabarnoma {success_count} ta o'quvchiga yuborildi!")

# Tugmalar bosilganda ishlovchi qism
@dp.callback_query()
async def process_callback(callback: types.CallbackQuery):
    data = callback.data
    user_id = callback.from_user.id
    current_time = time.time()
    
    # --- SPAMGA QARSHI TEKSHIRUV (ANTI-FLOOD) ---
    if user_id in user_spam_control:
        last_click_time = user_spam_control[user_id]
        if current_time - last_click_time < 3:
            await callback.answer("⚠️ Iltimos, tugmalarni juda tez bosmang! Biroz kuting.", show_alert=True)
            return
            
    user_spam_control[user_id] = current_time

    # --- BSB MENYUSI ---
    if data == "menu_bsb":
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="📂 1_BSB_DEMO", callback_data="pdf_1_BSB_DEMO"),
                    types.InlineKeyboardButton(text="📖 Mavzular", callback_data="pdf_1_BSB_DEMO_Mavzular"))
        builder.row(types.InlineKeyboardButton(text="📂 2_BSB_DEMO", callback_data="pdf_2_BSB_DEMO"),
                    types.InlineKeyboardButton(text="📖 Mavzular", callback_data="pdf_2_BSB_DEMO_Mavzular"))
        builder.row(types.InlineKeyboardButton(text="📂 3_BSB_DEMO", callback_data="pdf_3_BSB_DEMO"),
                    types.InlineKeyboardButton(text="📖 Mavzular", callback_data="pdf_3_BSB_DEMO_Mavzular"))
        builder.row(types.InlineKeyboardButton(text="📂 4_BSB_DEMO", callback_data="pdf_4_BSB_DEMO"),
                    types.InlineKeyboardButton(text="📖 Mavzular", callback_data="pdf_4_BSB_DEMO_Mavzular"))
        builder.row(types.InlineKeyboardButton(text="⬅️ Ortga qaytish", callback_data="back_to_main"))
        
        await callback.message.edit_text("📋 **BSB bo'limi**\n\nKerakli nazorat ishi namunasini tanlang:", 
                                         reply_markup=builder.as_markup(), parse_mode="Markdown")

    # --- CHSB MENYUSI ---
    elif data == "menu_chsb":
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="📂 1_Chorak_CHSB_DEMO", callback_data="pdf_1_Chorak_CHSB_DEMO"),
                    types.InlineKeyboardButton(text="📖 Mavzular", callback_data="pdf_1_Chorak_CHSB_DEMO_Mavzular"))
        builder.row(types.InlineKeyboardButton(text="📂 2_Chorak_CHSB_DEMO", callback_data="pdf_2_Chorak_CHSB_DEMO"),
                    types.InlineKeyboardButton(text="📖 Mavzular", callback_data="pdf_2_Chorak_CHSB_DEMO_Mavzular"))
        builder.row(types.InlineKeyboardButton(text="📂 3_Chorak_CHSB_DEMO", callback_data="pdf_3_Chorak_CHSB_DEMO"),
                    types.InlineKeyboardButton(text="📖 Mavzular", callback_data="pdf_3_Chorak_CHSB_DEMO_Mavzular"))
        builder.row(types.InlineKeyboardButton(text="📂 4_Chorak_CHSB_DEMO", callback_data="pdf_4_Chorak_CHSB_DEMO"),
                    types.InlineKeyboardButton(text="📖 Mavzular", callback_data="pdf_4_Chorak_CHSB_DEMO_Mavzular"))
        builder.row(types.InlineKeyboardButton(text="⬅️ Ortga qaytish", callback_data="back_to_main"))
        
        await callback.message.edit_text("📊 **CHSB bo'limi**\n\nKerakli choraklik test namunasini tanlang:", 
                                         reply_markup=builder.as_markup(), parse_mode="Markdown")

    # --- AMALIY ISHLAR MENYUSI ---
    elif data == "menu_amaliy":
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="📂 1_Amaliy_ish", callback_data="pdf_1_Amaliy_ish"),
                    types.InlineKeyboardButton(text="📖 Mavzular", callback_data="pdf_1_Amaliy_ish_Mavzular"))
        builder.row(types.InlineKeyboardButton(text="📂 2_Amaliy_ish", callback_data="pdf_2_Amaliy_ish"),
                    types.InlineKeyboardButton(text="📖 Mavzular", callback_data="pdf_2_Amaliy_ish_Mavzular"))
        builder.row(types.InlineKeyboardButton(text="📂 3_Amaliy_ish", callback_data="pdf_3_Amaliy_ish"),
                    types.InlineKeyboardButton(text="📖 Mavzular", callback_data="pdf_3_Amaliy_ish_Mavzular"))
        builder.row(types.InlineKeyboardButton(text="📂 4_Amaliy_ish", callback_data="pdf_4_Amaliy_ish"),
                    types.InlineKeyboardButton(text="📖 Mavzular", callback_data="pdf_4_Amaliy_ish_Mavzular"))
        builder.row(types.InlineKeyboardButton(text="⬅️ Ortga qaytish", callback_data="back_to_main"))
        
        await callback.message.edit_text("💻 **Amaliy ishlar bo'limi**\n\nKerakli amaliy ishni tanlang:", 
                                         reply_markup=builder.as_markup(), parse_mode="Markdown")

    # --- BOT HAQIDA ---
    elif data == "menu_haqida":
        await callback.answer("🤖 Informatika fanidan 11-sinf BSB va CHSB testlariga yordamchi bot.", show_alert=True)

    # --- BOSH MENYUGA ORTGA QAYTISH ---
    elif data == "back_to_main":
        await callback.message.edit_text("Bosh menyuga qaytdingiz. Kerakli bo'limni tanlang:", reply_markup=get_main_menu())

    # --- FAYL YUBORISH REJIMINI ISHGA TUSHIRISH ---
    elif data.startswith("pdf_"):
        file_name = data.replace("pdf_", "")
        await send_pdf_file(callback, file_name)

    await callback.answer()

# Kodingizning eng pastidagi main() funksiyasini shu kod bilan yangilang:

async def main():
    # UptimeRobot va Render portlarini to'g'ri bog'lash uchun haqiqiy veb-server ochamiz
    from aiohttp import web
    
    async def handle(request):
        # UptimeRobot so'rov yuborganda unga "OK" va 200 kodini qaytaradi
        return web.Response(text="Bot muvaffaqiyatli ishlamoqda!", content_type="text/plain")
        
    app = web.Application()
    app.router.add_get('/', handle)
        
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render taqdim etadigan rasmiy portni aniqlaymiz
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    print("Informatika BSB/CHSB boti to'liq va tezkor rejimda ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
