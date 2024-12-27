import asyncio
from asyncio.exceptions import TimeoutError
from pyrogram import Client, filters
from pyrogram.errors import (
    ApiIdInvalid,
    PasswordHashInvalid,
    PhoneCodeExpired,
    PhoneCodeInvalid,
    PhoneNumberInvalid,
    SessionPasswordNeeded,
    PhoneNumberBanned,
    PhonePasswordFlood,
    AccessTokenInvalid,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telethon import TelegramClient
from telethon.errors import (
    ApiIdInvalidError,
    PasswordHashInvalidError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    PhoneNumberInvalidError,
    SessionPasswordNeededError,
    AccessTokenInvalidError,
)
from telethon.sessions import StringSession

from data import Data
from ssnbot import LOGGER

ask_ques = "ᴘʟᴇᴀꜱᴇ ᴄʜᴏᴏꜱᴇ ᴛʜᴇ ᴘʏᴛʜᴏɴ ʟɪʙʀᴀʀʏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ꜱᴛʀɪɴɢ ꜱᴇꜱꜱɪᴏɴ ꜰᴏʀ 🤖"
buttons_ques = [
    [
        InlineKeyboardButton("🍷ᴘʏʀᴏɢʀᴀᴍ🍷", callback_data="pyrogram"),
        InlineKeyboardButton("🍧ᴛᴇʟᴇᴛʜᴏɴ🍧", callback_data="telethon"),
    ],
]


@Client.on_message(filters.private & ~filters.forwarded & filters.command("generate"))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(
    bot: Client,
    msg: Message,
    telethon=False,
    old_pyro: bool = False,
    is_bot: bool = False,
):
    if telethon:
        ty = "Telethon"
    else:
        ty = "Pyrogram"
    if is_bot:
        ty += " Bot"
    await msg.reply(f"ꜱᴛᴀʀᴛɪɴɢ {ty} ꜱᴇꜱꜱɪᴏɴ ɢᴇɴᴇʀᴀᴛɪᴏɴ🪺...")

    user_id = msg.chat.id
    try:
        api_id_msg = await bot.ask_message(
            user_id, "Please send your `API_ID`", filters=filters.text, timeout=360
        )
    except TimeoutError:
        await msg.reply_text("ʀᴇQᴜᴇꜱᴛ ᴛɪᴍᴇᴅ ᴏᴜᴛ, ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴡɪᴛʜ /start")
        return

    if await cancelled(api_id_msg):
        return

    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "Not a valid API_ID (which must be an integer). ᴘʟᴇᴀꜱᴇ ꜱᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ꜱᴇꜱꜱɪᴏɴ ᴀɢᴀɪɴ🌱.",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return

    try:
        api_hash_msg = await bot.ask_message(
            user_id, "ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ʏᴏᴜʀ `API_HASH`", filters=filters.text, timeout=360
        )
    except TimeoutError:
        await msg.reply_text("ʀᴇQᴜᴇꜱᴛ ᴛɪᴍᴇᴅ ᴏᴜᴛ, ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴡɪᴛʜ /start")
        return
    if await cancelled(api_hash_msg):
        return

    api_hash = api_hash_msg.text
    if not is_bot:
        t = "ɴᴏᴡ ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ʏᴏᴜʀ `PHONE_NUMBER` ᴀʟᴏɴɢ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ⚡ \nᴇxᴀᴍᴘʟᴇ : `+19876543210`'"
    else:
        t = "ɴᴏᴡ ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ʏᴏᴜʀ `BOT_TOKEN` \nᴇxᴀᴍᴘʟᴇ : `12345:abcdefghijklmnopqrstuvwxyz`'"

    try:
        phone_number_msg = await bot.ask_message(
            user_id, t, filters=filters.text, timeout=360
        )
    except TimeoutError:
        await msg.reply_text("ʀᴇQᴜᴇꜱᴛ ᴛɪᴍᴇᴅ ᴏᴜᴛ, ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ /start")
        return
    
    if await cancelled(phone_number_msg):
        return

    phone_number = phone_number_msg.text
    await msg.reply("ꜱᴇɴᴅɪɴɢ ᴏᴛᴘ👀...")

    if telethon and is_bot:
        clientt = TelegramClient(StringSession(), api_id, api_hash)
        await clientt.start(bot_token=phone_number)
    elif telethon:
        clientt = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        clientt = Client(
            name="bot",
            api_id=api_id,
            api_hash=api_hash,
            bot_token=phone_number,
            in_memory=True,
        )
    else:
        clientt = Client(
            name="sess_user", api_id=api_id, api_hash=api_hash, in_memory=True
        )

    try:
        await clientt.connect()
    except Exception as e:
        LOGGER.error(e)

    try:
        code = None
        if not is_bot:
            if telethon:
                code = await clientt.send_code_request(phone_number)
            else:
                code = await clientt.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply(
            "`API_ID` and `API_HASH` ᴄᴏᴍʙɪɴᴀᴛɪᴏɴ ɪꜱ ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀꜱᴇ ꜱᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ꜱᴇꜱꜱɪᴏɴ ᴀɢᴀɪɴ😶.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply(
            "`PHONE_NUMBER` ɪꜱ ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀꜱᴇ ꜱᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ꜱᴇꜱꜱɪᴏɴ ᴀɢᴀɪɴ💤.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except PhoneNumberBanned:
        await msg.reply("`PHONE_NUMBER` ɪꜱ ʙᴀɴɴᴇᴅ, ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴡɪᴛʜ ᴀɴᴏᴛʜᴇʀ ɴᴜᴍʙᴇʀ🌪️")
        return
    except PhonePasswordFlood:
        await msg.reply(
            "ᴜɴᴀʙʟᴇ ᴛᴏ ꜱᴇɴᴅ ᴄᴏᴅᴇ, ʏᴏᴜ ʜᴀᴠᴇ ᴛʀɪᴇᴅ ʟᴏɢɢɪɴɢ ɪɴ ᴛᴏᴏ ᴍᴀɴʏ ᴛɪᴍᴇꜱ🍩"
        )
        return

    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask_message(
                user_id,
                "ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ꜰᴏʀ ᴀɴ ᴏᴛᴘ ɪɴ ᴏꜰꜰɪᴄɪᴀʟ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ. ɪꜰ ʏᴏᴜ ɢᴏᴛ ɪᴛ, ꜱᴇɴᴅ ᴏᴛᴘ ʜᴇʀᴇ ᴀꜰᴛᴇʀ ʀᴇᴀᴅɪɴɢ ᴛʜᴇ ʙᴇʟᴏᴡ ꜰᴏʀᴍᴀᴛ🍿 \nɪꜰ ᴏᴛᴘ ɪꜱ `12345`, **ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ɪᴛ ᴀꜱ** `1 2 3 4 5`.",
                filters=filters.text,
                timeout=360,
            )
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply(
            "ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏꜰ 5 ᴍɪɴᴜᴛᴇꜱ. ᴘʟᴇᴀꜱᴇ ꜱᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ꜱᴇꜱꜱɪᴏɴ ᴀɢᴀɪɴ ʙʏ ᴛᴀᴘᴘɪɴɢ😸 /start.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return

    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await clientt.sign_in(phone_number, phone_code, password=None)
            else:
                await clientt.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply(
                "ᴏᴛᴘ ɪꜱ ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀꜱᴇ ꜱᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ꜱᴇꜱꜱɪᴏɴ ᴀɢᴀɪɴ🌴",
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply(
                "ᴏᴛᴘ ɪꜱ ᴇxᴘɪʀᴇᴅ. ᴘʟᴇᴀꜱᴇ ꜱᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ꜱᴇꜱꜱɪᴏɴ ᴀɢᴀɪɴ🍬",
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
        except (
            SessionPasswordNeeded,
            SessionPasswordNeededError,
        ):
            try:
                two_step_msg = await bot.ask_message(
                    user_id,
                    "ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀꜱ ᴇɴᴀʙʟᴇᴅ ᴛᴡᴏ-ꜱᴛᴇᴘ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ. ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴘᴀꜱꜱᴡᴏʀᴅ🙈",
                    filters=filters.text,
                    timeout=300,
                )
            except TimeoutError:
                await msg.reply(
                    "ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏꜰ 5 ᴍɪɴᴜᴛᴇꜱ. ᴘʟᴇᴀꜱᴇ ꜱᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ꜱᴇꜱꜱɪᴏɴ ᴀɢᴀɪɴ ʙʏ ᴛᴀᴘᴘɪɴɢ /start.",
                    reply_markup=InlineKeyboardMarkup(Data.generate_button),
                )
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await clientt.sign_in(password=password)
                else:
                    await clientt.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (
                PasswordHashInvalid,
                PasswordHashInvalidError,
            ):
                await two_step_msg.reply(
                    "ɪɴᴠᴀʟɪᴅ ᴘᴀꜱꜱᴡᴏʀᴅ ᴘʀᴏᴠɪᴅᴇᴅ. ᴘʟᴇᴀꜱᴇ ꜱᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ꜱᴇꜱꜱɪᴏɴ ᴀɢᴀɪɴ🫧",
                    quote=True,
                    reply_markup=InlineKeyboardMarkup(Data.generate_button),
                )
                return
    else:
        try:
            if telethon:
                await clientt.start(bot_token=phone_number)
            else:
                await clientt.sign_in_bot(phone_number)
        except (AccessTokenInvalid, AccessTokenInvalidError):
            await msg.reply(
                "`BOT_TOKEN` ɪꜱ ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀꜱᴇ ꜱᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ꜱᴇꜱꜱɪᴏɴ ᴀɢᴀɪɴ🙁",
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return

    try:
        if telethon:
            string_session = clientt.session.save()
        else:
            string_session = await clientt.export_session_string()
    except Exception as e:
        LOGGER.error(e)

    text = f"**{ty.upper()} STRING SESSION** \n\n`{string_session}` \n\nɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @The_Architect04"
    try:
        if not is_bot:
            await clientt.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError as e:
        LOGGER.error(e)

    try:
        await clientt.disconnect()
    except Exception as e:
        LOGGER.error(e)

    await bot.send_message(
        msg.chat.id,
        "ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ɢᴇɴᴇʀᴀᴛᴇᴅ {} ꜱᴛʀɪɴɢ ꜱᴇꜱꜱɪᴏɴ. \n\nᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ꜱᴀᴠᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ🍫 \n\nʙʏ @The_Architect04".format(
            "telethon" if telethon else "pyrogram"
        ),
    )


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply(
            "Cancelled the Process!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    elif "/restart" in msg.text:
        await msg.reply(
            "Restarted the Bot!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("Cancelled the generation process!", quote=True)
        return True
    else:
        return False
