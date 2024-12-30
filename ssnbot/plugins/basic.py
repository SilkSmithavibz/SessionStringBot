import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import AiogramError
from aiogram.filters import Command, PrivateFilter
from ssnbot.db.sql import add_user
from data import Data
from ssnbot import LOGGER

# Initialize Dispatcher
bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()


def command_filter(cmd: str):
    """Custom filter for handling bot commands."""
    return Command(commands=[cmd]) & PrivateFilter()


# Start Message
@dp.message(command_filter("start"))
async def start(msg: types.Message):
    """
    Handles the /start command. Greets the user and stores their information in the database.
    """
    user_id = msg.from_user.id
    username = f"@{msg.from_user.username}" if msg.from_user.username else "Anonymous"

    try:
        # Add the user to the database
        await add_user(user_id, username)
    except Exception as e:
        LOGGER.error(f"Error adding user to database: {e}")

    bot_user = await bot.get_me()
    mention = bot_user.mention

    try:
        await msg.answer(
            Data.START.format(msg.from_user.mention, mention),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=Data.buttons)
        )
    except Exception as e:
        LOGGER.error(f"Error sending start message: {e}")


# Help Message
@dp.message(command_filter("help"))
async def help_command(msg: types.Message):
    """
    Handles the /help command. Provides usage instructions to the user.
    """
    user_id = msg.from_user.id
    username = f"@{msg.from_user.username}" if msg.from_user.username else "Anonymous"

    try:
        await add_user(user_id, username)
    except Exception as e:
        LOGGER.error(f"Error adding user to database: {e}")

    try:
        await msg.answer(
            Data.HELP,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=Data.home_buttons)
        )
    except Exception as e:
        LOGGER.error(f"Error sending help message: {e}")


# About Message
@dp.message(command_filter("about"))
async def about(msg: types.Message):
    """
    Handles the /about command. Provides information about the bot.
    """
    try:
        await msg.answer(
            Data.ABOUT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=Data.home_buttons)
        )
    except Exception as e:
        LOGGER.error(f"Error sending about message: {e}")

# Run the bot
if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
