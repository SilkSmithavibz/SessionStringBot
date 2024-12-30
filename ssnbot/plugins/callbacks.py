import asyncio
import traceback
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from ssnbot.plugins.generate import generate_session, ask_ques, buttons_ques
from ssnbot import LOGGER
from data import Data

# Initialize Bot and Dispatcher
bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()

ERROR_MESSAGE = (
    "Oops! An exception occurred! \n\n**Error** : {} "
    "\n\nPlease visit @The_Architect04 if this message doesn't contain any "
    "sensitive information and you want to report this issue, "
    "as this error message is not being logged by us!"
)

# Home Callback
@dp.callback_query(Text("home"))
async def home(query: types.CallbackQuery):
    user = await bot.get_me()
    mention = user.full_name
    await query.message.edit_text(
        Data.START.format(query.from_user.mention, mention),
        reply_markup=InlineKeyboardBuilder(Data.buttons).as_markup()
    )

# About Callback
@dp.callback_query(Text("about"))
async def about(query: types.CallbackQuery):
    await query.message.edit_text(
        Data.ABOUT,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardBuilder(Data.home_buttons).as_markup()
    )

# Help Callback
@dp.callback_query(Text("help"))
async def help(query: types.CallbackQuery):
    await query.message.edit_text(
        Data.HELP,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardBuilder(Data.home_buttons).as_markup()
    )

# Generate Session Callback
@dp.callback_query(Text("generate"))
async def generate(query: types.CallbackQuery):
    await query.answer("Select your library")
    await query.message.reply(ask_ques, reply_markup=InlineKeyboardBuilder(buttons_ques).as_markup())

# Pyrogram Callback
@dp.callback_query(Text("pyrogram"))
async def pyro(query: types.CallbackQuery):
    try:
        await query.answer(
            "Please note that the new type of string sessions may not work in all bots, i.e., only the bots that have been updated to pyrogram v2 will work!",
            show_alert=True,
        )
        await generate_session(bot, query.message)
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        LOGGER.error(e)
        await query.message.reply(ERROR_MESSAGE.format(str(e)))

# Telethon Callback
@dp.callback_query(Text("telethon"))
async def tele(query: types.CallbackQuery):
    try:
        await query.answer()
        await generate_session(bot, query.message, telethon=True)
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        LOGGER.error(e)
        await query.message.reply(ERROR_MESSAGE.format(str(e)))

# Run the bot
if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
