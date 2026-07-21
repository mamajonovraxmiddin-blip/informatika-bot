import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile

# BotFather bergan O'Z TOKENINGIZNI shu yerga qo'ying
import os
API_TOKEN = os.environ.get('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Foydalanuvchilar ID'sini xabarnoma uchun saqlash (Xotirada saqlanadi)
users_db = set()

# PDF fayllarni papkadan topib o'quvchiga yuboruvchi asosiy funksiya
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
        # Fayl hali papkaga tashlanmagan bo'lsa, ogohlantirish beradi
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
    users_db.add(message.from_user.id) # O'quvchini xabarnoma ro'yxatiga qo'shish
    await message.reply(
        f"Salom, {message.from_user.full_name}!\n"
        f"11-sinf **Informatika** fanidan BSB va CHSB imtihonlariga tayyorgarlik botiga xush kelibsiz!\n\n"
        f"Kerakli bo'limni tanlang:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

# --- ADMIN UCHUN XABARNOMA BUYRUG'I ---
# Masalan yangi fayl yuklasangiz: /yangi 1_BSB_DEMO deb yozasiz
# Shaxsiy Telegram ID raqamingizni kiriting
# @userinfobot orqali olgan raqamingizni shu yerga yozing
ADMIN_ID = 678275001  

@dp.message()
async def admin_notify(message: types.Message):
    # Agar xabar yuborayotgan odam siz bo'lmasangiz, buyruq umuman ishlamaydi
    if message.from_user.id != ADMIN_ID:
        return 

    if message.text.startswith("/yangi "):
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

# Kodingizning eng pastidagi eski main va asyncio.run qismini shu kod bilan almashtiring:

async def main():
    # Web Service bepul ishlashi uchun soxta port yaratamiz
    from aiohttp import web
    async def handle(request):
        return web.Response(text="Bot ishlamoqda!")
    
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render beradigan portni oladi yoki avtomat 10000-portni yoqadi
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    asyncio.create_task(site.start())
    
    print("Informatika BSB/CHSB boti to'liq va tezkor rejimda ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

