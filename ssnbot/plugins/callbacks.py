import traceback
from data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, LinkPreviewOptions
from ssnbot.plugins.generate import generate_session, ask_ques, buttons_ques
from ssnbot import LOGGER

# Default messages to avoid issues if Data variables are undefined
DEFAULT_START = "Welcome, {0}! Use the buttons below to navigate."
DEFAULT_ABOUT = "This bot allows you to generate session strings for your libraries."
DEFAULT_HELP = "Click the buttons below to explore more features or get help."
DEFAULT_ERROR_MESSAGE = (
    "Oops! An error occurred! \n\n**Error** : {} "
    "\n\nPlease contact @ElUpdates if this message is unclear or if you need further assistance."
)


@Client.on_callback_query(filters.regex(r"^home$"))
async def home(bot, query):
    """
    Handles the 'home' callback.
    Sends the start message with navigation buttons.
    """
    try:
        user = await bot.get_me()
        mention = user.mention
        chat_id = query.from_user.id
        message_id = query.message.id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=Data.START.format(query.from_user.mention, mention) if Data.START else DEFAULT_START.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(Data.buttons),
        )
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        await query.message.reply(DEFAULT_ERROR_MESSAGE.format(str(e)))


@Client.on_callback_query(filters.regex(r"^about$"))
async def about(bot, query):
    """
    Handles the 'about' callback.
    Sends the about message.
    """
    try:
        chat_id = query.from_user.id
        message_id = query.message.id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=Data.ABOUT if Data.ABOUT else DEFAULT_ABOUT,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        await query.message.reply(DEFAULT_ERROR_MESSAGE.format(str(e)))


@Client.on_callback_query(filters.regex(r"^help$"))
async def help(bot, query):
    """
    Handles the 'help' callback.
    Sends the help message with navigation buttons.
    """
    try:
        chat_id = query.from_user.id
        message_id = query.message.id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=Data.HELP if Data.HELP else DEFAULT_HELP,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        await query.message.reply(DEFAULT_ERROR_MESSAGE.format(str(e)))


@Client.on_callback_query(filters.regex(r"^generate$"))
async def generate(bot, query):
    """
    Handles the 'generate' callback.
    Prompts the user to choose a library for session generation.
    """
    try:
        await query.answer("Select your library")
        await query.message.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        await query.message.reply(DEFAULT_ERROR_MESSAGE.format(str(e)))


@Client.on_callback_query(filters.regex(r"^pyrogram$"))
async def pyro(bot, query):
    """
    Handles the 'pyrogram' callback.
    Generates a session string for Pyrogram.
    """
    try:
        await query.answer(
            "Note: New string sessions may not work with older bots. Ensure compatibility with Pyrogram v2.",
            show_alert=True,
        )
        await generate_session(bot, query.message)
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        await query.message.reply(DEFAULT_ERROR_MESSAGE.format(str(e)))


@Client.on_callback_query(filters.regex(r"^telethon$"))
async def tele(bot, query):
    """
    Handles the 'telethon' callback.
    Generates a session string for Telethon.
    """
    try:
        await query.answer()
        await generate_session(bot, query.message, telethon=True)
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        await query.message.reply(DEFAULT_ERROR_MESSAGE.format(str(e)))


ERROR_MESSAGE = (
    "Oops! An error occurred! \n\n**Error** : {} "
    "\n\nPlease contact @ElUpdates if this message is unclear or if you need further assistance."
)
