from pyrogram.types import InlineKeyboardButton


class Data:
    generate_single_button = InlineKeyboardButton("🔥 Start Generating Session 🔥", callback_data="generate")

    home_buttons = [
        [generate_single_button],
        [InlineKeyboardButton(text="🏠 Return Home 🏠", callback_data="home")]
    ]

    buttons = [
        [generate_single_button],
        [InlineKeyboardButton("✨ Bot Status and More Bots ✨", url="https://t.me/ELUpdates/8")],
        [
            InlineKeyboardButton("How to Use ❔", callback_data="help"),
            InlineKeyboardButton("🎪 About 🎪", callback_data="about")
        ],
        [InlineKeyboardButton("♥ More Amazing Bots ♥", url="https://t.me/ELUpdates")],
    ]

    START = """
**Hey {0}**

Welcome to {1}

If you don't trust this bot, 
> Please stop reading this message
> Delete this chat

Still reading?
You can use me to generate Pyrogram and Telethon string sessions. Use the buttons below to learn more!

By @ELUpdates**
    """

    HELP = """
✨ **Available Commands** ✨

/about - About the Bot
/help - This Message
/start - Start the Bot
/generate - Generate Session
/cancel - Cancel the process
/restart - Cancel and Restart the process
"""

    ABOUT = """
**About This Bot** 

Telegram Bot to generate Pyrogram and Telethon string sessions by @ELUpdates

Source Code: [Click Here](https://github.com/EL-Coders/SessionStringBot)

Framework: [Pyrogram](https://docs.pyrogram.org)

Language: [Python](https://www.python.org)

Developer: @CoderELAlpha
    """
