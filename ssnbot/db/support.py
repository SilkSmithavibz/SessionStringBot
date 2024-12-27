import asyncio
from pyrogram.errors import FloodWait, RPCError
from pyrogram import enums
from ssnbot.db.sql import query_msg, del_user
from ssnbot import LOGGER

async def users_info(bot) -> tuple[int, int]:
    """
    Function to check user activity and manage the broadcast list.
    
    Args:
        bot: The Pyrogram bot/client instance.
    
    Returns:
        A tuple containing the number of active users and blocked users.
    """
    users = 0  # Count of active users
    blocked = 0  # Count of blocked users
    identity = await query_msg()  # Fetch user IDs from the database

    for user in identity:
        user_id = int(user[0])
        try:
            # Attempt to send a "typing" action to the user
            await bot.send_chat_action(user_id, enums.ChatAction.TYPING)
            users += 1  # If successful, increment active users count
        except FloodWait as e:
            LOGGER.warning("FloodWait triggered for %d seconds", e.value)
            await asyncio.sleep(e.value)  # Wait for the required time
        except RPCError as e:
            LOGGER.error("RPCError for user %s: %s", user_id, e)
            await del_user(user_id)  # Remove the user from the broadcast list
            LOGGER.info("Deleted user ID %s from broadcast list", user_id)
            blocked += 1  # Increment blocked users count
        except Exception as e:
            LOGGER.error("Unexpected error for user %s: %s", user_id, e)

    return users, blocked  # Return the counts of active and blocked users
