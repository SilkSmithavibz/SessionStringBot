from pyrogram.types import InlineKeyboardButton


class Data:
    generate_single_button = InlineKeyboardButton("🦋 ꜱᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ꜱᴇꜱꜱɪᴏɴ 🦋", callback_data="generate")

    home_buttons = [
        [generate_single_button],
        [InlineKeyboardButton(text="🧃 ʀᴇᴛᴜʀɴ ʜᴏᴍᴇ 🧃", callback_data="home")]
    ]

    buttons = [
        [generate_single_button],
        [InlineKeyboardButton("🍬 ʙᴏᴛ ꜱᴛᴀᴛᴜꜱ ᴀɴᴅ ᴍᴏʀᴇ ʙᴏᴛꜱ 🍬", url="https://t.me/The_Architect04/13")],
        [
            InlineKeyboardButton("👻 ʜᴏᴡ ᴛᴏ ᴜꜱᴇ 👻", callback_data="help"),
            InlineKeyboardButton("🌲 ᴀʙᴏᴜᴛ 🌲", callback_data="about")
        ],
        [InlineKeyboardButton("⚡ ᴍᴏʀᴇ ᴀᴍᴀᴢɪɴɢ ʙᴏᴛꜱ ⚡", url="https://t.me/The_Architect04")],
    ]

    START = """
**ʜᴇʏ {0}**

ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {1}

ɪꜰ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴛʀᴜꜱᴛ ᴛʜɪꜱ ʙᴏᴛ, 
> ᴘʟᴇᴀꜱᴇ ꜱᴛᴏᴘ ʀᴇᴀᴅɪɴɢ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ
> ᴅᴇʟᴇᴛᴇ ᴛʜɪꜱ ᴄʜᴀᴛ

ꜱᴛɪʟʟ ʀᴇᴀᴅɪɴɢ?
ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴍᴇ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴘʏʀᴏɢʀᴀᴍ ᴀɴᴅ ᴛᴇʟᴇᴛʜᴏɴ ꜱᴛʀɪɴɢ ꜱᴇꜱꜱɪᴏɴꜱ. ᴜꜱᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ʟᴇᴀʀɴ ᴍᴏʀᴇ!

ʙʏ @The_Architect04**
    """

    HELP = """
🌴 **ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ** 🌴

/about - ᴀʙᴏᴜᴛ ᴛʜᴇ ʙᴏᴛ
/help - ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ
/start - ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ
/generate - ɢᴇɴᴇʀᴀᴛᴇ ꜱᴇꜱꜱɪᴏɴ
/cancel - ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴇꜱꜱ
/restart - ᴄᴀɴᴄᴇʟ ᴀɴᴅ ʀᴇꜱᴛᴀʀᴛ ᴛʜᴇ ᴘʀᴏᴄᴇꜱꜱ
"""

    ABOUT = """
**ᴀʙᴏᴜᴛ ᴛʜɪꜱ ʙᴏᴛ** 

ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴘʏʀᴏɢʀᴀᴍ ᴀɴᴅ ᴛᴇʟᴇᴛʜᴏɴ ꜱᴛʀɪɴɢ ꜱᴇꜱꜱɪᴏɴꜱ ʙʏ @The_Architect04

ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ: [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://github.com/)

ꜰʀᴀᴍᴇᴡᴏʀᴋ: [ᴘʏʀᴏɢʀᴀᴍ](https://docs.pyrogram.org)

ʟᴀɴɢᴜᴀɢᴇ: [ᴘʏᴛʜᴏɴ](https://www.python.org)

ᴅᴇᴠᴇʟᴏᴘᴇʀ: @Marwin_ll
    """
