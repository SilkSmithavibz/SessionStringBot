import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from ssnbot import ADMINS
from ssnbot.db.sql import query_msg
from ssnbot.db.support import users_info


@Client.on_message(filters.private & filters.command("stats"))
async def get_subscribers_count(bot: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        return
    wait_msg = "__Calculating, please wait...__"
    msg = await message.reply_text(wait_msg)
    active, blocked = await users_info(bot)
    stats_msg = f"**Stats**\nSubscribers: `{active}`\nBlocked / Deleted: `{blocked}`"
    await msg.edit(stats_msg)


@Client.on_message(filters.private & filters.command("broadcast"))
async def send_text(bot: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        return

    if message.reply_to_message is None:
        reply_error = "`Use this command as a reply to any telegram message without any spaces.`"
        msg = await message.reply_text(reply_error)
        await asyncio.sleep(8)
        await msg.delete()
        return

    # Check if message text is exactly "broadcast"
    if "broadcast" in message.text.lower():
        query = query_msg()  # Remove await here if query_msg is not async
        if query:  # Ensure there are results to send the message to
            for row in query:
                chat_id = int(row[0])
                try:
                    await bot.copy_message(
                        chat_id=chat_id,
                        from_chat_id=message.chat.id,
                        message_id=message.reply_to_message_id,
                        caption=message.reply_to_message.caption,
                        reply_markup=message.reply_to_message.reply_markup,
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception as e:
                    logger.error(f"Error sending message to {chat_id}: {e}")
        else:
            await message.reply_text("No users found in the database.")
    else:
        reply_error = "`Please reply to a message and use the command properly.`"
        msg = await message.reply_text(reply_error)
        await asyncio.sleep(8)
        await msg.delete()
