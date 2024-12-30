import asyncio
from aiogram import Bot, types
from aiogram.types import ChatAction
from ssnbot.db.sql import query_msg, del_user
from ssnbot import LOGGER

async def users_info(bot: Bot):
    users = 0
    blocked = 0
    identity = await query_msg()
    for user in identity:
        user_id = int(user[0])
        name = None
        try:
            # Send typing action to the user (replaces 'send_chat_action' in aiogram)
            name = await bot.send_chat_action(user_id, ChatAction.TYPING)
        except asyncio.exceptions.TimeoutError:  # Handling timeout
            await asyncio.sleep(1)
        except Exception:
            pass
        if name:
            users += 1
        else:
            await del_user(user_id)
            LOGGER.info("Deleted user id %s from broadcast list", user_id)
            blocked += 1
    return users, blocked
