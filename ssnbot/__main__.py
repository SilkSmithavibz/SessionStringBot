import uvloop
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from ssnbot import APP_ID, API_HASH, BOT_TOKEN, LOGGER


# Install uvloop to speed up asyncio
uvloop.install()

# Initialize the bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def on_start(msg: types.Message):
    """
    Start command handler to confirm the bot is working.
    """
    user = msg.from_user
    LOGGER.info(f"{user.first_name} - @{user.username} - Bot started!")
    await msg.answer(f"Hello {user.first_name}, I am your bot!")


async def on_shutdown(dp):
    """
    Handler for bot shutdown, logging the stop event.
    """
    LOGGER.info("Bot is shutting down!")


# Register the handler for `/start`
dp.register_message_handler(on_start, commands=['start'])

async def main():
    """
    Main function to initialize and start the bot.
    """
    LOGGER.info("Bot is starting...")
    # Start polling and run the bot
    await dp.start_polling(on_shutdown=on_shutdown)


# Run the main async function in the event loop
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
