import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, PrivateFilter
from ssnbot import ADMINS, LOGGER
from ssnbot.db.sql import query_msg
from ssnbot.db.support import users_info

# Initialize Bot and Dispatcher
bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()

def command_filter(cmd: str):
    """Custom filter for handling bot commands."""
    return Command(commands=[cmd]) & PrivateFilter()


# Stats Command
@dp.message(command_filter("stats"))
async def get_subscribers_count(msg: types.Message):
    """
    Handles the /stats command to display subscriber stats.
    """
    user_id = msg.from_user.id
    if user_id not in ADMINS:
        return

    wait_msg = "__Calculating, please wait...__"
    msg_reply = await msg.answer(wait_msg)

    try:
        active, blocked = await users_info(bot)
        stats_msg = f"**Stats**\nSubscribers: `{active}`\nBlocked / Deleted: `{blocked}`"
        await msg_reply.edit_text(stats_msg)
    except Exception as e:
        LOGGER.error(f"Error fetching stats: {e}")


# Broadcast Command
@dp.message(command_filter("broadcast"))
async def send_text(msg: types.Message):
    """
    Handles the /broadcast command to send a message to all subscribers.
    """
    user_id = msg.from_user.id
    if user_id not in ADMINS:
        return

    if msg.reply_to_message:
        try:
            query = await query_msg()
            for row in query:
                chat_id = int(row[0])
                try:
                    await bot.copy_message(
                        chat_id=chat_id,
                        from_chat_id=msg.chat.id,
                        message_id=msg.reply_to_message.message_id
                    )
                except TelegramBadRequest as e:
                    LOGGER.error(f"Failed to send message to {chat_id}: {e}")
                except Exception as e:
                    LOGGER.error(f"Unexpected error: {e}")
        except Exception as e:
            LOGGER.error(f"Error during broadcast: {e}")
    else:
        reply_error = "`Use this command as a reply to any Telegram message without any spaces.`"
        error_msg = await msg.answer(reply_error)
        await asyncio.sleep(8)
        await error_msg.delete()

# Run the bot
if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
