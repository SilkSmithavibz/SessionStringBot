import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.exceptions import (
    ApiIdInvalid,
    BotBlocked,
    PhoneNumberBanned,
    PhoneNumberInvalid,
)
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Text
from telethon import TelegramClient
from telethon.errors import (
    ApiIdInvalidError,
    PasswordHashInvalidError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    PhoneNumberInvalidError,
    SessionPasswordNeededError,
    AccessTokenInvalidError,
)
from telethon.sessions import StringSession
from data import Data

TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

ask_ques = "ᴘʟᴇᴀꜱᴇ ᴄʜᴏᴏꜱᴇ ᴛʜᴇ ᴘʏᴛʜᴏɴ ʟɪʙʀᴀʀʏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ꜱᴛʀɪɴɢ ꜱᴇꜱꜱɪᴏɴ ꜰᴏʀ 🤖"
buttons_ques = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("🍷ᴘʏʀᴏɢʀᴀᴍ🍷", callback_data="pyrogram"),
            InlineKeyboardButton("🍧ᴛᴇʟᴇᴛʜᴏɴ🍧", callback_data="telethon"),
        ],
    ]
)


@dp.message_handler(commands=["generate"])
async def send_library_choice(message: types.Message):
    await message.reply(ask_ques, reply_markup=buttons_ques)


@dp.callback_query_handler(Text(equals=["pyrogram", "telethon"]))
async def handle_library_choice(callback_query: types.CallbackQuery):
    library = callback_query.data
    is_telethon = library == "telethon"
    await callback_query.message.reply(
        f"ᴄʜᴏꜱᴇɴ {library.upper()}. ꜱᴛᴀʀᴛɪɴɢ ꜱᴇꜱꜱɪᴏɴ ɢᴇɴᴇʀᴀᴛɪᴏɴ 🪺..."
    )
    await generate_session(callback_query.message, is_telethon)


async def generate_session(message: types.Message, telethon=False):
    user_id = message.chat.id
    ty = "Telethon" if telethon else "Pyrogram"
    await message.reply(f"ꜱᴛᴀʀᴛɪɴɢ {ty} ꜱᴇꜱꜱɪᴏɴ ɢᴇɴᴇʀᴀᴛɪᴏɴ🪺...")

    # Step 1: Ask for API_ID
    await message.answer("Please send your `API_ID`.")
    try:
        api_id_msg = await bot.wait_for(
            "message", timeout=360, check=lambda m: m.chat.id == user_id
        )
        api_id = int(api_id_msg.text)
    except ValueError:
        await message.answer(
            "Invalid API_ID. Please try again with `/generate`."
        )
        return
    except asyncio.TimeoutError:
        await message.answer("Request timed out. Please try again with `/generate`.")
        return

    # Step 2: Ask for API_HASH
    await message.answer("Please send your `API_HASH`.")
    try:
        api_hash_msg = await bot.wait_for(
            "message", timeout=360, check=lambda m: m.chat.id == user_id
        )
        api_hash = api_hash_msg.text
    except asyncio.TimeoutError:
        await message.answer("Request timed out. Please try again with `/generate`.")
        return

    # Step 3: Ask for Phone Number or Bot Token
    if not telethon:
        t = (
            "Please send your `PHONE_NUMBER` with country code.\n"
            "Example: `+19876543210`."
        )
    else:
        t = "Please send your `BOT_TOKEN`.\nExample: `12345:abcdefghijklmnopqrstuvwxyz`."
    await message.answer(t)
    try:
        phone_number_msg = await bot.wait_for(
            "message", timeout=360, check=lambda m: m.chat.id == user_id
        )
        phone_number = phone_number_msg.text
    except asyncio.TimeoutError:
        await message.answer("Request timed out. Please try again with `/generate`.")
        return

    # Step 4: Send OTP or Authenticate
    client = None
    try:
        if telethon:
            client = TelegramClient(StringSession(), api_id, api_hash)
            await client.start(bot_token=phone_number)
        else:
            client = TelegramClient(
                StringSession(), api_id=api_id, api_hash=api_hash
            )
            await client.connect()
            await client.send_code_request(phone_number)

        await message.answer("OTP sent! Please check Telegram for the code.")
    except ApiIdInvalidError:
        await message.answer("Invalid API_ID and API_HASH combination.")
        return
    except PhoneNumberInvalidError:
        await message.answer("Invalid phone number. Please try again.")
        return
    except PhoneNumberBanned:
        await message.answer("Phone number is banned. Please try a different number.")
        return

    # Step 5: Enter OTP
    try:
        otp_msg = await bot.wait_for(
            "message", timeout=360, check=lambda m: m.chat.id == user_id
        )
        otp = otp_msg.text.replace(" ", "")
        await client.sign_in(phone=phone_number, code=otp)
    except PhoneCodeInvalidError:
        await message.answer("Invalid OTP. Please try again.")
        return
    except PhoneCodeExpiredError:
        await message.answer("OTP expired. Please try again.")
        return

    # Step 6: Generate String Session
    string_session = client.session.save()
    await message.answer(
        f"**{ty.upper()} STRING SESSION**\n\n`{string_session}`\n\nGenerated by @YourBot."
    )
    await client.disconnect()


if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
