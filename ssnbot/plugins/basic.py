from data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, Message
from ssnbot.db.sql import add_user


def command_filter(cmd: str):
    """Custom filter for handling bot commands."""
    return filters.private & filters.incoming & filters.command(cmd)


# Start Message
@Client.on_message(command_filter("start"))
async def start(bot: Client, msg: Message):
    """
    Handles the /start command. Greets the user and stores their information in the database.
    """
    user_id = msg.from_user.id
    username = f"@{msg.from_user.username}" if msg.from_user.username else "Anonymous"

    try:
        # Add the user to the database
        await add_user(user_id, username)
    except Exception as e:
        print(f"Error adding user to database: {e}")

    bot_user = await bot.get_me()
    mention = bot_user.mention

    try:
        await bot.send_message(
            msg.chat.id,
            Data.START.format(msg.from_user.mention, mention),
            reply_markup=InlineKeyboardMarkup(Data.buttons)
        )
    except Exception as e:
        print(f"Error sending start message: {e}")


# Help Message
@Client.on_message(command_filter("help"))
async def help_command(bot: Client, msg: Message):
    """
    Handles the /help command. Provides usage instructions to the user.
    """
    user_id = msg.from_user.id
    username = f"@{msg.from_user.username}" if msg.from_user.username else "Anonymous"

    try:
        await add_user(user_id, username)
    except Exception as e:
        print(f"Error adding user to database: {e}")

    try:
        await bot.send_message(
            msg.chat.id,
            Data.HELP,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons)
        )
    except Exception as e:
        print(f"Error sending help message: {e}")


# About Message
@Client.on_message(command_filter("about"))
async def about(bot: Client, msg: Message):
    """
    Handles the /about command. Provides information about the bot.
    """
    try:
        await bot.send_message(
            msg.chat.id,
            Data.ABOUT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons)
        )
    except Exception as e:
        print(f"Error sending about message: {e}")
