import uvloop
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from ssnbot import API_TOKEN, LOGGER  # noqa: E402

# Install uvloop for faster event loop performance
uvloop.install()

API_TOKEN = 'your-bot-api-token'

# Initialize the bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def on_start(msg: types.Message):
    user = msg.from_user
    LOGGER.info(
        "%s - @%s - aiogram - Started...",
        user.first_name,
        user.username,
    )
    await msg.reply("Bot started. Use /help for assistance.")

async def on_stop():
    LOGGER.info("Bot stopped.")

async def main():
    # Registering the start command handler
    @dp.message_handler(commands=['start'])
    async def cmd_start(msg: types.Message):
        await on_start(msg)

    # Handling shutdown signal (graceful shutdown)
    dp.loop.add_signal_handler(asyncio.Event(), on_stop)

    # Start polling for updates
    await dp.start_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
