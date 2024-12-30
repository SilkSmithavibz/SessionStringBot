from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Data:
    # Inline buttons
    generate_single_button = InlineKeyboardButton(
        text="🦋 ʒᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʒᴇᴄᴄɪᴀᴏ 🦋",
        callback_data="generate"
    )

    # InlineKeyboardMarkup for "home" screen
    home_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [generate_single_button],
        [InlineKeyboardButton(text="🧃 ʀᴇᴛᴜʀɴ ʜᴏᴍᴇ 🧃", callback_data="home")]
    ])

    # InlineKeyboardMarkup for main buttons
    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [generate_single_button],
        [
            InlineKeyboardButton(text="👻 ʜᴏᴏ ᴛᴏ ᴜʀᴇ 👻", callback_data="help"),
            InlineKeyboardButton(text="🌲 ᴀʙᴏᴜᴛ 🌲", callback_data="about")
        ]
    ])

    # Text messages
    START = """
**ʜᴇʀ {0}**

ʜᴇʟᴏᴄʀᴇ ᴛᴏ {1}

ɪʟ ᴏᴜ ᴅᴏɴ'ᴛ ᴛʀᴜʟᴛ ᴛʜɪᴛ ʙᴏᴛ, 
> ᴘʟᴏᴇᴀᴅᴇ ᴛᴏᴏ ʀᴇᴀᴄʟɪᴏɴ
> ᴅᴇʟᴇᴛᴇ ᴛʜɪᴛ ᴄʜᴀᴛ

ᴛɪʟʟ ʀᴇᴀᴄᴇᴇɴɢ?
ᴜᴜ ᴀᴄᴀɴ ᴛᴇ ᴍᴇ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴘᴀʏʀᴏɢᴛᴀᴜ ᴀɴᴅ ᴛᴇʟᴇᴛʜᴏɴ ʒᴇᴄᴄɪᴀᴏᴄᴛᴇ. ᴜᴜᴇ ᴛᴇ ʙᴜᴛᴛᴏɴᴛʟ ʙᴇʟᴏᴜ ᴛᴏ ʟᴇᴀᴜʀᴇ ᴛʜᴇᴜ!

ʙᴇ @The_Architect04**
    """

    HELP = """
🌴 **ᴀᴠᴀɪʟᴇᴌᴇ ᴄᴏᴍᴍᴀᴎᴅᴛᴇ** 🌴

/about - ᴀʙᴏᴜᴛ ᴛʜᴇ ʙᴏᴛ
/help - ᴛʜɪᴛ ᴍᴇᴛᴛᴇᴄʒᴇ
/start - ᴛᴛᴀʀᴛ ᴛᴇ ʙᴏᴛ
/generate - ɢᴇɴᴇʀᴇ ʒᴇᴄᴄɪᴀᴏᴄᴛ
/cancel - ᴄᴀɴᴄᴇʟ ᴛᴇ ᴘʀᴏᴄᴇᴅᴛʀ
/restart - ᴄᴀɴᴄᴇʟ ᴀɴᴅ ʀᴇᴛʟᴀʀᴛ ᴛᴇ ᴘʀᴏᴄᴇᴅᴛʀ
"""

    ABOUT = """
🍄 **ᴀʙᴏᴜᴛ ᴛʜɪᴛ ʙᴏᴛ** 🍄

ᴛᴇʟᴇɢᴏᴄʜᴏ ʙᴏᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴘᴀʏʀᴏɢᴛᴀᴜ ᴀɴᴅ ᴛᴇʟᴇᴛʜᴏɴ ʒᴇᴄᴄɪᴀᴏᴄᴛᴇᴄᴇ @The_Architect04

ᴛᴏᴜʀᴆᴛᴆ ᴄᴏᴄᴇ: [ᴄ
