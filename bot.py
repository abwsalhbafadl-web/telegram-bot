Enterimport asyncio
import json
import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# معلومات البوت
TOKEN = "8239691778:AAGa09czNPGSJiY6smUh2ued3KALaFs9uos"
ADMIN_ID = 8584398384

# القنوات
MAIN_CHANNEL = -1003861798499   # القناة الرسمية
ACTIVATE_CHANNEL = -1003361910905   # قناة التفعيلات

SUPPORT_USER = "A_ar_78"
HELP_CHANNEL = "https://t.me/xxx_gjko"

bot = Bot(token=TOKEN)
dp = Dispatcher()

DB_FILE = "users.json"

# تحميل المستخدمين
def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE) as f:
        return json.load(f)

# حفظ المستخدمين
def save_users(data):
    with open(DB_FILE,"w") as f:
        json.dump(data,f,indent=2)

users = load_users()

# إنشاء حساب
def create_account(user_id):

    email = f"user{random.randint(1000,9999)}@bot.com"
    password = str(random.randint(10000,99999))

    users[str(user_id)] = {
        "email":email,
        "password":password,
        "balance":0,
        "referrals":0
    }

    save_users(users)

    return email,password

# التحقق من الاشتراك
async def check_join(user_id):

    try:
        ch1 = await bot.get_chat_member(MAIN_CHANNEL,user_id)
        ch2 = await bot.get_chat_member(ACTIVATE_CHANNEL,user_id)

        if ch1.status in ["member","administrator","creator"] and \
           ch2.status in ["member","administrator","creator"]:
            return True

        return False

    except:
        return False


@dp.message(CommandStart())
async def start(message: types.Message):

    user_id = message.from_user.id
    name = message.from_user.first_name

    joined = await check_join(user_id)

    # اذا لم يشترك
    if not joined:

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="القناة الرسمية",url="https://t.me/A_ar_78")],
                [InlineKeyboardButton(text="قناة التفعيلات",url="https://t.me/A_ar_78")],
                [InlineKeyboardButton(text="قناة شرح البوت",url=HELP_CHANNEL)],
                [InlineKeyboardButton(text="تحقق من الاشتراك",callback_data="check")]
            ]
        )

        await message.answer(
            "⚠️ يجب الاشتراك في القنوات لاستخدام البوت",
            reply_markup=kb
        )
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="تسجيل دخول",callback_data="login")],
            [InlineKeyboardButton(text="إنشاء حساب",callback_data="register")],
            [InlineKeyboardButton(text="رصيدي",callback_data="balance")],
            [InlineKeyboardButton(text="الدعم",url=f"https://t.me/{SUPPORT_USER}")]
        ]
    )

    await message.answer(
        f"مرحبا {name}\nاختر من القائمة",
        reply_markup=kb
    )


@dp.callback_query()
async def callbacks(call: types.CallbackQuery):

    user_id = str(call.from_user.id)

    if call.data == "check":

        joined = await check_join(call.from_user.id)

        if joined:
            await call.message.edit_text("✅ تم التحقق من الاشتراك\nأرسل /start")
        else:
            await call.answer("❌ لم تشترك بعد",show_alert=True)

    elif call.data == "register":

        if user_id in users:

            await call.message.edit_text("لديك حساب بالفعل")

        else:

            email,password = create_account(user_id)

            await call.message.edit_text(
                f"✅ تم إنشاء حساب\n\n"
                f"Email : {email}\n"
                f"Password : {password}"
            )

    elif call.data == "login":

        if user_id not in users:

            await call.message.edit_text("ليس لديك حساب")

        else:

            user = users[user_id]

            await call.message.edit_text(
                f"✅ تم تسجيل الدخول\n\n"
                f"الحساب : {user['email']}\n"
                f"الرصيد : {user['balance']} ₽"
            )

    elif call.data == "balance":

        if user_id not in users:
            await call.message.edit_text("أنشئ حساب أولاً")
        else:
            bal = users[user_id]["balance"]

            await call.message.edit_text(
                f"💰 رصيدك الحالي\n\n{bal} ₽"
            )


async def main():

    print("Bot Started...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

