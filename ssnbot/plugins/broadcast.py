import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
from pyrogram.types import Message
from ssnbot import ADMINS
from ssnbot.db.sql import query_msg
from ssnbot.db.support import users_info


@Client.on_message(filters.private & filters.command("stats"))
async def get_subscribers_count(bot: Client, message: Message):
    """
    Fetch and display subscriber statistics.
    Only accessible to admins.
    """
    user_id = message.from_user.id
    if user_id not in ADMINS:
        return

    wait_msg = "__Calculating, please wait...__"
    msg = await message.reply_text(wait_msg)

    active, blocked = await users_info(bot)
    stats_msg = (
        f"**📊 Stats**\n"
        f"👤 Active Subscribers: `{active}`\n"
        f"🚫 Blocked / Deleted: `{blocked}`"
    )
    await msg.edit(stats_msg)


@Client.on_message(filters.private & filters.command("broadcast"))
async def send_text(bot: Client, message: Message):
    """
    Broadcast a message to all users in the database.
    Usage: Reply to a message with the /broadcast command.
    """
    user_id = message.from_user.id
    if user_id not in ADMINS:
        return

    if message.reply_to_message:
        query = await query_msg()
        sent, failed = 0, 0
        for row in query:
            chat_id = int(row[0])
            try:
                await bot.copy_message(
                    chat_id=chat_id,
                    from_chat_id=message.chat.id,
                    message_id=message.reply_to_message.message_id,
                    caption=message.reply_to_message.caption or "",
                    reply_markup=message.reply_to_message.reply_markup,
                )
                sent += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except RPCError as e:
                failed += 1
                print(f"Failed to send message to {chat_id}: {e}")
            except Exception as e:
                failed += 1
                print(f"Unexpected error for {chat_id}: {e}")

        await message.reply_text(
            f"**Broadcast Report**\n"
            f"✅ Sent: `{sent}`\n"
            f"❌ Failed: `{failed}`"
        )
    else:
        reply_error = (
            "❗ **Usage Error:**\n"
            "Reply to a message with `/broadcast` to send it to all subscribers."
        )
        msg = await message.reply_text(reply_error)
        await asyncio.sleep(8)
        await msg.delete()

